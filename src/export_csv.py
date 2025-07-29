# src/export_csv.py

import sqlite3
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "facturas.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "facturas_export.csv")

def export_to_csv():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM facturas", conn)
    conn.close()
    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Exportado a CSV: {CSV_PATH}")
