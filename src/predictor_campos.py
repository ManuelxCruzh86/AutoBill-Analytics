# src/predictor_campos.py

import joblib
import os

modelos = {}
vectorizadores = {}

def cargar_modelo_y_vectorizador(nombre_campo):
    modelo_path = os.path.join("src", f"model_{nombre_campo}.pkl")
    vector_path = os.path.join("src", f"vectorizer_{nombre_campo}.pkl")

    if not os.path.exists(modelo_path) or not os.path.exists(vector_path):
        print(f"⚠️ Modelo o vectorizador para '{nombre_campo}' no existe.")
        return None, None

    if nombre_campo not in modelos:
        modelos[nombre_campo] = joblib.load(modelo_path)
        vectorizadores[nombre_campo] = joblib.load(vector_path)

    return modelos[nombre_campo], vectorizadores[nombre_campo]


def predecir_campo(texto, campo):
    modelo, vector = cargar_modelo_y_vectorizador(campo)
    if not modelo or not vector:
        return "no_modelo"
    X = vector.transform([texto])
    return modelo.predict(X)[0]
