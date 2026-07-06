import pandas as pd





def predecir_manana(df):

    # =========================
    # ORDEN SEGURIDAD
    # =========================

    from .lstm import ejecutar_prediccion


    df = df.sort_values("fecha")

    if df.empty:
        raise ValueError("DataFrame vacío")

    # =========================
    # VALORES BASE
    # =========================

    precio_actual = float(df["cierre"].iloc[-1])

    precio_predicho = ejecutar_prediccion(df)

    # =========================
    # RETORNO
    # =========================

    retorno = (
        (precio_predicho - precio_actual)
        / precio_actual
    ) * 100

    # =========================
    # TENDENCIA
    # =========================

    umbral = 1.5

    if retorno > umbral:

        tendencia = "SUBE FUERTE 📈"

        interpretacion = (
            "Se observa presión alcista en el modelo LSTM"
        )

    elif retorno < -umbral:

        tendencia = "BAJA FUERTE 📉"

        interpretacion = (
            "Se observa presión bajista en el modelo LSTM"
        )

    else:

        tendencia = "NEUTRO ➖"

        interpretacion = (
            "El modelo no detecta movimiento significativo"
        )

    # =========================
    # SEÑAL DE INVERSIÓN
    # =========================

    if retorno > 2:

        senal = "🟢 COMPRAR"

    elif retorno < -2:

        senal = "🔴 VENDER"

    else:

        senal = "🟡 MANTENER"

    # =========================
    # RANGO ESPERADO
    # =========================

    MAPE = 0.0306

    error = precio_predicho * MAPE

    minimo = precio_predicho - error

    maximo = precio_predicho + error

    # =========================
    # CONFIANZA
    # =========================

    confianza = round(
        100 - (MAPE * 100),
        2
    )

    # =========================
    # RESULTADO
    # =========================

    return {

        "precio_actual": round(precio_actual, 2),

        "precio_predicho": round(precio_predicho, 2),

        "retorno": round(retorno, 2),

        "tendencia": tendencia,

        "interpretacion": interpretacion,

        "senal": senal,

        "minimo": round(minimo, 2),

        "maximo": round(maximo, 2),

        "confianza": confianza
    }