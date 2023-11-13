import pytesseract


# Path to the image
path = r'aadhar-front.jpg'


from PIL import Image
# If you don't have tesseract executable in your PATH, include the following:

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd="C:\\MyApps\\Tesseract-ocr\\tesseract.exe"

# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
# Simple image to string

# myconfig = r"--psm 3 --oem 3"

text = pytesseract.image_to_string(Image.open(path))
print(text)
