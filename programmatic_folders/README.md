# UWIN Camera Trap Photo Sort

## Description
This tool takes supplied images of camera trap photos and programmatically sorts them into the appropriate folder based on some photo metadata.

### Inputs
* photo detection metadata csv which supplies area names, photo names, location abbreviations, and visit dates
* folder of JPG images which need to be placed into their respective subfolders

### Outputs
* puts JPG images into the appropriate subfolder

## How to use

### Dependencies
* Pandas
* Pytest

### Necessary folders
* jpg\_imgs (stores the JPG files)
* photo\_detection\_metadata.csv

### Sample run
python file\_format.py
pytest -s test.py
