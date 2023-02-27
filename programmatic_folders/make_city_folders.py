"""
Use this script to create city names from the photo detection metadata csv!

Run the script with the following command:
python make_city_folders.py 

No inputs
Outputs processed_cities.txt, which is a text file with the city names from photo detection metadata csv
"""

import pandas as pd
import re
import os

pm = pd.read_csv(os.path.dirname(__file__) + '/photo_detection_metadata.csv')

city_names = pm['areaName']

# convert pandas city_names series into a unique list
print(list(set(list(city_names))))

city_names = list(set(list(city_names)))

# filter out "Lure Study"
city_names.remove("Lure Study")

# print(city_names)

processed_cities = []

for c in city_names:
	
	# https://stackoverflow.com/questions/12985456/replace-all-non-alphanumeric-characters-in-a-string
	re_city = re.sub(r'\W+', '', c)
	processed_cities.append(re_city)

# print("Cities:")
# print(processed_cities)

with open('processed_cities.txt', 'w') as f:
    for c in processed_cities:
        f.write(f"{c}\n")

# print(pm)
