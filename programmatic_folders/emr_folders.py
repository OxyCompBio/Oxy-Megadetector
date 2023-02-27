"""
Script to create VID subfolders inside the city name folders programmatically
No inputs
Outputs all VID subfolders for each city in local directory structure

To run the file:
python emr_folders.py
"""

import pandas as pd

import re

import os

pm = pd.read_csv(os.path.dirname(__file__) + '/photo_detection_metadata.csv')

vid_nums = pm['filepath']
vid_nums = list(set(list(vid_nums)))

# filter out "Lure Study"
vid_nums.remove("Lure Study")

city_vid_dict = {}

# first, get all city codes
# then, use city codes as hash key
# then, put vids as values
# then keys are one list - subfolder 1
# then, vids go inside their respective subfolders

# populate dict keys with city codes
# start at index 20 to get city code (e.g., chil for Chicago, IL)
# this assumes a uniform format - 'gs://urban-wildlife-chil/CHIL-D02-RCP1-01232020/VID7357-00000.jpg' 

print("cities")
print(city_vid_dict)

# populate dict values with vids

for v in vid_nums:
	start = 20
	end = v[20:].find('/') + 20

	# initialize keys in dict
	if v[start:end] not in city_vid_dict:
		city_vid_dict[v[start:end]] = {}	
	
	vid_var = os.path.basename(v)
	vid_var = vid_var.split('-')[0]

	city_vid_dict[v[start:end]][vid_var] = True  


for k in city_vid_dict:
	for v in city_vid_dict[k].keys():
		os.makedirs(str(k) + '/' + str(v))
 


