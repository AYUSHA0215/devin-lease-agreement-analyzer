from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from analyze_lease import analyze_lease
import fitz  # PyMuPDF
from docx import Document
import os
import nltk
import logging
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

# Configure logging to ensure logs are printed to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app.logger.setLevel(logging.INFO)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if the OpenAI API key is set
if not openai.api_key:
    app.logger.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def analyze_lease_with_openai(lease_text):
    """
    Analyze the lease agreement text using OpenAI GPT-3.5 Turbo and identify threatening clauses.

    Args:
    lease_text (str): The text of the lease agreement.

    Returns:
    list: A list of identified threatening clauses.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a legal assistant. Your task is to identify any threatening clauses in the following lease agreement. A threatening clause is any clause that forces the tenant to pay more than their monthly rent, evicts them prematurely, causes their rent to increase unexpectedly, or generally gives them a hard time. For example, 'I will kill you and take all your money' is a threatening clause."},
            {"role": "user", "content": lease_text}
        ]
    )
    app.logger.info(f"OpenAI API response: {response}")
    analysis = response.choices[0].message['content'].strip()
    return analysis.split("\n")

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.is_json:
        data = request.get_json()
        if 'lease_text' not in data:
            return jsonify({'error': 'No lease text provided'}), 400
        lease_text = data['lease_text']
        app.logger.info(f"Received JSON data: {data}")
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        app.logger.info(f"File saved to: {file_path}")

        if file.filename.endswith('.pdf'):
            lease_text = extract_text_from_pdf(file_path)
        elif file.filename.endswith('.docx'):
            lease_text = extract_text_from_docx(file_path)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        # Check if the file exists before attempting to remove it
        if os.path.exists(file_path):
            os.remove(file_path)  # Clean up the saved file
        else:
            app.logger.warning(f"File not found: {file_path}")
    else:
        return jsonify({'error': 'No file or lease text provided'}), 400

    # Set the NLTK data path to ensure the 'punkt' resource is found
    nltk.data.path.append('/usr/local/share/nltk_data')

    # Log the lease text being analyzed
    app.logger.info(f"Lease text for analysis: {lease_text}")

    # Use OpenAI GPT-3.5 Turbo to analyze the lease text
    results = analyze_lease_with_openai(lease_text)

    # Log the results of the analysis
    app.logger.info(f"Analysis results: {results}")

    return jsonify({'results': results})

@app.route('/get_sample_lease', methods=['GET'])
def get_sample_lease():
    file_path = '/home/ubuntu/leaseguard-ai/sample_lease.pdf'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    # Ensure Flask logs are output to stdout
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=5000)
