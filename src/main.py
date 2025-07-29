# src/main.py

import os
from ocr_reader import extract_text_from_file
from extractor import parse_invoice_data
from database import create_table, insert_factura
from export_csv import export_to_csv

def abrir_powerbi():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        plantilla_path = os.path.join(script_dir, "..", "plantillas", "plantilla.pbix")
        os.startfile(plantilla_path)
        print("🟢 Power BI abierto. Solo presiona 'Actualizar' para ver los nuevos datos.")
    except Exception as e:
        print("⚠️ No se pudo abrir Power BI automáticamente:", e)



def main():
    print("📥 Procesando archivos de entrada...")

    input_folder = "input"
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"⚠️ La carpeta '{input_folder}' no existía y fue creada. Agrega archivos para procesar.")
        return

    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
      

        if not file_name.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
            continue

        print(f"📄 Leyendo archivo: {file_name}")
        text = extract_text_from_file(file_path)
        data = extract_invoice_data(text)

        if data:
            save_invoice_to_db(data)
        else:
            print(f"❌ No se pudo extraer información válida de: {file_name}")

    print("✅ Extracción completada.")

    print("📤 Exportando datos a CSV...")
    export_to_csv()

    print("✅ Archivo Excel generado correctamente.")
    
    abrir_powerbi()

if __name__ == "__main__":
    main()
