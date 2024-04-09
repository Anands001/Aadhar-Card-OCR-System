# Aadhar Card OCR System

## Overview

This project is aimed at developing an OCR (Optical Character Recognition) system tailored for extracting essential information from Aadhar cards. The system processes Aadhar card images and extracts key details such as the individual's name, Aadhar number, date of birth, address, and other relevant information. It utilizes various technologies and libraries to achieve accurate and efficient OCR capabilities.

## Technologies Used

- **Python**: Programming language used for the backend implementation.
- **Tesseract OCR**: Open-source OCR engine for accurate text recognition.
- **EasyOCR**: Python library for OCR tasks, providing support for multiple languages and scripts.
- **Flask**: Lightweight Python web framework used for building the backend server.
- **Matplotlib**: Python plotting library for visualization purposes.
- **MongoDB**: NoSQL database used for storing extracted information (optional, based on project requirements).

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/aadhar-card-ocr.git
   cd aadhar-card-ocr
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python main_extract.py
   ```
4. Access the OCR system through the provided endpoints.

## Project Structure

- **`main_extract.py`**: Flask application entry point containing API endpoints for OCR functionality.
- **`ocr.py`**: Module for performing OCR tasks using Tesseract OCR and EasyOCR.
- **`uploads`**: Contains the images uploaded
- **`Reports/report1.py`**: Module for generating visualizations using Matplotlib.
- **`UI/ocr-ui/index.js`**: Module for react UI.
- **`requirements.txt`**: List of Python dependencies.
- **`README.md`**: Project documentation.
Sure, here's the section for running the UI:

## Running the UI

To run the UI, navigate to the `UI/ocr-ui` folder and execute the following command:

```bash
npm start
```

This will start the development server for the UI, allowing you to access it in your web browser.
```

## Contributing

Contributions are welcome! Feel free to submit pull requests or raise issues for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

---
# Data flow

![image](https://github.com/Anands001/OCR-Project/assets/110816114/0b329a29-674e-409e-b557-4387729be740)

# Project Demo Images
![image](https://github.com/Anands001/OCR-Project/assets/110816114/67a9e15f-2673-436c-9b08-8fcb8b67151c)

