from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.ocr_extractor import extract_text_from_file
from utils.llm_processor import process_text_with_llm

app = FastAPI()

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # STEP 1: OCR
    extracted_text = await extract_text_from_file(file)

    if not extracted_text.strip():
        raise HTTPException(status_code=500, detail="No text extracted")

    # STEP 2: Gemini
    result = await process_text_with_llm(extracted_text)

    return result
