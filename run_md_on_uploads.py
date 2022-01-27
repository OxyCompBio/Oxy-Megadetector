"""

run megadetector on gdrive upload folder

"""
# python run_md_on_uploads.py "C:\Users\baezh\OneDrive\Desktop\Oxy\Spring2021\Megadetector\Photo_Upload" 
# "C:\Users\baezh\OneDrive\Desktop\Oxy\Spring2021\Megadetector\MegaDetectorOutput"

import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='Run MegaDetector on new upload folder photos')
parser.add_argument('photo_folder', type=str, help='Path to upload folder')
parser.add_argument('md_output', type=str, help='Path to MegaDetector json output file destination')
args = parser.parse_args()


def main(PHOTO_UPLOAD, md_output_dest):
    for dirpath, dirnames, filenames in os.walk(PHOTO_UPLOAD):
        if dirpath is not PHOTO_UPLOAD:
            continue
        
        print(dirnames)
        for i in dirnames:
            newfolder = True
            for dirpath_, dirnames_, filenames_ in os.walk(md_output_dest):
                if (i + ".json") in filenames_:
                    newfolder = False
                    break
            if not newfolder:
                print("Old Folder!")
                continue
            print("New Folder!")
            detector_file = "/home/compbio/megadetector/md_v4.1.0.pb"
            output_file = os.path.join(md_output_dest, i + ".json")
            current_photo_folder = os.path.join(PHOTO_UPLOAD, i)
            subprocess.call(["python", "/home/compbio/megadetector/CameraTraps/detection/run_tf_detector_batch.py", detector_file, current_photo_folder, output_file, "--recursive", "--output_relative_filenames"])
        

if __name__ == "__main__":
    main(args.photo_folder, args.md_output)
