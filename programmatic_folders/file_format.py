"""
Script to create VID subfolders inside the city name folders programmatically
No inputs
Outputs all VID subfolders for each city in local directory structure

To run the file:
python file_format.py
"""

import pandas as pd

import os

import logging

def main(input_folder, output_folder, photo_csv):

	pm = pd.read_csv(photo_csv)

	area_names = pm['areaName']
	loc_abbrs = pm['locationAbbr']

	visit_dates = pm['visitDatetime']
	visit_dates = list(set(list(visit_dates)))

	photo_names = pm['photoName']
	photo_names = list(set(list(photo_names)))


	area_names = list(set(list(area_names)))
	loc_abbrs = list(set(list(loc_abbrs)))

	area_names_col = list(pm['areaName'])
	area_names_col = list(map(lambda x: x.replace(', ', ''), area_names_col))

	# list of loc_abbrs_col -> reference by index

	loc_abbrs_col = list(pm['locationAbbr'])
	loc_abbrs_col = list(map(lambda x: x.split('-')[-1], loc_abbrs_col))

	# AustinTexas
	# EML
	area_names = list(map(lambda x: x.replace(', ', ''), area_names))
	loc_abbrs = list(map(lambda x: x.split('-')[-1], loc_abbrs))

	city_vid_dict = {}

	for a in area_names:
		city_vid_dict[a] = {}


	for i, v in enumerate(visit_dates):
		
		date = v.split(' ')[0].replace('-', '_')

		city = area_names_col[i]
		
		site = loc_abbrs_col[i] 

		city_vid_dict[city][site + '_' + date] = True  

	# k = city
	# v = date
	# p = VID names

	for k in city_vid_dict:
		for v in city_vid_dict[k].keys():
			
			img_path = str(k) + '/' + str(v)
			full_img_path = output_folder + '/' + img_path 

	# https://stackoverflow.com/questions/8933237/how-do-i-check-if-directory-exists-in-python
			if not os.path.exists(full_img_path):
				os.makedirs(full_img_path)


