import argparse
import subprocess
import os
from datetime import datetime, timedelta
import json

parser = argparse.ArgumentParser(description='Run visualize_detector_output.py on new upload folder photos')
parser.add_argument(
        'detector_output_folder', type=str,
        help='Path to json output folder of the detector')
parser.add_argument(
        'out_dir', type=str,
        help='Path to directory where the annotated images are saved.')
parser.add_argument(
        'photo_upload_base_path', type=str,
        help='photos upload base path')
parser.add_argument(
        '-c', '--confidence', type=float, default=0.8,
        help='Value between 0 and 1, indicating the confidence threshold '
             'above which to visualize bounding boxes')
args = parser.parse_args()
    
def  main(detector_output_path, output_dir, PHOTO_UPLOAD, confidence):
    for dirpath, dirnames, filenames in os.walk(detector_output_path):
        if dirpath is not detector_output_path:
            continue
        
        for i in filenames:
            detector_output_file = os.path.join(detector_output_path, i)
            output_dir_current = os.path.join(output_dir, i.split(".")[0])
            if datetime.now() - datetime.fromtimestamp(os.stat(detector_output_file).st_ctime) < timedelta(0, 0, 0, 0, 0, 1):
                subprocess.call(["python", "visualize_detector_output.py", detector_output_file, output_dir_current, confidence])

if __name__ == "__main__":
  main(args.detector_output_folder,args.output_dir, args.photo_upload_base_path, args.confidence)