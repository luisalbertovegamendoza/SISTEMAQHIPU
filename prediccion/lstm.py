import os
import json
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "modelos")


# =========================
# CARGA UNA SOLA VEZ (OPTIMIZADO)
# =========================
modelo = load_model(os.path.join(MODEL_DIR, "modelo_lstm_ferreycorp.keras"))
scaler_X = joblib.load(os.path.join(MODEL_DIR, "scaler_X.pkl"))
scaler_y = joblib.load(os.path.join(MODEL_DIR, "scaler_y.pkl"))

with open(os.path.join(MODEL_DIR, "config.json"), "r") as f:
    config = json.load(f)


def ejecutar_prediccion(df):

    features = config["features"]
    window_size = config["window_size"]

    # =========================
    # VALIDACIONES CRÍTICAS
    # =========================
    df = df.sort_values("fecha") if "fecha" in df.columns else df

    if len(df) < window_size:
        raise ValueError("No hay suficientes datos para predecir")

    missing = [c for c in features if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")

    # =========================
    # LIMPIEZA SEGURA
    # =========================
    data = df[features].tail(window_size).copy()
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.dropna()

    if len(data) < window_size:
        raise ValueError("Datos insuficientes después de limpieza")

    # =========================
    # ESCALADO
    # =========================
    data_scaled = scaler_X.transform(data.values)

  

    # =========================
    # RESHAPE LSTM
    # =========================
    X = np.reshape(
        data_scaled,
        (1, window_size, len(features))
    )

    # =========================
    # PREDICCIÓN
    # =========================
    pred_scaled = modelo.predict(X, verbose=0)

    pred = scaler_y.inverse_transform(pred_scaled)[0][0]

    print("Predicción Django:", pred)

    return float(pred)

   

def predecir_historico(df):

    features = config["features"]
    window_size = config["window_size"]

    df = df.sort_values("fecha")

    data = df[features].copy()

    data = data.replace([np.inf, -np.inf], np.nan)

    data = data.dropna()

    data_scaled = scaler_X.transform(data.values)

    predicciones = []

    fechas = []

    # =========================
    # OPTIMIZACIÓN
    # =========================
    # Antes:
    # for i in range(window_size, len(data_scaled))
    #
    # Ahora:
    # calcula una predicción cada 3 registros
    # =========================

    for i in range(window_size, len(data_scaled), 3):

        X = data_scaled[
            i - window_size:i
        ]

        X = X.reshape(
            1,
            window_size,
            len(features)
        )

        pred_scaled = modelo.predict(
            X,
            verbose=0
        )

        pred_real = scaler_y.inverse_transform(
            pred_scaled
        )[0][0]

        predicciones.append(
            float(pred_real)
        )

        fechas.append(
            df.iloc[i]["fecha"]
        )

    return fechas, predicciones