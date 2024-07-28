from utils.utils import extract_mrz_from_image, extract_mrz_type1_data, extract_mrz_type2_data, extract_mrz_type3_data, display_formatted_data

def process_image(img_path):
    """
    Processes an image to extract MRZ data and print the extracted information.
    """
    lines = extract_mrz_from_image(img_path)
    user_info = {}

    # Process MRZ lines based on their structure
    if len(lines) == 3 and all(len(line) >= 30 for line in lines):
        user_info = extract_mrz_type1_data(lines)
    elif len(lines) == 2:
        if all(len(line) >= 36 for line in lines):
            user_info = extract_mrz_type2_data(lines)
        elif all(len(line) >= 44 for line in lines):
            user_info = extract_mrz_type3_data(lines)
    else:
        print("Unrecognized MRZ format")

    # Print user information
    display_formatted_data(user_info)
