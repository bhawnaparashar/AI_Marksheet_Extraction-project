from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io

app = FastAPI()

@app.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # TEMP DUMMY RESPONSE (for deployment)
        return {
            "message": "Image received successfully",
            "filename": file.filename,
            "image_size": image.size
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )    
