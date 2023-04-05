import pytest

import file_format

import shutil
import os

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
        assert os.path.isfile(output_folder + '/AustinTexas/EML_2018_08_18/IMG_0002.JPG')

def test_create_folder():

        output_folder = 'test_output'

        if os.path.isdir('test_create_folder'):
            print("directory already exists")
        else:
            os.mkdir('test_create_folder')
            print("directory created")

        assert os.path.exists('test_create_folder')
