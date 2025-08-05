# src/train_fields.py

import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Ruta del dataset
data_path = os.path.join("data", "datos_entrenamiento.csv")

# Campos que vamos a entrenar
campos_objetivo = ["rfc_emisor", "rfc_receptor", "total", "fecha", "folio"]

# Cargando los datos
print("📊 Cargando datos de entrenamiento...")
df = pd.read_csv(data_path)

if "texto_crudo" not in df.columns:
    raise ValueError("El archivo debe contener la columna 'texto_crudo'.")

for campo in campos_objetivo:
    if campo not in df.columns:
        print(f"⚠️ Campo '{campo}' no encontrado en el CSV. Se omite.")
        continue

    print(f"🚀 Entrenando modelo para el campo: {campo}")

    X = df["texto_crudo"]
    y = df[campo].astype(str)  

    vectorizer = TfidfVectorizer(max_features=1000)
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression(max_iter=200)
    model.fit(X_vec, y)

    joblib.dump(vectorizer, os.path.join("src", f"vectorizer_{campo}.pkl"))
    joblib.dump(model, os.path.join("src", f"model_{campo}.pkl"))

    print(f"✅ Modelo y vectorizador para '{campo}' guardados correctamente.")

print("🎉 Entrenamiento completado para todos los campos disponibles.")
