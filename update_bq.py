"""
Updates BigQuery with all new photos in photo upload directory. New rows will include photo directory,
exif timestamp, location abbreviation and correct timestamp columns.
This file takes 4 arguments: path to photo upload directory, path to MegaDetector json files,
path to BigQuery's key, and file name for CSV output file.
"""


import os
import argparse
import json
from datetime import datetime as dt
from PIL import Image, ExifTags
from google.cloud import bigquery

parser = argparse.ArgumentParser(
    description='Update BigQuery with new MegaDetector output')
parser.add_argument('upload_folder_dir', type=str,
                    help='Path to upload folder')
parser.add_argument('md_output_dir', type=str,
                    help='Path to MegaDetector json output directory')
parser.add_argument('bigquery_key', type=str,
                    help='Path to BigQuery json key file')
parser.add_argument('table_id', type=str,
                    help='Path to BigQuery table: e.g "project-name.dataset-name.table-name"')
args = parser.parse_args()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.bigquery_key
BASE_PATH = args.upload_folder_dir

# Construct a BigQuery client object.
client = bigquery.Client()


def drop_table(table_id):
  """
  Drops table every time script is run.

  If the table does not exist, delete_table raises
  google.api_core.exceptions.NotFound unless not_found_ok is True.
  """

  client.delete_table(table_id, not_found_ok=True)  # Make an API request.
  print(f"Deleted table '{table_id}'.")


def create_table(table_id):
  """
  Creates table using schema of uwin/multicity.
  """

  schema = [
      bigquery.SchemaField("photoDir", "STRING", mode="REQUIRED"),
      bigquery.SchemaField("exifTimestamp", "DATETIME", mode="NULLABLE"),
      bigquery.SchemaField("numAnimalDetections", "INTEGER", mode="NULLABLE"),
      bigquery.SchemaField("numHumanDetections", "INTEGER", mode="NULLABLE"),
      bigquery.SchemaField("jsonAnimalDetection", "STRING", mode="NULLABLE"),
      bigquery.SchemaField("jsonOtherDetection", "STRING", mode="NULLABLE"),
      bigquery.SchemaField("maxDetectionConf", "FLOAT", mode="NULLABLE"),
      bigquery.SchemaField("maxDetectionConfHuman", "FLOAT", mode="NULLABLE"),
      bigquery.SchemaField("exifImageDescription", "STRING", mode="NULLABLE"),
      bigquery.SchemaField("exifMake", "STRING", mode="NULLABLE"),
      bigquery.SchemaField("exifModel", "STRING", mode="NULLABLE"),
      bigquery.SchemaField("exifShutterSpeedValue", "FLOAT", mode="NULLABLE"),
      bigquery.SchemaField("exifApertureValue", "FLOAT", mode="NULLABLE"),
      bigquery.SchemaField("exifISOSpeedRatings", "FLOAT", mode="NULLABLE"),
      bigquery.SchemaField("imgWidth", "INTEGER", mode="NULLABLE"),
      bigquery.SchemaField("imgHeight", "INTEGER", mode="NULLABLE"),
  ]

  table = bigquery.Table(table_id, schema=schema)
  table = client.create_table(table)  # Make an API request.
  print(
      f"Created table {table.project}.{table.dataset_id}.{table.table_id}"
  )


