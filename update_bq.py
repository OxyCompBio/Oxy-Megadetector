import os
from google.cloud import bigquery
from datetime import datetime, timedelta
import json
import argparse
import exif

parser = argparse.ArgumentParser(description = 'Update BigQuery with new MegaDetector output')
parser.add_argument('file_location', type=str, help='Path to detector output directory')
parser.add_argument('bigquery_key', type=str, help='Path to BigQuery json key file')
parser.add_argument('base_path', type=str, help='photos base path')
args = parser.parse_args()

BASE_PATH = args.base_path

# python update_bq.py "C:\Users\baezh\OneDrive\Desktop\Oxy\Spring2021\Megadetector\MegaDetectorOutput\AST1_2019_01_01.json"
# "C:\PythonProjects\CameraTraps\detection\gdrive-uwin-8a3068713c42.json" "C:\Users\baezh\OneDrive\Desktop\Oxy\Spring2021\Megadetector\Photo_Upload"
"""
Add new rows to BigQuery: photoDir, locationAbbr, exifTimestamp
"""
def updateBQ(detector_output_dir):
	client = bigquery.Client()
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
					
					is_animal = False
					is_human = False
					is_car = False
					print(entry['file'][:4])

					timestamp = str(datetime.strptime(exif.Image(os.path.join(BASE_PATH, entry['file'])).datetime, "%Y:%m:%d %H:%M:%S"))

					for detection in entry['detections']:
						if detection['category'] == '1' and entry['max_detection_conf'] > 0.8 and is_animal is False:
							is_animal = True
						elif detection['category'] == '2' and entry['max_detection_conf'] > 0.8 and is_human is False:
							is_human = True
						elif detection['category'] == '3' and entry['max_detection_conf'] > 0.8 and is_car is False:
							is_car = True
				
					if not is_animal and not is_human and not is_car:
						files.append([entry['file'], timestamp, "Empty", entry['file'][:4]])
					elif is_animal:
						files.append([entry['file'], timestamp, "Animal", entry['file'][:4]])
					elif is_human:
						files.append([entry['file'], timestamp, "Person", entry['file'][:4]])
					elif is_car:
						files.append([entry['file'], timestamp, "Car", entry['file'][:4]])

				rows_to_insert = []
				for file in files:
					print(file[0])

					rows_to_insert.append({"photoDir": file[0], "isEmpty": 0, "hasExif": 1, "successfulOCR": 0, "ocrTimestamp": None, "exifTimestamp": file[1],
											"lastModTimestamp": None, "photoDatetime": None, "locationAbbr": file[3], "photoName": None, "commonName": file[2], "numIndividuals": None, "correctTimestamp": file[1]})
					break

				errors = client.insert_rows_json("photos.PACAGDRIVE", rows_to_insert)
				if errors == []:
					print("New rows have been added to BigQuery.")
				else:
					print("Encountered errors while inserting rows: {}".format(errors))
        

if __name__ == "__main__":
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.bigquery_key
	updateBQ(args.file_location)