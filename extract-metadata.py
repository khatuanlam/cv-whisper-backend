from flask import Flask, request, jsonify
import pdfplumber
import openai
import io
import os
from flask_cors import CORS

# Lấy OpenAI API key từ biến môi trường
openai.api_key = os.getenv("VITE_OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

def extract_text_pdfplumber(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

# Function to extract structured information using OpenAI
def extract_metadata_with_openai(text):
    prompt = (
        "Extract the following information from the text: "
        "1. Name, 2. Email, 3. Phone Number, 4. Skills, 5. Job Titles, 6. Education, 7. Location. "
        "Return the result as a JSON object with keys: name, email, phone, skills, job_titles, education, location.\n\n"
        f"Text: {text}\n\n"
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured information from resumes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.2
        )
        content = response.choices[0].message.content.strip()
        # Ensure always return a dict, not raw string
        import json
        try:
            metadata = json.loads(content)
        except Exception:
            metadata = content
        return metadata
    except Exception as e:
        return {"error": str(e)}

@app.route('/api/extract-metadata', methods=['POST'])
def extract_metadata():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    file_bytes = file.read()
    try:
        # Extract raw text from the PDF
        text = extract_text_pdfplumber(file_bytes)
        # Use OpenAI to extract structured metadata
        metadata = extract_metadata_with_openai(text)
        return jsonify({'metadata': metadata, 'fullText': text})
    except Exception as e:
        import traceback
        print('--- Exception in /api/extract-metadata ---')
        traceback.print_exc()
        print('-----------------------------------------')
        return jsonify({'error': str(e)}), 500

# Vercel Python function entrypoint
def handler(request):
    with app.app_context():
        return app.full_dispatch_request()
