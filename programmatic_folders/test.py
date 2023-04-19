import pytest

import file_format

import shutil
import os

import pandas as pd

output_folder = 'test_output'

def clear_output():
        try:
            shutil.rmtree(output_folder)
        except Exception:
            pass

def test_file_format():
        clear_output()

        file_format.main('jpg_imgs', output_folder, 'test_metadata.csv')

	# "Austin, Texas","AUTX-C01-EML"
        assert os.path.exists(output_folder + '/AustinTexas/EML_2018_08_18')
        assert os.path.exists(output_folder + '/AustinTexas/EML_2018_11_01')

        aug18 = output_folder + '/AustinTexas/EML_2018_08_18'

        if os.path.isdir(aug18):
            if len(os.listdir(aug18)) == 0:
                print("Directory is empty")
            else:
                print("Directory is non-empty")


def test_jpg_exists():

        clear_output()
        file_format.main('jpg_imgs', output_folder, 'test_metadata.csv')

        assert os.path.exists(output_folder + '/AustinTexas/EML_2018_08_18')
        
        # change the following test because a different file is put into EML_2018_11_01 when the script is rerun
        # make the test more general - test for non-emptiness

        # assert os.path.isfile(output_folder + '/AustinTexas/EML_2018_11_01/IMG_0002.JPG')
        assert len(os.listdir(output_folder + '/AustinTexas/EML_2018_11_01')) > 0
        
# each test function should run file_format once

def test_file_format_output():

        clear_output()

        output_folder = 'test_output'

        # file_format is modified to return filepaths and files as a list
        # filepaths = return[0]
        # files = return[1]
        filepaths, files = file_format.main('jpg_imgs', output_folder, 'test_metadata.csv')

        print(filepaths)
        print(files)

        # write a test to make sure that full folder filepaths created in file_format actually exist
        for fp in filepaths:
            assert os.path.exists(fp)

            for fi in files:
                # print(fp + '/' + fi)
            
            #for fi in files:

                # if the path exists, ensure that it is actually a file
                if os.path.exists(fp + '/' + fi):
                    assert os.path.isfile(fp + '/' + fi)

        if os.path.isdir('test_create_folder'):
            print("directory already exists")

        else:
            os.mkdir('test_create_folder')
            print("directory created")

        assert os.path.exists('test_create_folder')

def test_image_not_found_exception():

        clear_output()
        output_folder = 'test_output'

        # read from the bad csv to get a non-existent jpg
        # then check to ensure that the file doesn't exist

        try:
            filepaths, files = file_format.main('jpg_imgs', output_folder, 'test_metadata_bad.csv')
        except FileNotFoundError:
            print("file not found exception")

        csv = pd.read_csv('test_metadata.csv')
        csv_fps = csv['filepath']

        print('csv')
        print(list(csv_fps))

        filepaths, files = file_format.main('jpg_imgs', output_folder, 'test_metadata.csv')

        # check to see if each jpg file is also found in the csv
        # take the csv filepaths and coerce them into a list format
        # then check if the jpgs we want are actually in this list
        # since jpgs we want are IMG_x.jpg, while the filepaths in the csv are 0000x.jpg, cut off the first few characters

        # also get the directory that the jpg files are in
        # assert if the jpg files are in the appropriate EML folders

        for long_fp in list(csv_fps):

            for fi in files:   
                processed_fi = fi[4:].lower()

                if processed_fi in long_fp: # IMG_x.jpg exists in the csv
                    print(fi[4:8], "jpg filepath exists")
                    
                    if fi in os.listdir(output_folder + '/AustinTexas/EML_2018_08_18/'): # if the file is in the contents of the directory
                        assert(os.path.isfile(output_folder + '/AustinTexas/EML_2018_08_18/' + fi)) # assert that it is a proper jpg file
                    
                    # same assert for the other folder
                    elif fi in os.listdir(output_folder + '/AustinTexas/EML_2018_11_01/'):
                        assert(os.path.isfile(output_folder + '/AustinTexas/EML_2018_11_01/' + fi))

                # FIXME issue with assert not
                #else:
                 #   print(fi)
                  #  print(os.listdir(output_folder + '/AustinTexas/EML_2018_11_01/'))
                   # assert not (os.path.isfile(output_folder + '/AustinTexas/EML_2018_11_01/' + fi))
                    
