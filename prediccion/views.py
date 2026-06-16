from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import pandas as pd
from datetime import datetime

from cargar.models import StockData
from django.shortcuts import redirect, render
from django.contrib import messages

from .predictores import predecir_manana
from .graficos import grafico_prediccion
from .indicadores_ia import agregar_indicadores
from cargar.utils import usuario_tiene_datos



@login_required
def prediccion_ia(request):
    if not usuario_tiene_datos(request.user):

        messages.warning(
            request,
            "Primero debe cargar datos históricos."
        )

        return redirect("cargar")

    try:

        # ==================================
        # 1. CARGAR DATOS
        # ==================================
        datos = list(
            StockData.objects
            .filter(usuario=request.user)
            .order_by('fecha')
            .values(
                'fecha',
                'apertura',
                'cierre',
                'maximo',
                'minimo',
                'volumen'
            )
        )

        df = pd.DataFrame.from_records(datos)

        if df.empty:
            raise ValueError("No existen datos cargados para realizar la predicción.")

        # ==================================
        # 2. LIMPIEZA
        # ==================================
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

        columnas_numericas = ['apertura', 'cierre', 'maximo', 'minimo', 'volumen']

        df[columnas_numericas] = df[columnas_numericas].apply(pd.to_numeric, errors='coerce')

        df = df.dropna(subset=['fecha', 'cierre'])

        df = df.sort_values('fecha')

        # ==================================
        # 3. INDICADORES
        # ==================================
        df = agregar_indicadores(df)
        df = df.dropna()
        df = df.reset_index(drop=True)

        if len(df) < 60:
            raise ValueError("No existen suficientes registros para generar la predicción.")

        # ==================================
        # 4. INDICADORES ÚLTIMOS
        # ==================================
        rsi = round(float(df['rsi'].iloc[-1]), 2)

        if rsi > 70:
            estado_rsi = "Sobrecomprado"

        elif rsi < 30:
            estado_rsi = "Sobrevendido"

        else:
            estado_rsi = "Neutral"



        macd = round(float(df['macd'].iloc[-1]), 4)

        if macd > 0:
                estado_macd = "Alcista"

        elif macd < 0:
                 estado_macd = "Bajista"

        else:
                estado_macd = "Neutral"


        sma10 = round(float(df['sma_10'].iloc[-1]), 2)
        sma30 = round(float(df['sma_30'].iloc[-1]), 2)

        # ==================================
        # 5. PREDICCIÓN IA
        # ==================================
        resultado = predecir_manana(df)

        # ==================================
        # 6. DATOS ADICIONALES
        # ==================================
        fecha_prediccion = datetime.now().strftime("%d/%m/%Y %H:%M")

        diferencia = round(
            resultado["precio_predicho"] - resultado["precio_actual"],
            2
        )

        ganancia_potencial = round(
            resultado["precio_predicho"] -
            resultado["precio_actual"],
             2
                )




        # ==================================
        # 7. RIESGO
        # ==================================
        retorno_abs = abs(resultado["retorno"])

        if retorno_abs < 2:
            riesgo = "🟢 Bajo"

        elif retorno_abs < 5:
            riesgo = "🟡 Moderado"

        else:
             riesgo = "🔴 Alto"

        # ==================================
        # 8. RECOMENDACIÓN IA
        # ==================================
        retorno_predicho = resultado["retorno"]

        if retorno_predicho > 5:

            recomendacion = (
                     "La IA detecta una posible oportunidad de compra con expectativa alcista fuerte."
             )

        elif retorno_predicho > 2:

            recomendacion = (
                         "La IA detecta una tendencia alcista moderada."
             )

        elif retorno_predicho < -5:

            recomendacion = (
                         "La IA detecta una presión bajista importante."
    )

        elif retorno_predicho < -2:

            recomendacion = (
                         "La IA detecta una tendencia bajista moderada."
    )

        else:

            recomendacion = (
                "La IA no detecta movimientos significativos."
         )

        # ==================================
        # 9. MÉTRICAS DEL MODELO
        # ==================================
        r2 = 0.8745
        rmse = 0.1486
        mape = 3.06
        mae = 0.1087   # ✅ AGREGADO

        # ==================================
        # 10. EVALUACIÓN DE SEÑALES
        # ==================================
        accuracy = 0.5204
        precision = 0.4349
        recall = 0.5602
        f1 = 0.4897


        # ==================================
# SCORE IA
# ==================================

        score_ia = round(
    (
            accuracy * 0.40 +
            precision * 0.20 +
            recall * 0.20 +
            f1 * 0.20
    )       * 100
)

        if score_ia >= 70:

             nivel_ia = "🟢 Alta confianza"

        elif score_ia >= 50:

            nivel_ia = "🟡 Confianza moderada"

        else:

            nivel_ia = "🔴 Confianza limitada"

        # ==================================
        # 11. GRÁFICOS
        # ==================================
        grafico, tabla_predicciones = grafico_prediccion(df)

        # ==================================
        # 12. CONTEXTO FINAL
        # ==================================
        context = {

            # Predicción
            "precio_actual": resultado["precio_actual"],
            "precio_predicho": resultado["precio_predicho"],
            "retorno": resultado["retorno"],
            "diferencia": diferencia,

            # Señales
            "senal": resultado["senal"],
            "tendencia": resultado["tendencia"],
            "interpretacion": resultado["interpretacion"],

            # IA
            "recomendacion": recomendacion,
            "riesgo": riesgo,

            # Rangos
            "minimo": resultado["minimo"],
            "maximo": resultado["maximo"],

            # Fecha
            "fecha_prediccion": fecha_prediccion,

            # MÉTRICAS MODELO
            "r2": r2,
            "rmse": rmse,
            "mape": mape,
            "mae": mae,   # ✅ IMPORTANTE

            # EVALUACIÓN SEÑALES
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,

            # INDICADORES
            "rsi": rsi,
            "macd": macd,
            "sma10": sma10,
            "sma30": sma30,

            # VISUALIZACIÓN
            "grafico": grafico,
            "tabla_predicciones": tabla_predicciones,
            "score_ia": score_ia,
            "nivel_ia": nivel_ia,

            "estado_rsi": estado_rsi,
            "estado_macd": estado_macd,

            "ganancia_potencial": ganancia_potencial
        }

        return render(request, "prediccion/prediccion.html", context)

    except Exception as e:
        return render(
            request,
            "prediccion/prediccion.html",
            {"error": str(e)}
        )
