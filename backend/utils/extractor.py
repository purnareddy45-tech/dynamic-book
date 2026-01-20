import fitz  # PyMuPDF
from docx import Document
from io import BytesIO


def extract_text(file_bytes: bytes) -> str:
    """
    Extract text from text-based PDF and DOCX files.
    OCR is NOT used.
    """

    text = ""

    # Try PDF
    try:
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf:
            text += page.get_text()
        pdf.close()
        if text.strip():
            return text
    except Exception:
        pass

    # Try DOCX
    try:
        doc = Document(BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
        if text.strip():
            return text
    except Exception:
        pass

    raise ValueError("Unsupported file type or empty document")
