import json
import pytesseract
import cv2
import numpy as np
import sys
import re
import os
from PIL import Image
import ftfy
import pan_read
'''module which we made to read the text of the document'''
import aadhaar_read
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
path = r'aadhar-front.jpg'

img = cv2.imread(path)
img = cv2.resize(img, None, fx=2, fy=2,interpolation=cv2.INTER_CUBIC)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
var = cv2.Laplacian(img, cv2.CV_64F).var()
if var < 5:
    print("Image is Too Blurry....")
    k= input('Press Enter to Exit.')
    exit(1)

filename = path
text = pytesseract.image_to_string(Image.open(filename), lang = 'eng+tam')
# Tamtext = pytesseract.image_to_string(Image.open(filename), lang = 'tam')
#
# print(Tamtext)

text_output = open('output.txt', 'w', encoding='utf-8')
text_output.write(text)
text_output.close()

file = open('output.txt', 'r', encoding='utf-8')
text = file.read()

text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)
print(text)
if "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():
    data = pan_read.pan_read_data(text)
elif "male" in text.lower():
    data = aadhaar_read.adhaar_read_data(text)
else:
    data = aadhaar_read.adhaar_read_data(text)

print("Data :",data)
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
with io.open('info.json', 'w', encoding='utf-8') as outfile:
    data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(data))

with open('info.json', encoding = 'utf-8') as data:
    data_loaded = json.load(data)
print(data_loaded)

if data_loaded['ID Type'] == 'PAN':
    print("\n---------- PAN Details ----------")
    print("\nPAN Number: ",data_loaded['PAN'])
    print("\nName: ",data_loaded['Name'])
    print("\nFather's Name: ",data_loaded['Father Name'])
    print("\nDate Of Birth: ",data_loaded['Date of Birth'])
    print("\n---------------------------------")
elif str.upper(data_loaded['ID Type']) == 'ADHAAR':
    print("\n---------- ADHAAR Details ----------")
    print("\nADHAAR Number: ",data_loaded['Adhaar Number'])
    print("\nName: ",data_loaded['Name'])
    print("\nDate Of Birth: ",data_loaded['Date of Birth'])
    print("\nSex: ",data_loaded['Sex'])
    print("\n------------------------------------")
k = input("\n\nPress Enter To EXIT")
exit(0)