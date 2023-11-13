import pytesseract

# Download the Tamil language model for Tesseract
pytesseract.download_trained_data('tam')

# Configure Tesseract to use the Tamil language model
config = '--lang=tam'

path = r'aadhar-front.jpg'

# Extract text from the image
text = pytesseract.image_to_string(path, config)

# Print the extracted text
print(text)