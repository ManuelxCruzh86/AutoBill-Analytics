# src/ocr_reader.py

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# Ruta a tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ruta de Poppler
POPPLER_PATH = r"C:\Poppler\poppler-24.08.0\Library\bin"

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    full_text = ""
    for i, page in enumerate(pages):
        temp_filename = f"page_{i}.jpg"
        page.save(temp_filename, "JPEG")
        text = extract_text_from_image(temp_filename)
        full_text += f"\n--- Página {i+1} ---\n{text}"
        os.remove(temp_filename)
    return full_text

def extract_text_from_file(file_path):
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        return extract_text_from_image(file_path)
