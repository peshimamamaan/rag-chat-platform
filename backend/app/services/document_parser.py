from pypdf import PdfReader
from fastapi import UploadFile
import io

def parse_txt(file: UploadFile) -> str:
    content = file.file.read()
    return content.decode("utf-8", errors="ignore")

def parse_pdf(file: UploadFile) -> str:
    reader = PdfReader(io.BytesIO(file.file.read()))
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def parse_document(file: UploadFile) -> str:
    if file.filename and file.filename.endswith(".txt"):
        return parse_txt(file)

    if file.filename and file.filename.endswith(".pdf"):
        return parse_pdf(file)


    raise ValueError("Unsupported file type")

def parse_text(raw_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(raw_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    return raw_bytes.decode("utf-8")