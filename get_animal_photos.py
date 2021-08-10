"""
Get animal photos: this file takes two arguments, path to detector output .json file and desired output location for photos with animal detections to be copied.
Creates a folder titled 'animal' + the date and time this program was executed.
Created by Miles Koupal.
"""

# python get_animal_photos.py "C:\Users\baezh\OneDrive\Desktop\Oxy\Spring2021\Megadetector\MegaDetectorOutput" 
# "C:\Users\baezh\OneDrive\Desktop\Oxy\Spring2021\Megadetector\Photo_Archive" "C:\Users\baezh\OneDrive\Desktop\Oxy\Spring2021\Megadetector\Photo_Upload"
import json
import argparse
import os
import shutil
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description = 'Extract exif data from an image')
parser.add_argument('file_location', type=str, help='Path to detector output directory')
parser.add_argument('output_dest', type=str, help='Desired path for animal photos to be copied. May or may not exist.')
parser.add_argument('base_path', type=str, help='photos upload base path')
args = parser.parse_args()

BASE_PATH = args.base_path

def copy_files(detector_output_dir, images_output):
  for dirpath, dirnames, filenames in os.walk(detector_output_dir):
    if dirpath is not detector_output_dir:
      continue

    for i in filenames:
      detector_output = os.path.join(detector_output_dir, i)
      if datetime.now() - datetime.fromtimestamp(os.stat(detector_output).st_ctime) < timedelta(0, 0, 0, 0, 0, 1):
        files = []

        with open (detector_output) as f:
          images = json.load(f)
          
        for entry in images['images']:
          imgPath = i.split('.')[0] + '/' + entry['file']
          print(entry['file'])

          # add first and last image from folder
          if entry['file'] == images['images'][0]['file'] or entry['file'] == images['images'][-1]['file']:
            print("first/last")
            files.append(imgPath)
            continue

          for detection in entry['detections']:

            if detection['category'] == '1' and entry['max_detection_conf'] > 0.8:
              files.append(imgPath)
              continue
        
        
        for image_file in files:
          source = os.path.join(BASE_PATH, image_file)
          destination = os.path.join(images_output, image_file)

          if not os.path.isdir(os.path.dirname(os.path.join(images_output, image_file))):
            os.makedirs(os.path.dirname(os.path.join(images_output, image_file)))
      
          shutil.copy(source, destination)

if __name__ == "__main__":
  copy_files(args.file_location,args.output_dest)
