import numpy as np
import pandas as pd


def agregar_indicadores(df):

    df = df.copy()

    # =========================
    # 🔥 CONVERSIÓN CRÍTICA (OBLIGATORIO)
    # =========================
    columnas = ['cierre', 'apertura', 'maximo', 'minimo']

    for col in columnas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')



        

    # =========================
    # 🧹 LIMPIEZA BASE
    # =========================
    df = df.dropna(subset=['cierre', 'fecha'])

    
    df = df.sort_values('fecha')

    # =========================
    # 📊 SMA
    # =========================
    df['sma_10'] = df['cierre'].rolling(10, min_periods=1).mean()
    df['sma_30'] = df['cierre'].rolling(30, min_periods=1).mean()

    # =========================
    # 📈 RETORNO
    # =========================
    df['retorno'] = np.log(df['cierre'] / df['cierre'].shift(1))

    # =========================
    # 📉 VOLATILIDAD
    # =========================
    df['volatilidad'] = df['retorno'].rolling(10, min_periods=1).std()

    # =========================
    # 📊 EMA
    # =========================
    df['ema_10'] = df['cierre'].ewm(span=10, adjust=False).mean()

    # =========================
    # 📉 RSI (FIX CORRECTO)
    # =========================
    delta = df['cierre'].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, min_periods=14, adjust=False).mean()


    rs = avg_gain / (avg_loss + 1e-10)

    df['rsi'] = 100 - (100 / (1 + rs))

    # =========================
    # 📈 MACD (COMPLETO)
    # =========================
    ema12 = df['cierre'].ewm(span=12, adjust=False).mean()
    ema26 = df['cierre'].ewm(span=26, adjust=False).mean()

    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['histograma'] = df['macd'] - df['signal']

    # =========================
    # 🧹 LIMPIEZA FINAL
    # =========================
    
    df = df.fillna(method='bfill')
    df = df.fillna(0)


    return df