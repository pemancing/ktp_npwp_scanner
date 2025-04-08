from fastapi import FastAPI, UploadFile, File
from app.ocr_engine import extract_text
from app.parser_ktp import parse_ktp_text
from app.parser_npwp import parse_npwp_text
import shutil
import os

app = FastAPI()

@app.post("/scan/{doc_type}")
async def scan_document(doc_type: str, file: UploadFile = File(...)):
    path = f"temp_{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = extract_text(path)
        result = parse_ktp_text(text) if doc_type.lower() == "ktp" else parse_npwp_text(text)

        return {"text": text, "parsed": result}
    finally:
        if os.path.exists(path):
            os.remove(path)
