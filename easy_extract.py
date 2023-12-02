import cv2
import easyocr

# Replace 'en' with the language code of the text in your image
reader = easyocr.Reader(['en'])


def easy_read(path):
    # Replace 'your_image_path.jpg' with the path to your image file
    image_path = path

    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Extract text from the image
    results = reader.readtext(img)
    # print(results[1])
    # Print the extracted text
    result_string = ''
    for detection in results:
        print(detection[1])
        result_string = result_string + ' ' + ''.join(detection[1])
        # return detection[1]
        # print(detection[1])

    return result_string

    # Optionally, you can also print other information such as bounding boxes
    for detection in results:
        print(f"Text: {detection[1]}, Confidence: {detection[2]}, Bounding Box: {detection[0]}")
# easy_read(r'sample-aadhar4.jpg')
