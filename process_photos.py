import os
import csv
import argparse
from datetime import datetime
from PIL import Image, ExifTags

#what arguments do we need?
#just folder path, since we will turn each individual photo into a row in the csv
#after you get the csv, upload it to the AFC-UWIN folder in gdrive - leave this until after testing

parser = argparse.ArgumentParser(description = 'photo_uploads folder to csv.\
                                                Returns a csv .')
parser.add_argument('folder_name', type=str,
                    help='Name of photo folder')
args = parser.parse_args()

def createCSV(folder_name): 

    folder_path = os.getcwd() + "/" + folder_name #could I just replace this with folder_name in every case and have it still work
                                                  #bc the .py file is assumed to be in the same working directory as the folder?
                                                  #we still need the folder path anyway bc it's a column in the csv so I spose keep it
                                                  #change blah

    with open(os.getcwd()+"/"+folder_name+".csv", "w+") as c: #same deal here: is the os.getcwd necessary?
        writer = csv.writer(c, escapechar='\\')
        locAbbr = folder_name.split("_")[0]
        check_date = "_".join(folder_name.split("_")[1:4])

        firstline = True
        for photo_name in os.listdir(folder_path): #!!
                                   
            img = Image.open(folder_path + "/" + photo_name) #!!
            exif = {
                ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in ExifTags.TAGS
            }    
            
            if firstline:
                writer.writerow(["folder_path", "locAbbr", "check_date", "photo_name"] + list(exif.keys()))
                firstline = False
            
            rowlist = [folder_path, locAbbr, check_date, photo_name]

            #legitimately not sure what to do about the dates vis a vis UTC
            for k in exif.keys():
                if k == "MakerNote":
                    continue
                #elif k.contains("DateTime"):
                    #something with isoformat
                #else:
                #print(k, exif[k])
                rowlist.append(exif[k])

            #print and check for special charachters (commas, double-quotes)
            #print(rowlist)

            writer.writerow(rowlist)
            print("Finished "+photo_name)
            continue
    c.close()
    
if __name__ == "__main__":
  createCSV(args.folder_name)
