# src/main.py

import os
import shutil
from ocr_reader import extract_text_from_file
from extractor import parse_invoice_data
from database import create_table, insert_factura, factura_exists
from export_csv import export_to_csv

def abrir_powerbi():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        plantilla_path = os.path.join(script_dir, "..", "plantillas", "PlantillaAutobill.pbix")
        os.startfile(plantilla_path)
        print("🟢 Power BI abierto. Solo presiona 'Actualizar' para ver los nuevos datos.")
    except Exception as e:
        print("⚠️ No se pudo abrir Power BI automáticamente:", e)

def save_invoice_to_db(data):
    if factura_exists(data): 
        print(f"🔁 Factura ya existente (folio: {data.get('folio')}, emisor: {data.get('emisor')}). Se omite.")
    else:
        insert_factura(data)
        print(f"✅ Factura guardada: {data.get('folio')}")

def main():
    print("📥 Procesando archivos de entrada...")

    data_folder = "data"
    processed_folder = "procesados"

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"⚠️ La carpeta '{data_folder}' no existía y fue creada. Agrega archivos para procesar.")
        return

    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    for file_name in os.listdir(data_folder):
        file_path = os.path.join(data_folder, file_name)

        if not file_name.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
            continue

        print(f"📄 Leyendo archivo: {file_name}")
        text = extract_text_from_file(file_path)
        invoice_data = parse_invoice_data(text)

        if invoice_data:
            save_invoice_to_db(invoice_data)
            shutil.move(file_path, os.path.join(processed_folder, file_name))
        else:
            print(f"❌ No se pudo extraer información válida de: {file_name}")

    print("✅ Extracción completada.")

    print("📤 Exportando datos a CSV...")
    export_to_csv()
    print("✅ Archivo Excel generado correctamente.")

    abrir_powerbi()
 
if __name__ == "__main__":
    create_table()  
    main()
