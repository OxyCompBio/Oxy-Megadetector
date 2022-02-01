import csv
import os
import json

BASE_PATH = "/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/first_upload"

def createCSV():
  counter = 0
  with open("first_upload.csv", "w+") as c:
    writer = csv.writer(c)
    with open("first_upload.json", "r") as detector_output:
        images = json.load(detector_output)

        for entry in images['images']:
          counter += 1
          # print(counter)
          photoDir = os.path.join(BASE_PATH, entry['file'])
          # print(photoDir)

          is_animal = False
          is_human = False
          is_car = False

          numAnimalDetections = 0
          numHumanDetections = 0
          maxDetectionConfHuman = 0
          jsonAnimalDetection = "" # if above 0.8
          maxDetectionConf = 0 # only animal detection confidence
          jsonOtherDetection = ""
          try:
            for detection in entry['detections']:
              if detection['category'] == '1':
                is_animal = True
                numAnimalDetections += 1
                jsonAnimalDetection += str(detection)
                if detection["conf"] > maxDetectionConf:
                  maxDetectionConf = detection["conf"]

              elif detection['category'] == '2' and detection["conf"] > 0.8:
                is_human = True
                jsonOtherDetection += str(detection)
                numHumanDetections += 1
                if detection["conf"] > maxDetectionConfHuman:
                  maxDetectionConfHuman = detection["conf"]
              elif detection['category'] == '3' and detection["conf"] > 0.8:
                is_car = True
                jsonOtherDetection += str(detection)
              # elif detection['category'] == '1':
              # 	jsonOtherDetection += str(detection)
              # 	if detection["conf"] > maxDetectionConf:
              # 		maxDetectionConf = detection["conf"]
              # print(detection)

            writer.writerow([photoDir, str(numAnimalDetections), str(jsonAnimalDetection), str(numHumanDetections), str(jsonOtherDetection), maxDetectionConf, maxDetectionConfHuman])
          except KeyError:
            print(KeyError)
            continue
        detector_output.close()
    c.close()
  

createCSV()
