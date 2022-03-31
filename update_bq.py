"""
Updates BigQuery with all new photos in photo upload directory. New rows will include photo directory,
exif timestamp, location abbreviation and correct timestamp columns.

This file takes 4 arguments: path to photo upload directory, path to MegaDetector json files,
path to BigQuery's key, and file name for CSV output file.
"""

import os
from google.cloud import bigquery
from datetime import datetime, timedelta
import json
import argparse
# import exif
import csv
from PIL import Image, ExifTags
from datetime import datetime as dt

parser = argparse.ArgumentParser(description = 'Update BigQuery with new MegaDetector output')
parser.add_argument('upload_folder_dir', type=str,
                                        help='Path to upload folder')
parser.add_argument('md_output_dir', type=str,
                                        help='Path to MegaDetector json output directory')
parser.add_argument('bigquery_key', type=str,
                                        help='Path to BigQuery json key file')
parser.add_argument('csv_filename', type=str,
                                        help='Filename for CSV output file')
args = parser.parse_args()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.bigquery_key
BASE_PATH = args.upload_folder_dir


def updateBQ(detector_output_dir, csv_filename):
        client = bigquery.Client()
        rows_to_insert = []
        with open(csv_filename, "w+") as c:
                for dirpath, dirnames, filenames in os.walk(detector_output_dir):
                        if dirpath is not detector_output_dir:
                                continue

                        for i in filenames:
                                detector_output = os.path.join(detector_output_dir, i)
                                # if datetime.now() - datetime.fromtimestamp(os.stat(detector_output).st_ctime) < timedelta(0, 0, 0, 0, 0, 1):
                                if True:
                                        with open (detector_output) as f:
                                                images = json.load(f)

                                        rows_to_insert = appendCSV(images, c, i, rows_to_insert)
                                        # print(rows_to_insert)
        print("rows: " , rows_to_insert[0])
        errors = client.insert_rows_json("afc-uwin.photos.uwin", rows_to_insert)
        if errors == []:
                print("New rows have been added to BigQuery for MegaDetector file: {}".format(i))
        else:
                print("Encountered errors while inserting rows: {}".format(errors))


def appendCSV(images, csv_file, json_file, rows_to_insert):
#   md_output_csv = md_output.split(".")[0] + ".csv"
        folder_name = json_file.split(".")[0]
        for entry in images['images']:
#               counter += 1
                # print("inside: ", entry['file'])
                photoDir = os.path.join(BASE_PATH, folder_name, entry['file'])
                # print(photoDir)

                numAnimalDetections = 0
                numHumanDetections = 0
                maxDetectionConfHuman = 0
                jsonAnimalDetection = "" # if above 0.8
                maxDetectionConf = 0 # only animal detection confidence
                jsonOtherDetection = ""
                if ('detections' not in entry):
                        print(photoDir, 0)
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

                                try: img = Image.open(photoDir)
                                except: continue
                                exif = {
                                        ExifTags.TAGS[k]: v
                                        for k, v in img._getexif().items()
                                        if k in ExifTags.TAGS
                                }
    
                                width, height = img.size

                                # not sure if every camera has these values in their metadata
                                # DateTime, ImageDescription, Make, Model, ShutterSpeedValue, ApertureValue, ISOSpeedRatings
                                try: exifTimestamp = dt.strptime(exif["DateTime"], '%Y:%m:%d %H:%M:%S'); exifTimestamp = dt.strftime(exifTimestamp, '%Y-%m-%dT%H:%M:%S')
                                except: exifTimestamp = None
                                try: exifImageDescription = str(exif["ImageDescription"])
                                except: exifImageDescription = None
                                try: exifMake = exif["Make"]
                                except: exifMake = None
                                try: exifModel = exif["Model"]
                                except: exifModel = None
                                try: exifShutterSpeedValue = float(exif["ShutterSpeedValue"])
                                except: exifShutterSpeedValue = None
                                try: exifApertureValue = float(exif["ApertureValue"])
                                except: exifApertureValue = None
                                try: exifISOSpeedRatings = float(exif["ISOSpeedRatings"])
                                except: exifISOSpeedRatings = None
                                rows_to_insert.append({"photoDir": photoDir, "exifTimestamp": exifTimestamp, "numAnimalDetections": numAnimalDetections, "numHumanDetections": numHumanDetections,
                                                                "jsonAnimalDetection": jsonAnimalDetection, "jsonOtherDetection": jsonOtherDetection, "maxDetectionConf": maxDetectionConf,
                                                                "maxDetectionConfHuman": maxDetectionConfHuman, "exifImageDescription": exifImageDescription, "exifMake": exifMake,
                                                                "exifModel": exifModel, "exifShutterSpeedValue": exifShutterSpeedValue, "exifApertureValue": exifApertureValue, "exifISOSpeedRatings": exifISOSpeedRatings,
                                                        "imgWidth": width, "imgHeight": height})
                except KeyError as e:
                        print(e.args)
                        continue
        return rows_to_insert


if __name__ == "__main__":
        updateBQ(args.md_output_dir, args.csv_filename)
