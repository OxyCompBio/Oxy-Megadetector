'''
This file populates a CSV file of images with detection categories and confidences from a megadetector output
It takes three arguments, path to json output, path to CSV file and desired output path for copy of your CSV file
'''

from csv import reader
from csv import writer
import json
import os
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(
    description='Update CSV file with megadetector detections and categories')
parser.add_argument('detector_json', type=str,
                    help='Path to megadetector output file')
parser.add_argument('input_csv', type=str,
                    help='CSV file to be updated with megadetector detections')
parser.add_argument('output_path', type=str,
                    help='Desired path to updated CSV - include name')
args = parser.parse_args()


def update_csv(detector_output, input_csv, output_path):

  with open(input_csv, 'r') as read, open(output_path, 'w') as write, open(detector_output) as ref:

    csv_reader = reader(read)
    csv_writer = writer(write)
    images = json.load(ref)
    # print(len(images['images']))
    csv_writer.writerow(['photodir', 'isEmpty', 'hasExif', 'successfulOCR', 'OCRtimeStamp',
                        'exifTimeStamp', 'lastModifiedTimeStamp', 'detections catgegory/conf'])
    next(csv_reader, None)

    for row in tqdm(csv_reader):

      filename = str(row[0])

      for entry in images['images']:

        categories = []
        confs = []

        if entry['file'] == filename:

          for detection in entry['detections']:

            category = detection['category'] + '/'
            confidence = str(detection['conf']) + '/'
            categories.append(category)
            confs.append(confidence)

          # print(str(detections))
          categories_string = ''.join(categories)
          confs_string = ''.join(confs)
          row.append(categories_string)
          row.append(confs_string)
          # elif len(detections) == 0:
          # row.append('0')
          csv_writer.writerow(row)


if __name__ == '__main__':
  update_csv(args.detector_json, args.input_csv, args.output_path)
