import pdfplumber
import openai
import io
from typing import Any
import os

def extract_text_pdfplumber(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_metadata_with_openai(text):
    prompt = (
        "Extract the following information from the text: "
        "1. Name, 2. Email, 3. Phone Number, 4. Skills, 5. Job Titles, 6. Education, 7. Location. "
        "Return the result as a JSON object with keys: name, email, phone, skills, job_titles, education, location.\n\n"
        f"Text: {text}\n\n"
    )
    openai.api_key = os.environ.get("OPENAI_API_KEY")
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
        return response.choices[0].message.content.strip()
    except Exception as e:
        return {"error": str(e)}

def handler(request: Any):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": "Method Not Allowed"
        }
    try:
        file = request.files["file"]
        file_bytes = file.read()
        text = extract_text_pdfplumber(file_bytes)
        metadata = extract_metadata_with_openai(text)
        return {
            "statusCode": 200,
            "body": {"metadata": metadata}
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": {"error": str(e)}
        }
