# must be run on a GPU environment (ssh01)
cd ~/Oxy-Megadetector

conda activate tensorflow

echo "1. Running MegaDetector..."
# generates a JSON file (raw megadetector output file) and places it in MegaOutput
python /home/compbio/Oxy-Megadetector/run_md_on_uploads.py /home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload /home/compbio/GDrive/UWIN_Test_Dataset/Photo_MegaOutput

echo "2. Copying Animal Photos..."
# processes every unprocessed JSON file in MegaOutput
# copies matches above a threshold from source directory into MegaOutput
# also copies first and last photo from source directory
#python copy-detection-photos.py ./Photo_Upload ./MegaOutput 0.7
python /home/compbio/Oxy-Megadetector/get_animal_photos.py /home/compbio/GDrive/UWIN_Test_Dataset/Photo_MegaOutput /home/compbio/GDrive/UWIN_Test_Dataset/Photo_MegaOutput /home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload

