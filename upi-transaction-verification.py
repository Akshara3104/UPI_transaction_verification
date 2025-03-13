from flask import Flask, render_template, request, jsonify
import os
import cv2
import pytesseract
import pandas as pd
from datetime import datetime
import re
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create data directory for Excel files
DATA_FOLDER = 'data'
os.makedirs(DATA_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_excel_filename():
    """Generate Excel filename based on current date"""
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(DATA_FOLDER, f'transactions_{today}.xlsx')

def extract_text_from_image(image_path):
    """Extract text from image using Tesseract OCR"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def parse_transaction_details(text):
    """Parse transaction details from OCR text"""
    # Initialize result dictionary with default values
    result = {
        'transaction_id': None,
        'transaction_amount': None,
        'transaction_time': None,
        'transaction_date': None,
        'upi_id': None,
        'is_successful': False
    }
    
    # Extract Transaction ID
    txn_id_match = re.search(r'(?:UTR|Reference|ID|UPI Ref|Transaction ID)[:\s]+([A-Z0-9]+)', text, re.IGNORECASE)
    if txn_id_match:
        result['transaction_id'] = txn_id_match.group(1)
    
    # Extract Amount
    amount_match = re.search(r'(?:Rs\.?|₹|Amount)[:\s]*([0-9,.]+)', text, re.IGNORECASE)
    if amount_match:
        result['transaction_amount'] = amount_match.group(1).replace(',', '')
    
    # Extract Time
    time_match = re.search(r'(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)', text, re.IGNORECASE)
    if time_match:
        result['transaction_time'] = time_match.group(1)
    
    # Extract Date
    date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
    if date_match:
        result['transaction_date'] = date_match.group(1)
    
    # Extract UPI ID
    upi_match = re.search(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+)', text)
    if upi_match:
        result['upi_id'] = upi_match.group(1)
    
    # Check if transaction was successful
    result['is_successful'] = 'success' in text.lower() or 'paid' in text.lower() or 'completed' in text.lower()
    
    return result

def save_to_excel(data):
    """Save transaction data to Excel file"""
    excel_path = get_excel_filename()
    
    # If file exists, read it first
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
    else:
        # Create new DataFrame with columns
        df = pd.DataFrame(columns=[
            'name', 'image_path', 'transaction_id', 'transaction_amount',
            'transaction_time', 'transaction_date', 'upi_id', 'is_successful'
        ])
    
    # Append new data
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    
    # Save to Excel
    df.to_excel(excel_path, index=False)
    return excel_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_proof():
    if 'receipt_image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['receipt_image']
    name = request.form.get('name', '')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract and parse text from image
        try:
            text = extract_text_from_image(file_path)
            transaction_details = parse_transaction_details(text)
            
            # Prepare data for Excel
            data = {
                'name': name,
                'image_path': file_path,
                **transaction_details
            }
            
            # Save to Excel
            excel_path = save_to_excel(data)
            
            return jsonify({
                'success': True,
                'message': 'Transaction details saved successfully',
                'transaction_details': transaction_details
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
