import csv
import os
import json
import argparse
from PIL import Image, ExifTags


parser = argparse.ArgumentParser(description = 'Convert MegaDetector JSON file to csv.\
                                                Returns a csv of the same name as the json file.')
parser.add_argument('md_output', type=str,
                    help='Path to MegaDetectors JSON file')
parser.add_argument('base_path', type=str,
                    help='Path to photos in MegaDetectors JSON file')
args = parser.parse_args()

BASE_PATH = args.base_path

def createCSV(md_output):
  md_output_csv = md_output.split(".")[0] + ".csv"
  counter = 0
  with open(md_output_csv, "w+") as c:
    writer = csv.writer(c)
    with open(md_output, "r") as detector_output:
        images = json.load(detector_output)

        for entry in images['images']:
          counter += 1
          # print(counter)
          photoDir = os.path.join(BASE_PATH, entry['file'])
          # print(photoDir)

          numAnimalDetections = 0
          numHumanDetections = 0
          maxDetectionConfHuman = 0
          jsonAnimalDetection = "" # if above 0.8
          maxDetectionConf = 0 # only animal detection confidence
          jsonOtherDetection = ""
          try:
            for detection in entry['detections']:
              if detection['category'] == '1':
                is_animal = True
                numAnimalDetections += 1
                jsonAnimalDetection += str(detection)
                if detection["conf"] > maxDetectionConf:
                  maxDetectionConf = detection["conf"]

              elif detection['category'] == '2' and detection["conf"] > 0.8:
                is_human = True
                jsonOtherDetection += str(detection)
                numHumanDetections += 1
                if detection["conf"] > maxDetectionConfHuman:
                  maxDetectionConfHuman = detection["conf"]
              elif detection['category'] == '3' and detection["conf"] > 0.8:
                is_car = True
                jsonOtherDetection += str(detection)
              # elif detection['category'] == '1':
              # 	jsonOtherDetection += str(detection)
              # 	if detection["conf"] > maxDetectionConf:
              # 		maxDetectionConf = detection["conf"]
              # print(detection)
              
              img = Image.open(os.path.join(BASE_PATH, entry['file']))
            exif = {
                ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in ExifTags.TAGS
            }

            # not sure if every camera has these values in their metadata
            # DateTime, ImageDescription, Make, Model, ShutterSpeedValue, ApertureValue, ISOSpeedRatings
            try: exifTimestamp = exif["DateTime"]
            except: exifTimestamp = None
            try: exifImageDescription = exif["ImageDescription"]
            except: exifImageDescription = None
            try: exifMake = exif["Make"]
            except: exifMake = None
            try: exifModel = exif["Model"]
            except: exifModel = None
            try: exifShutterSpeedValue = exif["ShutterSpeedValue"]
            except: exifShutterSpeedValue = None
            try: exifApertureValue = exif["ApertureValue"]
            except: exifApertureValue = None
            try: exifISOSpeedRatings = exif["ISOSpeedRatings"]
            except: exifISOSpeedRatings = None

            writer.writerow([photoDir, str(numAnimalDetections), str(jsonAnimalDetection), str(numHumanDetections), str(jsonOtherDetection), maxDetectionConf, 
                             maxDetectionConfHuman, exifTimestamp, exifImageDescription, exifMake, exifModel, exifShutterSpeedValue, exifApertureValue, exifISOSpeedRatings])
          except KeyError:
            print(KeyError)
            continue
        detector_output.close()
    c.close()
  
if __name__ == "__main__":
    createCSV(args.md_output)
