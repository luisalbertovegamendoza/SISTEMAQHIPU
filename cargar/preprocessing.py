import pandas as pd
import numpy as np


def limpiar_datos(df):

    df = df.copy()

    # =========================
    # 📊 REPORTE
    # =========================

    reporte = {}

    registros_antes = len(df)

    # =========================
    # 🧼 LIMPIAR COLUMNAS
    # =========================

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace('\ufeff', '')
    )

    print("COLUMNAS DETECTADAS:", df.columns.tolist())

    # =========================
    # 📌 VALIDAR COLUMNAS
    # =========================

    columnas_requeridas = [
        'fecha', 'apertura', 'cierre',
        'maximo', 'minimo'
    ]

    for col in columnas_requeridas:

        if col not in df.columns:

            raise Exception(
                f"Falta columna: {col}"
            )

    # =========================
    # 📅 CONVERTIR FECHA
    # =========================

    df['fecha'] = pd.to_datetime(
        df['fecha'],
        errors='coerce',
        dayfirst=True
    )

    # fechas inválidas
    fechas_invalidas = df['fecha'].isnull().sum()

    df = df.dropna(subset=['fecha'])

    # =========================
    # 📊 ORDENAR
    # =========================

    df = df.sort_values(
        'fecha'
    ).reset_index(drop=True)

    # =========================
    # 🧹 DUPLICADOS
    # =========================

    duplicados = df.duplicated().sum()

    df = df.drop_duplicates()

    # =========================
    # ⚠️ NULOS
    # =========================

    nulos_antes = df.isnull().sum().sum()

    df = df.dropna()

    registros_despues = len(df)

    # =========================
    # 📦 REPORTE FINAL
    # =========================

    reporte = {

        'registros_antes': registros_antes,

        'registros_despues': registros_despues,

        'nulos_eliminados': int(nulos_antes),

        'duplicados_eliminados': int(duplicados),

        'fechas_invalidas': int(fechas_invalidas),

        'columnas_detectadas': len(df.columns)

    }

    return df, reporte