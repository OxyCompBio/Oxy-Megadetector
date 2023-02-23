# Oxy-Megadetector

Tech we use:

- Python (I like Python!)
- TensorFlow
- Google Colab Notebooks
- Bash
- Google Drive API  

### Reading

- https://github.com/microsoft/CameraTraps/blob/master/megadetector.md
- https://beerys.github.io/CaltechCameraTraps/
- https://beerys.github.io (see links at bottom)

## Using The Megadetector Pipeline ####

### Preparing the pipeline

Create shared google drive folders:
  - `Photo_Uploads` - A place to upload photos to
  - `Photo_MegaOutput` - A place to save megadetector results to
  - `Photo_Archive` - A place to archive your photos when done

Set up Cluster Account - need dedicated GPU

Install/set up `rclone` on Cluster
  - run `rclone config`
  - see rclone.org/drive/

Set up Conda Environment
  - Install Conda or Miniconda
  - Access our conda environment: https://github.com/OxyCompBio/Oxy-Megadetector
  - Create an environment from our environment file conda.yml
  - `conda env create -f conda.yml`
  - now you can run `conda activate tensorflow` to activate our environment

### Running the pipeline

Upload photos to shared google drive folder: "Photo_Uploads"
  - Naming convention: `OXY1_2021_10_01 *site name and check date of photos`

If off campus, log into vpn (Forticlient)
  - Use Oxy Login/Password
  - (if you don't have an account, David Dellinger can set up)

Log into cluster
  - username: `compbio`
  - enter password

cd into Oxy-Megadetector dir

Sync photos from Google Drive to Cluster
Run `./sync-photos.sh`, a script that:
  - syncs photos down from google drive/Photo_Uploads to cluster
  - syncs megadetector output down from google drive/Photo_MegaOutput to cluster
  - syncs megadetector output up from cluster to google drive/Photo_MegaOutput

Log into gpu
  - `ssh gpu01`
  - enter password

Run Megadetector
Run `./run-megadetector.sh`, a script that:
  - cds into Oxy-Megadetector dir
  - sets up environment
  - runs `conda activate tensorflow`
  - runs megadetector on all images in `Photo_Upload` and saves detection JSON and images above the detection threshhold to `Photo_MegaOutput`

Re-sync files between cluster and Google Drive
  - run `sync-photos.sh`
	
Notes:

These scripts are idempotent, meaning they are safe to run repeatedly without recreating files. Will skip if file already completed.

### Video

- Build Your First Neural Network: From Start to Finish (Colab Notebook): https://www.youtube.com/watch?v=5UTwLoaM_M8
- AI 101: https://www.youtube.com/watch?v=ospOM7qYx2Y&list=PL_-uv7N8XX4OitDyERnkCp9O80_jpvIx6

### Interactive Notebook Demo of Megedatector

- https://colab.research.google.com/github/microsoft/CameraTraps/blob/master/detection/megadetector_colab.ipynb#scrollTo=HkUMhkjB0zL_

## Issues

Check out the [issues](https://github.com/maxogden/Oxy-Megadetector/issues) page to see some stuff you can work on
