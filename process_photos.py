import os
import csv
import argparse
#from datetime import datetime
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS


parser = argparse.ArgumentParser(description='photo_uploads folder to csv.\
                                                Returns a csv .')
parser.add_argument('folder_path', type=str,
                    help='Path of photo folder to be processed')
parser.add_argument('dest_path', type=str,
                    help='Path of the destination folder for the csv')
args = parser.parse_args()


def createCSV(folder_path, dest_path):

  dir_name = folder_path.split("/")[-1]

  # create a csv file and a writer object
  with open(dest_path+"/"+dir_name+".csv", "w+", encoding="utf8") as c:
    writer = csv.writer(c, escapechar='\\')

    # create the header row
    firstrow = ["folder_path", "locAbbr", "check_date", "photo_name"]
    for k in TAGS:
      firstrow.append(TAGS[k])

    writer.writerow(firstrow)

    # iterate through directory, including subdirectories
    for root, dirs, files in os.walk(folder_path):

      folder_name = root.split("/")[-1]
      locAbbr = folder_name.split("_")[0]
      check_date = "_".join(folder_name.split("_")[1:4])

      for photo_name in files:

        # input validation
        if photo_name.split(".")[-1] == "JPG":

          try:
            img = Image.open(root + "/" + photo_name)
          except UnidentifiedImageError:
            writer.writerow([root, locAbbr, check_date,
                            photo_name] + ["Corrupted"]*(len(firstrow)-4))
            continue

          # rip exif data from image and create list to become row
          exif = img._getexif()

          rowlist = [root, locAbbr, check_date, photo_name]

          # assign each item in exif dict to appropriate row
          for k in TAGS:
            if TAGS[k] == "MakerNote":
              rowlist.append("Omitted")
              continue
            if k in exif.keys():
              rowlist.append(exif[k])
            else:
              rowlist.append("N/A")

          # write the row and repeat ad nauseum
          writer.writerow(rowlist)
          continue

      print("Finished "+root)

  c.close()


if __name__ == "__main__":
  createCSV(args.folder_path, args.dest_path)
