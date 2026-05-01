import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from PDF bytes. 
    First attempts to extract text directly using PyMuPDF. 
    If a page has no text, it falls back to OCR via pytesseract.
    """
    text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text + "\n"
            else:
                # Fallback to OCR for scanned pages/images
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
