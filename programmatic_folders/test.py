import pytest

import file_format

import shutil
import os

def test_file_format():
	output_folder = 'test_output'
	

	try:
		shutil.rmtree(output_folder)
	except Exception:
		pass

	file_format.main('photos', output_folder, 'test_metadata.csv')

	# "Austin, Texas","AUTX-C01-EML"
	# 2018-08-18
	assert os.path.exists(output_folder + '/AustinTexas/EML_2018_08_18') 
