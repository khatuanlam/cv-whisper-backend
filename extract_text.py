import pdfplumber
import io
from typing import Any

def handler(request: Any):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": "Method Not Allowed"
        }
    try:
        file = request.files["file"]
        file_bytes = file.read()
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        text = text.strip()
        return {
            "statusCode": 200,
            "body": {"text": text}
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": {"error": str(e)}
        }
