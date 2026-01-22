from PIL import Image
from PyPDF2 import PdfReader
import easyocr

reader = easyocr.Reader(['en'])

async def extract_text_from_file(file):
    if file.filename.lower().endswith(".pdf"):
        pdf = PdfReader(file.file)
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
        return text
    else:
        image = Image.open(file.file)
        result = reader.readtext(image)
        return " ".join([r[1] for r in result])
