from flask import Flask, request, jsonify
import pdfplumber
import io

app = Flask(__name__)

@app.route('/api/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    file_bytes = file.read()
    try:
        text = extract_text_pdfplumber(file_bytes)
    except Exception:
        text = ""
    return jsonify({'text': text})

def extract_text_pdfplumber(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

# Vercel Python function entrypoint
def handler(request):
    with app.app_context():
        return app.full_dispatch_request()
