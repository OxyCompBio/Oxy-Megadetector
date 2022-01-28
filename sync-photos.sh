# sync old photos
#time rclone copy -P gdrive:"Wildlife Camera Team/UWIN Protocols & Datasheets/Photos" /home/compbio/Photos

echo "1. Syncing Photo_Upload..."
time rclone copy -P gdrive:"Photo_Upload" /home/compbio/GDrive/Photo_Upload

echo "2. Syncing Photo_MegaOutput..."
time rclone copy -P gdrive:"Photo_MegaOutput" /home/compbio/GDrive/Photo_MegaOutput

echo "3. Uploading Photo_MegaOutput..."
time rclone copy -P /home/compbio/GDrive/Photo_MegaOutput gdrive:"Photo_MegaOutput"
