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

# get directory of file even in different folder
print(__file__)

print("os path dirname")
print(os.path.dirname(__file__))

pm = pd.read_csv(os.path.dirname(__file__) + '/photo_detection_metadata.csv')

vid_nums = pm['filepath']

# #print(vid_nums)

vid_nums = list(set(list(vid_nums)))

# Filter out "Lure Study"
# vid_nums.remove("Lure Study")

# print(vid_nums[0:2])

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
# characters 28-35 in photo csv
# add 20

for v in vid_nums:
	start = 20
	end = v[20:].find('/') + 20

	# initialize keys in dict
	if v[start:end] not in city_vid_dict:
		city_vid_dict[v[start:end]] = {}	
 
	#if v[start:end] in city_vid_dict:
	# vid_var = v[48:55]

	#print("basename")
	#print(os.path.basename(v))
	
	vid_var = os.path.basename(v)
	vid_var = vid_var.split('-')[0]

	city_vid_dict[v[start:end]][vid_var] = True  


# print(list(city_vid_dict.values())[0])

#with open('processed_cities.txt', 'w') as f:
 #   for c in processed_cities:
  #      f.write(f"{c}\n")


#with open('city_vid_dict_entries.txt', 'w') as f:
#	for k, v in city_vid_dict.items():
#		f.write(f"{k,v}\n")

# print(list(city_vid_dict)

for k in city_vid_dict:
	for v in city_vid_dict[k].keys():
		os.makedirs(str(k) + '/' + str(v))

# {Austin: vid1, vid2, ...}
# makedirs -p flag in Python
# os.path.dirnamei()

 


