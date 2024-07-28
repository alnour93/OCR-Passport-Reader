import os
import string as st
import cv2
from passporteye import read_mrz
import easyocr
from dateutil import parser
import datetime

# Initialize the OCR engine
reader = easyocr.Reader(lang_list=['en'], gpu=True)

def format_date_string(string, fix_year=False):
    """
    Parses a date string and optionally fixes the year if it's in the future.
    """
    try:
        date = parser.parse(string, yearfirst=True).date()
        if fix_year and date.year > datetime.datetime.now().year:
            date = date.replace(year=date.year - 100)
        return date.strftime('%d/%m/%Y')
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

def sanitize_string(string):
    """
    Cleans a string by removing non-alphanumeric characters and converting to uppercase.
    """
    return ''.join([i for i in string if i.isalnum()]).upper()

def normalize_gender_code(code):
    """
    Returns the normalized gender code from a given input.
    """
    normalized_code = code.upper()
    return normalized_code if normalized_code in ['M', 'F'] else 'Unknown'

def display_formatted_data(data):
    """
    Prints the key-value pairs from a dictionary in a formatted manner.
    """
    for key, value in data.items():
        formatted_key = key.replace('_', ' ').capitalize()
        print(f'{formatted_key}\t:\t{value}')

def extract_mrz_from_image(img_name):
    """
    Extracts MRZ lines from an image and returns them.
    """
    user_info = {}
    temp_image_path = 'tmp.png'

    # Extract MRZ from image
    mrz = read_mrz(img_name, save_roi=True)
    if not mrz:
        print(f'Machine cannot read image {img_name}.')
        return user_info

    # Save and process MRZ image
    cv2.imwrite(temp_image_path, mrz.aux['roi'])
    img = cv2.imread(temp_image_path)
    img = cv2.resize(img, None, fx=2, fy=2)  # Increase resolution for better OCR

    # Define allowed characters for OCR
    allowlist = st.ascii_letters + st.digits + '< '
    lines = reader.readtext(img, paragraph=False, detail=0, allowlist=allowlist)

    # Clean up temporary image file
    os.remove(temp_image_path)
    return lines

def extract_mrz_type1_data(lines):
    """
    Processes MRZ lines of type 1 to extract user information.
    """
    user_info = {}
    # Process Row 1
    user_info['document_type'] = sanitize_string(lines[0][0:2])
    user_info['issuing_country'] = sanitize_string(lines[0][2:5])
    user_info['document_number'] = sanitize_string(lines[0][5:14])
    # Process Row 2
    user_info['date_of_birth'] = format_date_string(lines[1][0:6], fix_year=True)
    user_info['gender'] = normalize_gender_code(lines[1][7:8])
    user_info['expiration_date'] = format_date_string(lines[1][8:14])
    user_info['nationality'] = sanitize_string(lines[1][15:18])
    # Process Row 3
    names = lines[2].replace('<', ' ').strip().split()
    user_info['surname'] = names[0] if names else ''
    user_info['name'] = ' '.join(names[1:]) if len(names) > 1 else ''
    return user_info

def extract_mrz_type2_data(lines):
    """
    Processes MRZ lines of type 2 to extract user information.
    """
    user_info = {}
    user_info['document_type'] = sanitize_string(lines[0][0:2])
    user_info['issuing_country'] = sanitize_string(lines[0][2:5])
    names = lines[0][5:].replace('<', ' ').split()
    user_info['surname'] = names[0] if names else ''
    user_info['name'] = ' '.join(names[1:]) if len(names) > 1 else ''
    user_info['document_number'] = sanitize_string(lines[1][0:9])
    user_info['nationality'] = sanitize_string(lines[1][10:13])
    user_info['date_of_birth'] = format_date_string(lines[1][13:19], fix_year=True)
    user_info['gender'] = normalize_gender_code(lines[1][20])
    user_info['expiration_date'] = format_date_string(lines[1][21:27])
    user_info['personal_number'] = sanitize_string(lines[1][28:35])
    return user_info

def extract_mrz_type3_data(lines):
    """
    Processes MRZ lines of type 3 to extract user information.
    """
    user_info = {}
    user_info['passport_type'] = sanitize_string(lines[0][0:2])
    user_info['issuing_country'] = sanitize_string(lines[0][2:5])
    names = lines[0][5:44].replace('<', ' ').split()
    user_info['surname'] = names[0] if names else ''
    user_info['name'] = ' '.join(names[1:]) if len(names) > 1 else ''
    user_info['passport_number'] = sanitize_string(lines[1][0:9])
    user_info['nationality'] = sanitize_string(lines[1][10:13])
    user_info['date_of_birth'] = format_date_string(lines[1][13:19], fix_year=True)
    user_info['gender'] = normalize_gender_code(lines[1][20])
    user_info['expiration_date'] = format_date_string(lines[1][21:27])
    user_info['personal_number'] = sanitize_string(lines[1][28:42])
    return user_info
