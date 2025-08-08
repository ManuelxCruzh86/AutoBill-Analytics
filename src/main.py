# src/main.py

import os
import shutil
import csv
import joblib
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
    entrenamiento_csv = os.path.join(data_folder, "datos_entrenamiento.csv")
    datos_entrenamiento = []

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

        # Guardar texto crudo + datos extraídos para entrenamiento supervisado
        datos_entrenamiento.append({
            "nombre_archivo": file_name,
            "texto_crudo": text.replace("\n", " "),
            "rfc_emisor": invoice_data.get("rfc_emisor", ""),
            "rfc_receptor": invoice_data.get("rfc_receptor", ""),
            "subtotal": invoice_data.get("subtotal", ""),      # <--- Agrega esto
            "iva": invoice_data.get("iva", ""),                # <--- Y esto
            "total": invoice_data.get("total", ""),
            "fecha": invoice_data.get("fecha", ""),
            "folio": invoice_data.get("folio", "")
        })

        if invoice_data:
            save_invoice_to_db(invoice_data)
            shutil.move(file_path, os.path.join(processed_folder, file_name))
        else:
            print(f"❌ No se pudo extraer información válida de: {file_name}")

    # Guardar CSV de entrenamiento (acumulativo)
    campos = ["nombre_archivo", "texto_crudo", "rfc_emisor", "rfc_receptor", "subtotal", "iva", "total", "fecha", "folio"]
    datos_previos = []

    # Si el archivo existe, lee los datos previos
    if os.path.exists(entrenamiento_csv):
        with open(entrenamiento_csv, mode="r", encoding="utf-8", newline="") as archivo_csv:
            reader = csv.DictReader(archivo_csv)
            datos_previos = list(reader)

    # Opcional: Evita duplicados por nombre_archivo
    archivos_existentes = {d["nombre_archivo"] for d in datos_previos}
    nuevos_datos = [d for d in datos_entrenamiento if d["nombre_archivo"] not in archivos_existentes]

    # Une los datos previos con los nuevos
    datos_finales = datos_previos + nuevos_datos

    with open(entrenamiento_csv, mode="w", encoding="utf-8", newline="") as archivo_csv:
        writer = csv.DictWriter(archivo_csv, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos_finales)

    print(f"✅ Se generó el archivo {entrenamiento_csv} con {len(datos_finales)} textos crudos.")

    print("📤 Exportando datos a CSV...")
    export_to_csv()
    print("✅ Archivo Excel generado correctamente.")

    abrir_powerbi()


if __name__ == "__main__":
    create_table()
    main()