def update_bq(detector_output_dir, table_id):
  """
  Loop through files MegaDetector output folder and
  update BigQuery table
  """

  rows_to_insert = []
  folderList = []
  # with open(csv_filename, "w+") as c:
  for dirpath, dirnames, filenames in os.walk(detector_output_dir):
    if dirpath is not detector_output_dir:
      continue

    for i in filenames:
      detector_output_file = os.path.join(detector_output_dir, i)
      folder_name = i.split(".")[0]
      # if datetime.now() - datetime.fromtimestamp(os.stat(detector_output).st_ctime) < timedelta(0, 0, 0, 0, 0, 1):
      if i.endswith(".json"):
        with open(detector_output_file) as f:
          images = json.load(f)

        for entry in images['images']:
          if i not in folderList:
            folderList.append(i)

          photoDir = os.path.join(BASE_PATH, folder_name, entry['file'])
          if ('detections' not in entry):
            print(photoDir, "Corrupted Image")

          rows_to_insert.append(get_image_data(entry, photoDir))

          if len(rows_to_insert) > 10000:
            errors = client.insert_rows_json(table_id, rows_to_insert)
            if not errors:
              folders = '[' + ', '.join(folderList) + ']'
              print(f"New {len(rows_to_insert)} rows have been added to BigQuery from MegaDetector files: {folders}")
            else:
              print(f"Encountered errors while inserting rows: {errors}")
            rows_to_insert = []
            folderList = []
      else:
        print(f"Skipping file {i}")
        # print(rows_to_insert)
  # print("rows: " , rows_to_insert[0])
  errors = client.insert_rows_json(table_id, rows_to_insert)
  if errors == []:
    folders = '[' + ','.join(folderList) + ']'
    print(f"New {len(rows_to_insert)} rows have been added to BigQuery from MegaDetector files: {folders}")
  else:
    print(f"Encountered errors while inserting rows: {errors}")


def get_image_data(entry, photoDir):
  """
  Returns all row information for 'photoDir' image.
  """

  numAnimalDetections = 0
  numHumanDetections = 0
  maxDetectionConfHuman = 0
  jsonAnimalDetection = ""  # if above 0.8
  maxDetectionConf = 0  # only animal detection confidence
  jsonOtherDetection = ""

  try:
    for detection in entry['detections']:
      if detection['category'] == '1':
        is_animal = True
        numAnimalDetections += 1
        jsonAnimalDetection += json.dumps(detection)
        if detection["conf"] > maxDetectionConf:
          maxDetectionConf = detection["conf"]

      elif detection['category'] == '2' and detection["conf"] > 0.8:
        is_human = True
        jsonOtherDetection += json.dumps(detection)
        numHumanDetections += 1
        if detection["conf"] > maxDetectionConfHuman:
          maxDetectionConfHuman = detection["conf"]
      elif detection['category'] == '3' and detection["conf"] > 0.8:
        is_car = True
        jsonOtherDetection += json.dumps(detection)

    try:
      img = Image.open(photoDir)
    except:
      return
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in ExifTags.TAGS
    }

    width, height = img.size

    # not sure if every camera has these values in their metadata
    # Timestamp, ImageDescription, Make, Model, ShutterSpeedValue, ApertureValue, ISOSpeedRatings
    try:
      exifTimestamp = dt.strptime(exif["DateTime"], '%Y:%m:%d %H:%M:%S')
      exifTimestamp = dt.strftime(exifTimestamp, '%Y-%m-%dT%H:%M:%S')
    except:
      exifTimestamp = None
    try:
      exifImageDescription = str(exif["ImageDescription"])
    except:
      exifImageDescription = None
    try:
      exifMake = exif["Make"]
    except:
      exifMake = None
    try:
      exifModel = exif["Model"]
    except:
      exifModel = None
    try:
      exifShutterSpeedValue = float(exif["ShutterSpeedValue"])
    except:
      exifShutterSpeedValue = None
    try:
      exifApertureValue = float(exif["ApertureValue"])
    except:
      exifApertureValue = None
    try:
      exifISOSpeedRatings = float(exif["ISOSpeedRatings"])
    except:
      exifISOSpeedRatings = None

  except KeyError as e:
    print(e.args)

  return {"photoDir": photoDir, "exifTimestamp": exifTimestamp, "numAnimalDetections": numAnimalDetections, "numHumanDetections": numHumanDetections,
          "jsonAnimalDetection": jsonAnimalDetection, "jsonOtherDetection": jsonOtherDetection, "maxDetectionConf": maxDetectionConf,
          "maxDetectionConfHuman": maxDetectionConfHuman, "exifImageDescription": exifImageDescription, "exifMake": exifMake,
          "exifModel": exifModel, "exifShutterSpeedValue": exifShutterSpeedValue, "exifApertureValue": exifApertureValue, "exifISOSpeedRatings": exifISOSpeedRatings,
          "imgWidth": width, "imgHeight": height}


if __name__ == "__main__":
  # first delete table if exists
  drop_table(args.table_id)
  # create table
  create_table(args.table_id)
  # update table
  update_bq(args.md_output_dir, args.table_id)
