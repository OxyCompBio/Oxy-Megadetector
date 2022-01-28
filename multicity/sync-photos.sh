echo "1. Downloading UWIN_Test_Dataset..."
time rclone sync -P gdrive:"UWIN_Test_Dataset" /home/compbio/GDrive/UWIN_Test_Dataset

echo "2. Uploading UWIN_Test_Dataset..."
time rclone sync -P /home/compbio/GDrive/UWIN_Test_Dataset gdrive:"UWIN_Test_Dataset"
