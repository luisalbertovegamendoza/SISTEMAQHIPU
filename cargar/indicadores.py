import numpy as np


def agregar_indicadores(df):

    df = df.copy()

    # =========================
    # 📊 MEDIAS MÓVILES
    # =========================
    df['sma_10'] = df['cierre'].rolling(10, min_periods=1).mean()
    df['sma_30'] = df['cierre'].rolling(30, min_periods=1).mean()

    # =========================
    # 📈 RETORNO LOG
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
    # 📉 RSI (seguro)
    # =========================
    delta = df['cierre'].diff()

    gain = delta.clip(lower=0).rolling(14, min_periods=1).mean()
    loss = (-delta.clip(upper=0)).rolling(14, min_periods=1).mean()

    rs = gain / (loss + 1e-10)  # evita división por cero

    df['rsi'] = 100 - (100 / (1 + rs))

    # =========================
    # 📊 MACD
    # =========================
    ema12 = df['cierre'].ewm(span=12, adjust=False).mean()
    ema26 = df['cierre'].ewm(span=26, adjust=False).mean()

    df['macd'] = ema12 - ema26

    # =========================
    # ⚠️ LIMPIEZA SEGURA (NO ROMPER DATASET)
    # =========================
    df = df.dropna(subset=['cierre'])

    return df