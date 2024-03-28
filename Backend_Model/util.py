import cv2
import easyocr
import numpy as np

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'@': '0', 'O': '0', 'D': '9'}
dict_int_to_char = {'1': 'I'}


def license_complies_format(text):
    if len(text) == 6 and text[:2].isalpha() and text[2:].isdigit():
        result = True
    elif len(text) == 7 and text[:3].isalpha() and text[3:].isdigit():
        result = True
    elif len(text) == 6 and text[:2].isdigit() and text[2:].isdigit():
        result = True
    else:
        result = False

    print(f"Format check result for '{text}': {result}")  # print the format check result
    return result


def format_license(text):
    # Strip double quotes from the text
    text = text.replace('"', '')
    text = text.replace('?', '')

    # Convert characters using the mapping dictionary only on the last 4 characters
    last_four = text[-4:]
    for char, replacement in dict_char_to_int.items():
        last_four = last_four.replace(char, replacement)
    text = text[:-4] + last_four

    # Convert integers using the mapping dictionary only on the first 2 or 3 characters
    first_two_or_three = text[:3] if len(text) > 6 else text[:2]
    for char, replacement in dict_int_to_char.items():
        first_two_or_three = first_two_or_three.replace(char, replacement)
    text = first_two_or_three + text[len(first_two_or_three):]

    return text


def read_license_plate(license_plate_crop):
    # Use EasyOCR to detect text
    detections = reader.readtext(license_plate_crop, detail=0)

    # Sort detections by x-coordinate
    detections.sort(key=lambda bbox_text_conf: bbox_text_conf[0][0][0])

    # Calculate average height of characters
    total_height = 0
    for text in detections:
        # Convert the text to a binary image
        text_img = np.array([[int(char == ' ') for char in line] for line in text], dtype=np.uint8)
        text_img = cv2.bitwise_not(text_img)  # invert the image

        # Calculate the height of the text by counting the white pixels in the vertical direction
        height = np.sum(text_img) // 255
        total_height += height

    if len(detections) > 0:
        average_height = total_height // len(detections)
    else:
        average_height = 0

    # Filter out the texts with smaller heights
    filtered_texts = []
    for text in detections:
        # Convert the text to a binary image
        text_img = np.array([[int(char == ' ') for char in line] for line in text], dtype=np.uint8)
        text_img = cv2.bitwise_not(text_img)  # invert the image

        # Calculate the height of the text by counting the white pixels in the vertical direction
        height = np.sum(text_img) // 255

        # If the height is larger than a certain fraction of the average height, keep the text
        if height > average_height / 1.5:  # Adjust the threshold according to your needs
            filtered_texts.append(text)

    print(f"Filtered texts: {filtered_texts}")

    # Concatenate all filtered text parts
    full_text = ''.join([text.upper().replace(' ', '') for text in filtered_texts])
    print(f"Detected text: {full_text}")  # print the detected text

    formatted_text = format_license(full_text)
    print(f"Formatted text: {formatted_text}")  # print the formatted text

    if license_complies_format(formatted_text):
        return formatted_text, None

    return None, None
