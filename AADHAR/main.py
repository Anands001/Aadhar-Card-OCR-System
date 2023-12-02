from pathlib import Path

import cv2
import pytesseract

from aadhaar_details import get_values, get_address, send_to_json

if __name__ == "__main__":
    tesseract_path = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    aadhaar_front_img_path = Path(r"../sample-aadhar2.jpg")
    aadhaar_back_img_path = Path("../sample-aadhar2.jpg")
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    # Path to aadhaar front image
    img = cv2.imread(str(aadhaar_front_img_path))
    # Resize image (fx=0.5,fy=0.5 is half the original size)
    img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
    four_points = []
    # getting all values (except address) from Front Aadhaar Card Image
    regex_name,regex_gender,regex_dob,regex_mobile_number,regex_aadhaar_number = get_values(img)
    regex_name = " ".join(regex_name[:3])
    print(regex_name,regex_gender,regex_dob,regex_mobile_number,regex_aadhaar_number)
    # path to aadhaar back image (address side)
    img = cv2.imread(str(aadhaar_back_img_path))
    # resize aadhaar back image
    img = cv2.resize(img,(0,0),fx=0.75,fy=0.75)
    # getting address back
    regex_address = get_address(img)
    print(regex_address)
    send_to_json(regex_name,regex_gender,regex_dob,regex_mobile_number,regex_aadhaar_number,regex_address)

