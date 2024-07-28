import os
import string as st
import cv2
from passporteye import read_mrz
import easyocr
from dateutil import parser
import datetime

def parse_date(string, fix_year=False):
    """
    Parses a date string and optionally fixes the year if it's in the future.

    Parameters:
    - string (str): The date string to parse.
    - fix_year (bool): If True, adjusts the year if it is greater than the current year.

    Returns:
    - str: The parsed date in 'DD/MM/YYYY' format.
    """
    try:
        date = parser.parse(string, yearfirst=True).date()
        if fix_year and date.year > datetime.datetime.now().year:
            date = date.replace(year=date.year - 100)
        return date.strftime('%d/%m/%Y')
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

def clean(string):
    """
    Cleans a string by removing all non-alphanumeric characters and converting to uppercase.

    Parameters:
    - string (str): The string to clean.

    Returns:
    - str: The cleaned string.
    """
    return ''.join([i for i in string if i.isalnum()]).upper()

def get_gender(code):
    """
    Returns the normalized gender code from a given input.

    Parameters:
    - code (str): The gender code to interpret. Expected to be 'M', 'F', or other values.

    Returns:
    - str: 'M' for male, 'F' for female, or 'Unknown' if the code is not recognized or provided.
    """
    normalized_code = code.upper()
    return normalized_code if normalized_code in ['M', 'F'] else ''

def print_data(data):
    """
    Prints the key-value pairs from a dictionary in a formatted manner.

    Parameters:
    - data (dict): A dictionary containing the data to be printed.
    """
    for key, value in data.items():
        formatted_key = key.replace('_', ' ').capitalize()
        print(f'{formatted_key}\t:\t{value}')

def process_mrz_type1(lines):
    """
    Processes MRZ lines of type 1 to extract user information.

    Parameters:
    - lines (list): List of MRZ lines extracted from the image.

    Returns:
    - dict: Extracted user information.
    """
    user_info = {}

    # Process Row 1
    user_info['document_type'] = clean(lines[0][0:1])
    user_info['document_type'] += clean(lines[0][1:2])  # Type character (e.g., I, A, or C)
    user_info['issuing_country'] = clean(lines[0][2:5])  # Issuing Country (ISO 3166-1 code)
    user_info['document_number'] = clean(lines[0][5:14])  # Document Number
    # Skip Check Digit over Document Number (position 15) and Optional (16-30)

    # Process Row 2
    user_info['date_of_birth'] = parse_date(lines[1][0:6], fix_year=True)  # Date of Birth (YYMMDD)
    user_info['gender'] = get_gender(lines[1][7:8])  # Sex (M, F, or <)
    user_info['expiration_date'] = parse_date(lines[1][8:14])  # Expiration Date (YYMMDD)
    user_info['nationality'] = clean(lines[1][15:18])  # Nationality
    # Skip Check Digit over Expiration Date (position 15) and Optional1 (19-29)

    # Process Row 3
    names = lines[2].replace('<', ' ').strip().split()
    user_info['surname'] = names[0] if names else ''
    user_info['name'] = ' '.join(names[1:]) if len(names) > 1 else ''

    return user_info

def process_mrz_type2(lines):
    """
    Processes MRZ lines of type 2 to extract user information.

    Parameters:
    - lines (list): List of MRZ lines extracted from the image.

    Returns:
    - dict: Extracted user information.
    """
    user_info = {}
    user_info['document_type'] = clean(lines[0][0:2])
    user_info['issuing_country'] = clean(lines[0][2:5])
    names = lines[0][5:].replace('<', ' ').split()
    user_info['surname'] = names[0] if names else ''
    user_info['name'] = ' '.join(names[1:]) if len(names) > 1 else ''
    user_info['document_number'] = clean(lines[1][0:9])
    user_info['nationality'] = clean(lines[1][10:13])
    user_info['date_of_birth'] = parse_date(lines[1][13:19], fix_year=True)
    user_info['gender'] = get_gender(lines[1][20])
    user_info['expiration_date'] = parse_date(lines[1][21:27])
    user_info['personal_number'] = clean(lines[1][28:35])
    return user_info

def process_mrz_type3(lines):
    """
    Processes MRZ lines of type 3 to extract user information.

    Parameters:
    - lines (list): List of MRZ lines extracted from the image.

    Returns:
    - dict: Extracted user information.
    """
    user_info = {}
    user_info['passport_type'] = clean(lines[0][0:2])
    user_info['issuing_country'] = clean(lines[0][2:5])
    names = lines[0][5:44].replace('<', ' ').split()
    user_info['surname'] = names[0] if names else ''
    user_info['name'] = ' '.join(names[1:]) if len(names) > 1 else ''
    user_info['passport_number'] = clean(lines[1][0:9])
    user_info['nationality'] = clean(lines[1][10:13])
    user_info['date_of_birth'] = parse_date(lines[1][13:19], fix_year=True)
    user_info['gender'] = get_gender(lines[1][20])
    user_info['expiration_date'] = parse_date(lines[1][21:27])
    user_info['personal_number'] = clean(lines[1][28:42])
    return user_info
