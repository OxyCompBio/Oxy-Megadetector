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

import shutil

def remove_duplicates(input_list):

    no_duplicates = []

    for i in input_list:
        if i not in no_duplicates:
            no_duplicates.append(i)

    return no_duplicates


def main(input_folder, output_folder, photo_csv):

    pm = pd.read_csv(photo_csv)

    area_names = pm['areaName']
    loc_abbrs = pm['locationAbbr']

    visit_dates = pm['visitDatetime']
    visit_dates = list(visit_dates)

    photo_names = pm['photoName']
    #photo_names = list(set(list(photo_names)))

    photo_names = list(photo_names)
    photo_names = remove_duplicates(photo_names)

    area_names = list(area_names)
    # area_names = remove_duplicates(area_names)
    

    loc_abbrs = list(loc_abbrs)
    # loc_abbrs = remove_duplicates(loc_abbrs)

    area_names_col = list(pm['areaName'])
    area_names_col = list(map(lambda x: x.replace(', ', ''), area_names_col))

    # list of loc_abbrs_col -> reference by index

    loc_abbrs_col = list(pm['locationAbbr'])
    loc_abbrs_col = list(map(lambda x: x.split('-')[-1], loc_abbrs_col))

    # AustinTexas:
    # EML
    area_names = list(map(lambda x: x.replace(', ', ''), area_names))
    loc_abbrs = list(map(lambda x: x.split('-')[-1], loc_abbrs))

    area_names = list(area_names)
    area_names = remove_duplicates(area_names)

    loc_abbrs = list(loc_abbrs)
    loc_abbrs = remove_duplicates(loc_abbrs)

    city_vid_dict = {}

    for a in area_names:
        city_vid_dict[a] = {}


    for i, v in enumerate(visit_dates):
        
        date = v.split(' ')[0].replace('-', '_')

        city = area_names_col[i]
        
        site = loc_abbrs_col[i] 


        sd = site + '_' + date

        if sd not in city_vid_dict[city]:
                city_vid_dict[city][sd] = []
    
        city_vid_dict[city][sd].append(photo_names[i])
        

    # k = city
    # v = date
    # p = VID names
        # c = images

    # temporarily modify to return full_folder_paths
    # this allows us to check folder path names
    # gracefully exit if folder path names already exist

    fp = []
    imgs = []

    for k in city_vid_dict:
        for v in city_vid_dict[k].keys():
            
            img_path = str(k) + '/' + str(v)
            full_folder_path = output_folder + '/' + img_path 

            fp.append(full_folder_path)

    # https://stackoverflow.com/questions/8933237/how-do-i-check-if-directory-exists-in-python
            if not os.path.exists(full_folder_path):
                os.makedirs(full_folder_path)
            else:
                print("directory already exists")

            for c in city_vid_dict[k][v]:
                imgs.append(c)
                shutil.copy(input_folder + '/' + c, full_folder_path + '/' + c)

        print(k, v)

        # print(p)

    return [fp, imgs]

            

