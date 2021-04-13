import json
import argparse
import os
import shutil
import datetime

parser = argparse.ArgumentParser(description = 'Extract exif data from an image')
parser.add_argument('file_location', type=str, help='Path to detector output file')
parser.add_argument('output_dest', type=str, help='Desired path for animal photos to be copied. May or may not exist.')
args = parser.parse_args()


def copy_files(detector_output, images_output):
	files = []
	animal_dir = images_output + '/animal' + str(datetime.datetime.now())
	os.makedirs(animal_dir)
	with open (detector_output) as f:
		images = json.load(f)
		
	for entry in images['images']:
		
		is_animal = False

		for detection in entry['detections']:

			if detection['category'] == '1' and entry['max_detection_conf'] > 0.8:

				is_animal = True
				files.append(entry['file'])



		#category = entry['detections'][0]['category']
		
		#if category == '1':
			
		#	files.append(entry['file'])
	
	
	for image_file in files:
		shutil.copy(image_file, animal_dir)
	

if __name__ == "__main__":
	copy_files(args.file_location,args.output_dest)
