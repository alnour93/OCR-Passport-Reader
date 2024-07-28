# OCR Passport Reader

## Overview

The **OCR Passport Reader** is a Python-based tool designed to extract and process personal information from passport images using Optical Character Recognition (OCR). This tool utilizes the EasyOCR library to interpret Machine Readable Zones (MRZ) in passports.

## Features

- Extracts information from different types of MRZ formats (Type 1, Type 2, Type 3).
- Processes MRZ data to retrieve personal information including name, document number, date of birth, gender, and expiration date.
- Supports OCR with EasyOCR, enabling GPU acceleration for faster processing.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/alnour93/OCR-Passport-Reader.git
    cd OCR-Passport-Reader
    ```

2. **Set Up the Environment**

    - Create and activate a virtual environment (optional but recommended):

      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows use: venv\Scripts\activate
      ```

    - Install the necessary dependencies:

      ```bash
      pip install -r requirements.txt
      ```

      Run the `setup.sh` script to install necessary system packages and Python dependencies:

      ```bash
      chmod +x setup.sh  # Make the script executable
      ./setup.sh
       ```
      The setup.sh script will:

      Update package lists and Install Tesseract OCR.

## Usage

1. **Prepare the Image**

    Ensure the passport image is in a supported format (e.g., PNG, JPG).

2. **Run the OCR Processing**

    Use the provided `main.py` script to process the passport image:

    ```bash
    python src/main.py --image_path path_to_your_image
    ```

    Replace `path_to_your_image` with the path to your passport image file.


## Example Output

```text
Document Type    : ID
Issuing Country   : USA
Document Number   : 123456789
Date of Birth     : 01/01/1980
Gender            : M
Expiration Date   : 01/01/2030
Nationality       : USA
Surname           : DOE
Name              : JOHN
 ```
## License

This project is licensed under the MIT License 

## Contact

For any questions or feedback, feel free to reach out to:

- **Name**: Alnour Abdalrahman
- **LinkedIn**: [linkedin.com/in/alnour-abdalrahman-3805b32a5](https://linkedin.com/in/alnour-abdalrahman-3805b32a5)
- **Email**: [alnourx93@gmail.com](mailto:alnourx93@gmail.com)
