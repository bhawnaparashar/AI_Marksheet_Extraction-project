from fastapi import FastAPI, UploadFile, File
import pytesseract
from PIL import Image
import io
import re

app = FastAPI()

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    text = pytesseract.image_to_string(image)

    # very basic extraction logic
    name = re.search(r"Name\s*:\s*(.*)", text)
    roll = re.search(r"Roll\s*No\s*:\s*(\d+)", text)

    return {
        "student_name": name.group(1) if name else None,
        "roll_number": roll.group(1) if roll else None,
        "raw_text": text[:1000]  # proof of OCR
    }
