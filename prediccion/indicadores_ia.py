import numpy as np
import pandas as pd


def agregar_indicadores(df):

    df = df.copy()

    # =========================
    # CONVERSIÓN DE TIPOS
    # =========================

    columnas = [
        'apertura',
        'maximo',
        'minimo',
        'cierre',
        'volumen'
    ]

    for col in columnas:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors='coerce'
            )

    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(
            df['fecha'],
            errors='coerce'
        )

    # =========================
    # LIMPIEZA BASE
    # =========================

    df = df.dropna(
        subset=['fecha', 'cierre']
    )

    df = df.sort_values(
        'fecha'
    )

    # =========================
    # TRANSFORMACIÓN VOLUMEN
    # IGUAL QUE COLAB
    # =========================

    df['volumen'] = np.log1p(
        df['volumen']
    )

    # =========================
    # SMA 10
    # =========================

    df['sma_10'] = (
        df['cierre']
        .rolling(10)
        .mean()
    )

    # =========================
    # SMA 30
    # =========================

    df['sma_30'] = (
        df['cierre']
        .rolling(30)
        .mean()
    )

    # =========================
    # RETORNO
    # =========================

    df['retorno'] = np.log(
        df['cierre'] /
        df['cierre'].shift(1)
    )

    # =========================
    # VOLATILIDAD
    # =========================

    df['volatilidad'] = (
        df['retorno']
        .rolling(10)
        .std()
    )

    # =========================
    # EMA 10
    # IGUAL QUE COLAB
    # =========================

    df['ema_10'] = (
        df['cierre']
        .ewm(span=10)
        .mean()
    )

    # =========================
    # RSI
    # IGUAL QUE COLAB
    # =========================

    delta = df['cierre'].diff()

    gain = (
        delta
        .clip(lower=0)
        .rolling(14)
        .mean()
    )

    loss = (
        -delta
        .clip(upper=0)
        .rolling(14)
        .mean()
    )

    rs = gain / loss

    df['rsi'] = (
        100 -
        (100 / (1 + rs))
    )

    # =========================
    # MACD
    # IGUAL QUE COLAB
    # =========================

    ema12 = (
        df['cierre']
        .ewm(span=12)
        .mean()
    )

    ema26 = (
        df['cierre']
        .ewm(span=26)
        .mean()
    )

    df['macd'] = ema12 - ema26

    # =========================
    # ELIMINAR NaN
    # =========================

    df = df.dropna()

    # =========================
    # RESET INDEX
    # =========================

    df = df.reset_index(
        drop=True
    )

    return df