from PyPDF2 import PdfReader

async def extract_text_from_file(file):
    if not file.filename.lower().endswith(".pdf"):
        return ""

    pdf = PdfReader(file.file)
    text = ""

    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()

    return text

