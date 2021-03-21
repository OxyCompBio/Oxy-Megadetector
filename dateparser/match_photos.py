#!/home/compbio/miniconda2/envs/dateparser/bin/python
import os
import cv2
# import csv
import pytesseract
from datetime import datetime
import logging
import logging.handlers
from mysql.connector import Error
# from mysql_config import read_db_config
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy
import re
import json


dir_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(dir_path, "match-photos.log")
handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", log_path))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)



engine = sqlalchemy.create_engine('mysql+pymysql://root:root@10.213.0.5:3307/csv_db')
Session = scoped_session(sessionmaker(bind=engine))
s = Session()

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# returns dictionary
# key: timestamp    value: image
def ocrDateTime(image_dir):
    timeDict = {}
    i = 0
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('.JPG') or file.endswith('.PNG') or file.endswith('.JPEG'):
                #print(root)
                image = cv2.imread(root + "/" + file)
                gray = get_grayscale(image)
                thresh = thresholding(gray)
                x,y,w,h = 1650, 2063, 2190, 97
                ROI = thresh[y:y+h,x:x+w]
                #print(i, '\n')
                ocrtime = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6').split()
                print(file + ":     " , ocrtime)
                i += 1
                print(i)

                try:
                    date1 = ocrtime[0] + " " + ocrtime[1]
                    print(date1)
                    start = re.search(r'\d', date1)
                    date1 = date1[start.start():]
                    #print(date1)
                    date1 = datetime.strptime(date1, '%m/%d/%Y %H:%M%p')
                    #print(date1)
                    # isodate = date1.isoformat()
                    # print(isodate)
                    # print(date1.isoformat())
                    # timeDict[date1] = root + "/" + file
                    # directory = root.replace("C:\\PythonProjects\\Tesseract_01\\", "")
                    photoDir = root + "/" + file
                    timeDict[str(date1)] = photoDir
                    # photoDir = photoDir.replace("\\", "\\\\")
                    # print(photoDir)
                    # photoDir.replace("C:\\PythonProjects\\Tesseract_01\\", "")
                    # print(photoDir)
                    # print(str(date1)[:-3])
                    print("File:    " + photoDir + "            Time:    " + str(date1)[:-3])
                    # updatePhotoDir(photoDir, str(date1)[:-3]
                    
                except:
                    logging.warning("File:    " + photoDir + "            Time:    " + date1)
                    continue
    return timeDict


# def update():
#     with open('PACA_TIMESTAMPS.csv') as csv_read, open('newPACA_TIMESTAMPS.csv', "w", newline="") as csv_write:

#         csv_reader = csv.reader(csv_read)
#         csv_writer = csv.writer(csv_write)

#         for row in csv_reader:
#             row.append("NULL")
#             # print(row)
#             csv_writer.writerow(row)



# def updateCSV(timeDict):
#     csvfile = pd.read_csv("SpeciesTimestamp.csv")

#     with open('SpeciesTimestamp.csv', "r+") as csv_file:
#         csv_reader = csv.reader(csv_file)
#         i = 0
#         for row in csv_reader:
#             if i == 0:
#                 i += 1
#                 continue
#             time = row[1].split(":")
#             time = time[0] + ":" + time[1] + ":00"
#             print(time)
#             if time in timeDict:
#                 csv.loc[i, "PhotoDir"] = timeDict[time] 
#                 print(row)
#             i += 1

def updatePhotoDir(photoDir, photoDateTime):
    query = 'UPDATE timestamp ts SET ts.photoDir = "{arg1}" WHERE ts.photoDateTime LIKE "{arg2}%" AND ts.photoDir IS NULL LIMIT 1'.format(arg1 = photoDir, arg2 = photoDateTime)
    # print('UPDATE timestamp ts SET ts.photoDir = "{arg1}" WHERE ts.photoDateTime LIKE "{arg2}%"'.format(arg1 = photoDir, arg2 = photoDateTime))

    try:
        s.execute(query)
        s.commit()
        # db_config = read_db_config()
        # conn = MySQLConnection(**db_config)

        # cursor = conn.cursor()
        # cursor.execute(query)

        # conn.commit()
    except Error as error:
        print(error)

def update():
    query = 'SELECT * FROM timestamp ts WHERE ts.photoDateTime LIKE "%s%"'()
    result = s.execute(query)
    # print(result.count())
    for i in result:
        print(i[4].split(':'))


if __name__ == "__main__":
    timeDict = ocrDateTime("/home/compbio/Photos")
    with open('data.json', 'w') as fp:
    	json.dump(timeDict, fp)
    # updateCSV(timeDict)

    # update()

    # timestamp = datetime.strptime('7/5/2019  7:36:00 PM', '%m/%d/%Y %I:%M:%S %p')
    # isodate = timestamp.isoformat()
    # print(isodate)



 # row = {'locationAbbr': r['locationAbbr'], 
#     'utmEast': r['utmEast'], 
#     'utmNorth': r['utmNorth'], 
#     'utmZone': r['utmZone'], 
#     'photoDateTime': r['photoDateTime'],
#     'defaultTimeZone': r['defaultTimeZone'],
#     'photoName': r['photoName'],
#     'commonName': r['commonName'],
#     'numIndividuals': r['numIndividuals'],
#     'valStatID': r['valStatID'],
#     'PhotoDir': r['PhotoDir']}
