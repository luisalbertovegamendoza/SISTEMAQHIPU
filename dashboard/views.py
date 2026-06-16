from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cargar.utils import usuario_tiene_datos
from django.shortcuts import redirect, render
from django.contrib import messages

import pandas as pd

from cargar.models import StockData

from prediccion.predictores import predecir_manana
from prediccion.graficos import grafico_prediccion
from prediccion.indicadores_ia import agregar_indicadores
from datetime import datetime


@login_required
def dashboard(request):
    if not usuario_tiene_datos(request.user):

        messages.warning(
            request,
            "Primero debe cargar datos históricos."
        )

        return redirect("cargar")
    

    try:

        datos = list(
            StockData.objects
            .filter(usuario=request.user)
            .order_by("fecha")
            .values(
                "fecha",
                "apertura",
                "cierre",
                "maximo",
                "minimo",
                "volumen"
            )
        )

        df = pd.DataFrame.from_records(datos)

        if df.empty:
            raise ValueError("No existen datos cargados.")

        df["fecha"] = pd.to_datetime(df["fecha"])

        df = agregar_indicadores(df)

        df = df.dropna()

        resultado = predecir_manana(df)

        grafico, _ = grafico_prediccion(df)

        rsi = round(float(df["rsi"].iloc[-1]), 2)
        macd = round(float(df["macd"].iloc[-1]), 4)
        sma10 = round(float(df["sma_10"].iloc[-1]), 2)
        sma30 = round(float(df["sma_30"].iloc[-1]), 2)


        fecha_prediccion = datetime.now().strftime("%d/%m/%Y %H:%M")

        ganancia_potencial = round(
            resultado["precio_predicho"] -
            resultado["precio_actual"],
                 2
            )

        retorno_abs = abs(resultado["retorno"])

        if retorno_abs < 2:
            riesgo = "🟢 Bajo"

        elif retorno_abs < 5:
            riesgo = "🟡 Moderado"

        else:
            riesgo = "🔴 Alto"

        accuracy = 0.5204
        precision = 0.4349
        recall = 0.5602
        f1 = 0.4897


# Score simple
        score_ia = round(
(
            accuracy * 0.40 +
            precision * 0.20 +
            recall * 0.20 +
            f1 * 0.20
        )       * 100
)

        if score_ia >= 70:
             nivel_ia = "Alta"

        elif score_ia >= 50:
             nivel_ia = "Moderada"

        else:
             nivel_ia = "Limitada"


        context = {

            "precio_actual": resultado["precio_actual"],
            "precio_predicho": resultado["precio_predicho"],
             "retorno": resultado["retorno"],
            "senal": resultado["senal"],

            "rsi": rsi,
            "macd": macd,
            "sma10": sma10,
            "sma30": sma30,

            "score_ia": score_ia,
            "nivel_ia": nivel_ia,
            "riesgo": riesgo,
            "ganancia_potencial": ganancia_potencial,
            "fecha_prediccion": fecha_prediccion,

            "grafico": grafico,
}

        return render(
            request,
            "dashboard/dashboard.html",
            context
        )

    except Exception as e:

        return render(
            request,
            "dashboard/dashboard.html",
            {"error": str(e)}
        )
    



