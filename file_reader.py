import os
import docx
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image
import io
import pytesseract

# Update this path to match your system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

SUPPORTED_EXTS = [".txt", ".pdf", ".docx", ".csv", ".xlsx"]

def extract_text_from_pdf_with_ocr(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes()))
        page_text = pytesseract.image_to_string(img)
        text += page_text + "\n"
    return text

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == ".pdf":
            return extract_text_from_pdf_with_ocr(file_path)
        elif ext == ".docx":
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        elif ext == ".csv":
            df = pd.read_csv(file_path)
            return df.to_string(index=False)
        elif ext == ".xlsx":
            df = pd.read_excel(file_path, sheet_name=None)
            return "\n".join([df[sheet].to_string(index=False) for sheet in df])
        else:
            return f"[Skipped unsupported file type: {file_path}]"
    except Exception as e:
        return f"[Error reading {file_path}: {str(e)}]"

def get_supported_files(folder_path):
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS
    ]