import cv2
import easyocr
from matplotlib import pyplot as plt

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0', 'D': '9'}

dict_int_to_char = {'1': 'I'}


def license_complies_format(text):
    if len(text) == 6 and text[:2].isalpha() and text[2:].isdigit():
        result = True
    elif len(text) == 6 and text[:2].isalpha() and text[2:].isdigit():
        result = True
    elif len(text) == 7 and text[:3].isalpha() and text[3:].isdigit():
        result = True
    else:
        result = False

    print(f"Format check result for '{text}': {result}")
    return result


def format_license(text):
    # check for invalid characters
    if len(text) == 8 and text[:4].isalpha():
        text = text[1:]

    if len(text) == 9 and text[:4].isalpha():
        text = text[2:]

    # check for invalid numbers
    if sum(c.isdigit() for c in text[-5:]) > 4:
        text = text[:text.rfind(text[-5])] + text[text.rfind(text[-5]) + 1:]

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


def remove_province_code_by_crop(license_plate_crop):
    # Define the width of the crop
    crop_width = int(license_plate_crop.shape[1] * 0.17)

    # Crop the left side of the image
    license_plate_crop = license_plate_crop[:, crop_width:]

    return license_plate_crop


def read_license_plate(license_plate_crop):
    # Remove the province code from the license plate
    license_plate_crop = remove_province_code_by_crop(license_plate_crop)

    # Adjust EasyOCR parameters to prevent text box merging
    detections = reader.readtext(
        license_plate_crop,
        allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        min_size=20,  # Minimum size of the text
        slope_ths=0.0,  # Disable merging based on slope
        ycenter_ths=0.0,  # Disable merging based on y-center shift
        height_ths=0.1,  # Allow merging only if text heights are very similar
        width_ths=0.1,  # Allow merging only if text widths are very similar
        link_threshold=0.7,
        low_text=0.5,
        text_threshold=0.92,
    )

    # Sort detections based on the x-coordinate of the bounding box
    sorted_detections = sorted(detections, key=lambda detection: detection[0][0][0])

    detections_list = []

    combined_text = ''
    for detection in sorted_detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')

        combined_text += text
        detections_list.append(text)

    print(f"Detected Text: {detections_list}")

    # remove the petrol diesel detection
    if len(sorted_detections) == 3:
        del sorted_detections[1]

    print(f"Combined Text: {combined_text}")

    # Format the license plate text
    formatted_text = format_license(combined_text)
    print(f"Formatted text: {formatted_text}")

    if license_complies_format(formatted_text):
        return formatted_text

    return None, None