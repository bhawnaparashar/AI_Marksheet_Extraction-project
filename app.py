from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.ocr_extractor import extract_text_from_file
from utils.llm_processor import process_text_with_llm

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Marksheet Extraction API is running"}

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    try:
        if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        extracted_text = await extract_text_from_file(file)

        if not extracted_text or len(extracted_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file does not contain enough readable marksheet text"
            )

        result = await process_text_with_llm(extracted_text)
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

