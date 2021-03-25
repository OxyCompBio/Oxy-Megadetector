#!/home/compbio/miniconda2/envs/dateparser/bin/python
import os
import cv2
import pytesseract
from datetime import datetime
import logging
import logging.handlers
import re
import json
from collections import defaultdict


dir_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(dir_path, "match-photos.log")
handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", log_path))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)



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
            if file.endswith('.JPG') or file.endswith('.PNG') or file.endswith('.JPEG') or file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                try:
                    image = cv2.imread(root + "/" + file)
                    gray = get_grayscale(image)
                except:
                    logging.info("File:    " + root + "/" + file)
                    continue
                #logging.info(root + "/" + file)
                #print(root)
                #image = cv2.imread(root + "/" + file)
                #gray = get_grayscale(image)
                thresh = thresholding(gray)
                x,y,w,h = 1650, 2063, 2190, 97
                ROI = thresh[y:y+h,x:x+w]
                #print(i, '\n')
                ocrtime = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6').split()
                # print(file + ":     " , ocrtime)
                i += 1
                #print(i)



                
                try:
                    date1 = ocrtime[0] + " " + ocrtime[1]
                    print(i , date1)
                    start = re.search(r'\d', date1)
                    date1 = date1[start.start():]
                    #print(i , file + ":     " , date1)
                    date1 = datetime.strptime(date1, '%m/%d/%Y %H:%M%p')
                    #print(str(date1))
                    photoDir = root + "/" + file
                    timeDict.setdefault(str(date1), []).append(photoDir)
                    print(str(timeDict[str(date1)]))
                    #print(i + ", File:    " + photoDir + "            Time:    " + str(date1)[:-3])
                    
                except:
                    logging.warning("File:    " + photoDir + "            Time:    " + str(date1))
                    continue
    return timeDict


def single_ocr(dir_path):
    image = cv2.imread(dir_path)
    gray = get_grayscale(image)
    thresh = thresholding(gray)
    x,y,w,h = 1650, 2063, 2190, 97
    ROI = thresh[y:y+h,x:x+w]
    #print(i, '\n')
    ocrtime = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6').split()
    print(ocrtime)
    
    
    
    date1 = ocrtime[0] + " " + ocrtime[1]
    print(date1)
    start = re.search(r'\d', date1)
    date1 = date1[start.start():]
    print(date1)
    date1 = datetime.strptime(date1, '%m/%d/%Y %H:%M%p')
    print(date1)
    print("Time:    " + str(date1)[:-3])
    




if __name__ == "__main__":
    timeDict = ocrDateTime("/home/compbio/Photos")
    with open('data.json', 'w') as fp:
    	json.dump(timeDict, fp)
    #single_ocr("/home/compbio/Photos/2020 January/AST1/IMG_0004.JPG")
    #f = open("data.json")
    #json_obj = json.load(f)
    #print(len(json_obj))

