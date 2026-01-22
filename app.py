from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.ocr_extractor import extract_text_from_file
from utils.llm_processor import process_text_with_llm

app = FastAPI()

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):

    # ✅ ONLY PDF allowed (memory safe)
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only text-based PDF marksheets are supported"
        )

    # STEP 1: Extract text from PDF
    extracted_text = await extract_text_from_file(file)

    if not extracted_text.strip():
        return {
            "error": "No readable text found",
            "reason": "This PDF may be scanned or image-based",
            "solution": "Please upload a text-based PDF marksheet"
        }

    # STEP 2: Gemini / LLM extraction
    result = await process_text_with_llm(extracted_text)

    return {
        "status": "success",
        "data": result
    }
