from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io
import easyocr
import re

app = FastAPI()

# Initialize EasyOCR once
reader = easyocr.Reader(['en'])  # English

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    try:
        # Read uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')

        # Convert image to bytes for EasyOCR
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        # OCR with EasyOCR
        result = reader.readtext(image_bytes)

        # Combine all detected text into a single string
        text = " ".join([item[1] for item in result])

        # Initialize extracted data
        extracted_data = {
            "name": None,
            "roll_no": None,
            "marks": None
        }

        # Extract Name (assumes "Name: John Doe")
        name_match = re.search(r"Name[:\-]?\s*([A-Za-z ]+)", text, re.IGNORECASE)
        if name_match:
            extracted_data["name"] = name_match.group(1).strip()

        # Extract Roll Number
        roll_match = re.search(r"Roll\s*No[:\-]?\s*(\w+)", text, re.IGNORECASE)
        if roll_match:
            extracted_data["roll_no"] = roll_match.group(1).strip()

        # Extract Marks
        marks_match = re.search(r"Marks[:\-]?\s*(\d+)", text, re.IGNORECASE)
        if marks_match:
            extracted_data["marks"] = marks_match.group(1).strip()

        return {
            "message": "Extraction successful",
            "filename": file.filename,
            "image_size": image.size,
            "extracted_data": extracted_data
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
)
