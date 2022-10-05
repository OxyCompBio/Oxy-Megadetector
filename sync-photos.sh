echo "0. Syncing down Photo_Archive"
time rclone sync -P gdrive:"AFC-UWIN-Photos/Photo_Archive" /home/compbio/GDrive/Photo_Archive

echo "1. Syncing down Photo_Upload..."
time rclone sync -P gdrive:"Photo_Upload" /home/compbio/GDrive/Photo_Upload

echo "2. Syncing up Photo_MegaOutput..."
time rclone copy -P /home/compbio/GDrive/Photo_MegaOutput gdrive:"Photo_MegaOutput"
