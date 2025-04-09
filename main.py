from fastapi import FastAPI, UploadFile, File
from app.ocr_engine import extract_text
from app.parser_ktp import parse_ktp_text
from app.parser_npwp import parse_npwp_text
from app.parser_CC import extract_credit_card_info
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
        doc_type = doc_type.lower()
        if doc_type == "ktp":
            result = parse_ktp_text(text)
        elif doc_type == "npwp":
            result = parse_npwp_text(text)
        elif doc_type in ["cc", "creditcard"]:
            result = extract_credit_card_info(text)
        else:
            result = {"error": f"Unsupported document type: {doc_type}"}

        return {"text": text, "parsed": result}
    finally:
        if os.path.exists(path):
            os.remove(path)
