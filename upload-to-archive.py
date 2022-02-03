import os
from importantText import convertDate, convertTime
import argparse
import datetime
import time
import subprocess

import pytesseract
import cv2

from ratelimiter import RateLimiter


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True,
                help="folder path in UWINUpload to archive")
args = vars(ap.parse_args())


# date modified
currTime = str(datetime.datetime.now())
print(currTime)
currTime = currTime.split(".")
currTime = currTime[0].split(" ")
currDate = currTime[0]
currTime = currTime[1]

date = convertDate(currDate)
timeStr = convertTime(currTime)
# make timestamp readable

# print(date)
# print(timeStr)


# move file and change name
currentPath = os.path.abspath(os.path.dirname(__file__))
RCLONE_PATH = os.path.join(currentPath, "rclone")
# mountpointPath = os.path.join(currentPath, "mountpoint")

# add as parse arg
sourcePath = "gdrive:UWINUpload/" + args["folder"]
targetPath = "gdrive:UWINArchive/" + args["folder"]

os.chdir(RCLONE_PATH)

cmd = "rclone lsf -R --files-only gdrive:UWINUpload"
proc = subprocess.Popen(["rclone", "lsf", "-R", "--files-only",
                        "gdrive:UWINUpload"], stdout=subprocess.PIPE)
(out, err) = proc.communicate()
out = out.decode("utf-8").split("\n")


rate_limiter = RateLimiter(5, 1)
for file in out:
  with rate_limiter:
    if file != "":
      dir_extList = file.split(".")
      filename = dir_extList[0] + "_ArchivedAt-" + \
          timeStr + date + "." + dir_extList[1]
      # print("rclone copyto gdrive:UWINUpload/" + file + " gdrive:UWINArchive/" + filename)

      src = "gdrive:UWINUpload/" + file
      dst = "gdrive:UWINArchive/" + filename
      subprocess.Popen(["rclone", "copyto", "--no-check-dest",
                       "--retries-sleep=2s", src, dst])

      # no need to rename archived files. use rclone purge command
      # renamed = src.split(".")
      # renamed = renamed[0] + "ARCHIVED_OK2DEL." +renamed[1]
      # subprocess.Popen(["rclone", "moveto", src, renamed])

# subprocess.Popen(["rclone", "purge", ])
