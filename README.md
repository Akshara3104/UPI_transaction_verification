# UPI_transaction_verification
A web application that allows users to submit proof of UPI payments using screenshots from apps like GPay, PayTM, PhonePe, etc. The system uses Optical Character Recognition (OCR) to extract transaction details and stores them in daily Excel sheets.

## Features

- User-friendly interface for submitting payment proofs
- OCR-based extraction of transaction details from screenshots
- Automatic detection of transaction success/failure
- Daily Excel sheet generation for transaction records
- Support for various UPI payment apps (GPay, PayTM, PhonePe, etc.)

## Prerequisites

- Python 3.8 or higher
- Tesseract OCR engine installed on your system

### Installing Tesseract OCR

#### Windows
1. Download the installer from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install and add the installation directory to your system PATH

#### macOS
```
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```
sudo apt update
sudo apt install tesseract-ocr
```

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/upi-transaction-verification.git
cd upi-transaction-verification
```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Create necessary directories:
```
mkdir -p uploads data
```

## Usage

1. Start the application:
```
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

3. Enter your name and upload a screenshot of your UPI payment proof
4. The system will process the image, extract details, and store them in a daily Excel sheet
5. Excel files will be stored in the `data` folder with filenames like `transactions_2025-03-13.xlsx`

## How It Works

1. **Frontend Interface**: Simple form for name input and payment screenshot upload
2. **OCR Processing**: Uses Tesseract OCR to extract text from payment screenshots
3. **Information Extraction**: Pattern recognition to identify transaction ID, amount, time, date, UPI ID
4. **Success Detection**: Identifies if the transaction was successful based on keywords
5. **Excel Storage**: Creates a new Excel sheet for each day with all transactions

## Excel Sheet Structure

Each Excel sheet contains the following columns:
- Name (submitted by user)
- Image Path (location of uploaded screenshot)
- Transaction ID
- Transaction Amount
- Transaction Time
- Transaction Date
- UPI ID
- Is Successful (True/False)

## Customization

You can customize the OCR text parsing by modifying the regex patterns in the `parse_transaction_details` function in `app.py`. The current implementation includes common patterns found in popular UPI apps, but you may need to adjust them for specific app formats.

## Limitations

- OCR accuracy depends on the quality of the uploaded screenshot
- Some UPI payment apps may have different formats that require additional patterns
- Only image files (.png, .jpg, .jpeg) are supported

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/)
- [pandas](https://pandas.pydata.org/)
