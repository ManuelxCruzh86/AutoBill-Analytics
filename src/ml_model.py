# src/ml_model.py

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Ruta del archivo de entrenamiento
data_path = os.path.join("data", "datos_entrenamiento.csv")

# Leer el archivo CSV
df = pd.read_csv(data_path)

# Asegurar que existe la columna "texto_crudo"
if 'texto_crudo' not in df.columns:
    raise ValueError("El archivo no contiene la columna 'texto_crudo'.")

X = df['texto_crudo']

# Vectorizar el texto con TF-IDF
vectorizer = TfidfVectorizer(max_features=500)
X_vec = vectorizer.fit_transform(X)

# Guardar solo el vectorizador para futuras predicciones
vectorizer_path = os.path.join("src", "vectorizer.pkl")
joblib.dump(vectorizer, vectorizer_path)

print("✅ Vectorizador TF-IDF entrenado y guardado correctamente. Aún no se entrena un modelo porque no hay etiquetas.")
