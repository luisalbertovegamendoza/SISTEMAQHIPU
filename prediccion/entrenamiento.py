import numpy as np
from sklearn.preprocessing import MinMaxScaler


def crear_secuencias(data_X, data_y, window_size=60):

    X = []
    y = []

    for i in range(window_size, len(data_X)-1):

        X.append(data_X[i-window_size:i])

        y.append(data_y[i+1])

    return np.array(X), np.array(y)


def preparar_dataset(df):

    dataset = df[
        [
            "apertura",
            "maximo",
            "minimo",
            "cierre",
            "volumen",
            "sma_10",
            "sma_30",
            "retorno",
            "volatilidad",
            "ema_10",
            "rsi",
            "macd"
        ]
    ].values

    scaler_X = MinMaxScaler(feature_range=(-1, 1))

    scaler_y = MinMaxScaler(feature_range=(-1, 1))

    X_scaled = scaler_X.fit_transform(dataset)

    y_scaled = scaler_y.fit_transform(
        dataset[:, 3].reshape(-1, 1)
    )

    X, y = crear_secuencias(
        X_scaled,
        y_scaled,
        window_size=60
    )

    return X, y, scaler_X, scaler_y