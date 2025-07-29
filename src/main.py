# src/main.py

import os
from ocr_reader import extract_text_from_file
from extractor import parse_invoice_data
from database import create_table, insert_factura

""" def process_invoice(file_path):
    print(f"Procesando: {file_path}")
    
    text = extract_text_from_file(file_path)
    data = parse_invoice_data(text)
    save_invoice_data(data)

    print("Factura procesada exitosamente.\n") """

def main():
    file_path = "data/factura_1.pdf"  # Cambiar por archivo a Analizar

    # Crear tabla si no existe
    create_table()

    text = extract_text_from_file(file_path)
    print("\nTexto extraído:\n")
    print(text)

    print("\n📊 Datos clave extraídos:\n")
    data = parse_invoice_data(text)
    for key, value in data.items():
        print(f"{key.upper()}: {value}")

    # Guardar en base de datos
    insert_factura(data)

if __name__ == "__main__":
    main()