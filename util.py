import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
# For Sri Lankan license plates, we don't need any character conversion
dict_char_to_int = {'@': '0', 'O': '0', 'D': '9'}

dict_int_to_char = {'1': 'I'}


def license_complies_format(text):

    if len(text) == 6 and text[:2].isalpha() and text[2:].isdigit():
        result = True
    elif len(text) == 7 and text[:3].isalpha() and text[3:].isdigit():
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

    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')
        print(f"Detected text: {text}")  # print the detected text

        formatted_text = format_license(text)
        print(f"Formatted text: {formatted_text}")  # print the formatted text

        if license_complies_format(formatted_text):
            return formatted_text, score

    return None, None


def get_car(license_plate, vehicle_track_ids):

    x1, y1, x2, y2, score, class_id = license_plate

    car_indx = -1  # Initialize car_indx before the loop

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1
