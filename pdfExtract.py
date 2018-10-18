#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wand.image import Image as Img
import csv
import sys
try:
	from PIL import Image
except ImportError:
	import Image
import pytesseract
import argparse
import cv2
import os
import re

def cleanUpData(data):
	# Remove blank lines
	new_data = os.linesep.join([s for s in data.splitlines() if s])

	# Replace ligatures
	# Seems to be better results than blacklisting ligatures
	common_ligatures = ["ﬁ", "ﬂ"]
	lig_replacements = ["fi", "fl"]
	for index, lig in enumerate(common_ligatures):
		new_data = re.sub(lig, lig_replacements[index], new_data)
	return new_data

def fixPhoneNumber(original_number):
	# I know it's not efficient...
	fixed_phone_number = re.sub("\(", "", original_number)
	fixed_phone_number = re.sub("\)", "", fixed_phone_number)
	fixed_phone_number = re.sub(" ", "-", fixed_phone_number.strip())
	return fixed_phone_number

def outputToCSV(array_to_print):
	with open(csv_name, 'w', newline = '') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerows(array_to_print)

def convertPdfToImage(pdf):
	with Img(filename=pdf, resolution=300) as img:
	    img.compression_quality = 99
	    img.save(filename=jpg_name)
	    return len(img.sequence)

def processImage(filename):
	image = cv2.imread(filename)
	grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imwrite("current_temp_page.jpg", grey_image)

	# Enlarge the image
	small_image = Image.open("current_temp_page.jpg")
	base_width = 5100
	width_percentage = (base_width/float(small_image.size[0]))
	corresponding_height = int((float(small_image.size[1])*float(width_percentage)))
	enlarged_image = small_image.resize((base_width, corresponding_height), Image.ANTIALIAS)
	enlarged_image.save("current_temp_page.jpg")
	os.remove(filename)
	
def readPages(filename, data):
	#	text = pytesseract.image_to_string(Image.open(filename), config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()-+=[]\\':;,./?| --psm 6")
	text = pytesseract.image_to_string(Image.open(filename), config="--psm 6")
	os.remove(filename)
	data += text + '\n'
	return data

def extractData(data):
	print("Extracting Data")
	array_to_print = []
	# Proprietary regex deleted
	# Add yours here!
	print(array_to_print)
	outputToCSV(array_to_print)


pdf_name = sys.argv[1] + ".pdf"
csv_name = sys.argv[1] + ".csv"
jpg_name = sys.argv[1] + ".jpg"
grey_jpg_name = sys.argv[1] + "_grey.jpg"

print("STARTING")
number_of_pages = convertPdfToImage(pdf_name)
print(f"Total number of pages: {number_of_pages}")

data = ''
for i in range(0,number_of_pages):
	print(f"Processing page {i+1}")
	processImage(f"{sys.argv[1]}-{i}.jpg")
	data = readPages("current_temp_page.jpg", data)
print("FINISH")
new_data = cleanUpData(data)
print(new_data)
extractData(new_data)
