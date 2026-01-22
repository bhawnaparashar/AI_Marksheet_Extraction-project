from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io
import pytesseract
import re

app = FastAPI()

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    try:
        # Read uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # OCR using pytesseract
        text = pytesseract.image_to_string(image)

        # Initialize extracted data
        extracted_data = {
            "name": None,
            "roll_no": None,
            "marks": None
        }

        # Extract Name
        name_match = re.search(r"Name[:\-]?\s*(.*)", text, re.IGNORECASE)
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
