import os
import csv
import argparse
#from datetime import datetime
from PIL import Image, ExifTags

parser = argparse.ArgumentParser(description='photo_uploads folder to csv.\
                                                Returns a csv .')
parser.add_argument('folder_path', type=str,
                    help='Path of photo folder to be processed')
parser.add_argument('dest_path', type=str,
                    help='Path of the destination folder for the csv')
args = parser.parse_args()


def createCSV(folder_path, dest_path):

  dir_name = folder_path.split("/")[-1]

  with open(dest_path+"/"+dir_name+".csv", "w+", encoding="utf8") as c:
    writer = csv.writer(c, escapechar='\\')

    firstline = True
    for root, dirs, files in os.walk(folder_path):

      folder_name = root.split("/")[-1]
      locAbbr = folder_name.split("_")[0]
      check_date = "_".join(folder_name.split("_")[1:4])

      for photo_name in files:

        if photo_name.split(".")[-1] == "JPG":

          img = Image.open(root + "/" + photo_name)
          exif = {
              ExifTags.TAGS[k]: v
              for k, v in img._getexif().items()
              if k in ExifTags.TAGS
          }

          if firstline:
            writer.writerow(
                ["folder_path", "locAbbr", "check_date", "photo_name"] + list(exif.keys()))
            firstline = False

          rowlist = [root, locAbbr, check_date, photo_name]

          for k in exif.keys():
            if k == "MakerNote":
              continue
            rowlist.append(exif[k])

          writer.writerow(rowlist)
          #print("Finished "+photo_name)
          continue

      print("Finished "+root)

  c.close()


if __name__ == "__main__":
  createCSV(args.folder_path, args.dest_path)
