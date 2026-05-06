"""
OCR / text extraction service — supports PDF, DOCX, and TXT files.
Dispatches to the right parser based on file extension.
"""

import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

try:
    from docx import Document as DocxDocument
    _DOCX_AVAILABLE = True
except ImportError:
    _DOCX_AVAILABLE = False


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from PDF bytes.
    First attempts direct text extraction via PyMuPDF.
    Falls back to Tesseract OCR for scanned / image-only pages.
    """
    text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text + "\n"
            else:
                # Fallback to OCR for scanned pages
                try:
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    ocr_text = pytesseract.image_to_string(img)
                    text += ocr_text + "\n"
                except Exception as e:
                    print(f"OCR failed for page: {e}")
    except Exception as e:
        print(f"Error processing PDF: {e}")
    return text


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extracts plain text from a .docx file."""
    if not _DOCX_AVAILABLE:
        raise RuntimeError("python-docx is not installed. Run: pip install python-docx")
    try:
        doc = DocxDocument(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        print(f"Error processing DOCX: {e}")
        return ""


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decodes plain text from a .txt file, trying UTF-8 then latin-1."""
    for encoding in ("utf-8", "latin-1", "cp1252"):
        try:
            return file_bytes.decode(encoding)
        except (UnicodeDecodeError, Exception):
            continue
    return file_bytes.decode("utf-8", errors="replace")


def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Dispatcher — routes to the right extractor based on file extension.
    Supports: .pdf, .docx, .doc, .txt
    """
    name_lower = filename.lower()
    if name_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif name_lower.endswith(".docx") or name_lower.endswith(".doc"):
        return extract_text_from_docx(file_bytes)
    elif name_lower.endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    else:
        # Best-effort: try PDF then plain text
        text = extract_text_from_pdf(file_bytes)
        if not text.strip():
            text = extract_text_from_txt(file_bytes)
        return text
