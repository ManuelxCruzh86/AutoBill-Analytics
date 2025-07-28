# src/main.py

import os
from ocr_reader import extract_text_from_file
""" from extractor import parse_invoice_data
from database import save_invoice_data """

""" def process_invoice(file_path):
    print(f"Procesando: {file_path}")
    
    text = extract_text_from_file(file_path)
    data = parse_invoice_data(text)
    save_invoice_data(data)

    print("Factura procesada exitosamente.\n") """

def main():
    file_path = "data/factura_1.pdf"  # Cambia por un archivo real que tengas
    text = extract_text_from_file(file_path)
    print("\nTexto extraído:\n")
    print(text)

if __name__ == "__main__":
    main()