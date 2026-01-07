import io
from docx import Document
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


def generate_txt(content: str) -> bytes:
    return content.encode("utf-8")


def generate_docx(content: str) -> bytes:
    doc = Document()
    doc.add_paragraph(content)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.read()


def generate_pdf(content: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)

    text = c.beginText(40, 750)
    for line in content.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()
