# src/database.py

import sqlite3
import os

# Ruta de base de datos en data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "facturas.db")

# Crear la carpeta data si no existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proveedor TEXT,
        rfc TEXT,
        fecha TEXT,
        subtotal TEXT,
        iva TEXT,
        total TEXT,
        UNIQUE(rfc, fecha, total)
    )
    """)

    conn.commit()
    conn.close()

def insert_factura(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO facturas (proveedor, rfc, fecha, subtotal, iva, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get("proveedor"),
            data.get("rfc"),
            data.get("fecha"),
            data.get("subtotal"),
            data.get("iva"),
            data.get("total")
        ))
        conn.commit()
        print("✅ Factura guardada en la base de datos.")
    except sqlite3.IntegrityError:
        print("⚠️ Factura duplicada. No se guardó.")
    finally:
        conn.close()

# Verificar si ya existe la factura
def factura_exists(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM facturas 
        WHERE rfc = ? AND fecha = ? AND total = ?
    """, (
        data.get("rfc"),
        data.get("fecha"),
        data.get("total")
    ))

    result = cursor.fetchone()[0]
    conn.close()
    return result > 0
