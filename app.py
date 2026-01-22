from fastapi import FastAPI, UploadFile, File
from PIL import Image
import pytesseract
import io
import re

app = FastAPI(title="AI Marksheet Extraction API")

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    text = pytesseract.image_to_string(image)

    name = re.search(r"Name\s*[:\-]?\s*(.*)", text)
    roll = re.search(r"Roll\s*No\s*[:\-]?\s*(\d+)", text)

    return {
        "student_name": name.group(1).strip() if name else None,
        "roll_number": roll.group(1) if roll else None,
        "raw_text_preview": text[:500]
    }
