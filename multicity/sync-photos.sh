echo "1. Syncing down UWIN_Test_Dataset..."
time rclone copy -P gdrive:"UWIN_Test_Dataset" /home/compbio/GDrive/UWIN_Test_Dataset

echo "2. Syncing up UWIN_Test_Dataset..."
time rclone copy -P /home/compbio/GDrive/UWIN_Test_Dataset gdrive:"UWIN_Test_Dataset"
