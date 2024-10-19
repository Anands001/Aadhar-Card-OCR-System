import io
import json
import os
import time

import cv2
import ftfy
import pytesseract
from flask import Flask, request, jsonify
from flask_cors import CORS
import Dbmongo.connect_database as db

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, origins=["https://aadhar-ocr-frontend.onrender.com"], supports_credentials=True)

@app.route('/upload', methods=['POST'])
def main():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if needed
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        # Start time for OCR extraction
        start_time = time.time()

        # Read and process the image
        img = cv2.imread(path)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        var = cv2.Laplacian(img, cv2.CV_64F).var()

        if var < 5:
            return jsonify({'error': 'Image is too blurry'}), 400

        # Perform OCR using Tesseract
        text = pytesseract.image_to_string(img, lang='eng')

        # Fix text and encoding
        text = ftfy.fix_text(text)
        text = ftfy.fix_encoding(text)

        # Prepare the output data
        data = {
            'extracted_text': text,
            'extraction_time': time.time() - start_time
        }

        # Save the extracted data to JSON
        with io.open('info.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

        # Optionally, store the extracted data in MongoDB
        db.store_aadhar_info(data)

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
