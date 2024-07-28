import os
import cv2
import numpy as np
import easyocr
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from passporteye import read_mrz
import argparse
from utils.utils import parse_date, clean, get_gender, print_data, process_mrz_type1, process_mrz_type2, process_mrz_type3

# Load OCR engine (easyOCR)
reader = easyocr.Reader(lang_list=['en'], gpu=True)  # Enable GPU if available
def ocr(img_name):
    """
    Extracts and processes personal information from the passport image.

    Parameters:
    - img_name (str): Path to the passport image.

    Returns:
    - dict: Extracted personal information.
    """
    user_info = {}
    temp_image_path = 'tmp.png'

    # Extract MRZ from image
    mrz = read_mrz(img_name, save_roi=True)
    if not mrz:
        print(f'Machine cannot read image {img_name}.')
        return user_info

    # Save and process MRZ image
    mpimg.imsave(temp_image_path, mrz.aux['roi'], cmap='gray')
    img = cv2.imread(temp_image_path)
    img = cv2.resize(img, None, fx=2, fy=2)  # Increase resolution for better OCR

    # Define allowed characters for OCR
    allowlist = st.ascii_letters + st.digits + '< '
    lines = reader.readtext(img, paragraph=False, detail=0, allowlist=allowlist)

    # Process MRZ lines based on their structure
    if len(lines) == 3 and all(len(line) >= 30 for line in lines):
        user_info = process_mrz_type1(lines)
    elif len(lines) == 2:
        if all(len(line) >= 36 for line in lines):
            user_info = process_mrz_type2(lines)
        elif all(len(line) >= 44 for line in lines):
            user_info = process_mrz_type3(lines)
    else:
        print("Unrecognized MRZ format")

    # Clean up temporary image file
    os.remove(temp_image_path)
    return user_info
if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="OCR Passport Reader")
    
    # Add argument for image path
    parser.add_argument('--image_path', type=str, required=True, help='Path to the passport image')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the main function with the image path
    ocr(args.image_path)
