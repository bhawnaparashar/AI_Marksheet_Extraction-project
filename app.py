from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="AI Marksheet Extraction API")

@app.get("/")
def root():
    return {"message": "API is running successfully"}

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "status": "received"
    }
