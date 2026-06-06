from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd

from cargar.models import StockData

from .predictores import predecir_manana
from .graficos import grafico_prediccion
from .indicadores_ia import agregar_indicadores


@login_required
def prediccion_ia(request):

    try:

        # =========================
        # 1. CARGA DE DATOS
        # =========================
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
            raise ValueError("No hay datos cargados.")

        # =========================
        # 2. LIMPIEZA
        # =========================
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

        numeric_cols = ['apertura', 'cierre', 'maximo', 'minimo', 'volumen']

        df[numeric_cols] = df[numeric_cols].apply(
            pd.to_numeric,
            errors='coerce'
        )

        df = df.dropna(subset=['fecha', 'cierre'])
        df = df.sort_values('fecha')

        # =========================
        # 3. INDICADORES
        # =========================
        df = agregar_indicadores(df)

        
        # 🔥 IMPORTANTE: limpiar NaN de indicadores
        df = df.dropna()

        df = df.reset_index(drop=True)

        if len(df) < 60:
            raise ValueError("No hay suficientes datos después de indicadores.")

        # =========================
# INDICADORES ACTUALES
# =========================

        rsi = round(
            float(df["rsi"].iloc[-1]),
             2
                )

        macd = round(
             float(df["macd"].iloc[-1]),
             4
                )

        sma10 = round(
            float(df["sma_10"].iloc[-1]),
             2
                )

        sma30 = round(
             float(df["sma_30"].iloc[-1]),
             2
                )



        # =========================
        # 4. PREDICCIÓN
        # =========================
        resultado = predecir_manana(df)

        # =========================
        # 5. GRÁFICO
        # =========================

        grafico = grafico_prediccion(df)
        
        # =========================
        # 6. CONTEXTO
        # =========================

        context = {

                 "precio_actual": resultado["precio_actual"],

                "precio_predicho": resultado["precio_predicho"],

                "retorno": resultado["retorno"],

                "tendencia": resultado["tendencia"],

                 "interpretacion": resultado["interpretacion"],

                 "senal": resultado["senal"],

                 "minimo": resultado["minimo"],

                 "maximo": resultado["maximo"],

                "confianza": resultado["confianza"],

                "rsi": rsi,

                 "macd": macd,

                "sma10": sma10,

                "sma30": sma30,

                "grafico": grafico
                }
       

        return render(
            request,
            "prediccion/prediccion.html",
            context
        )

    except Exception as e:

        return render(
            request,
            "prediccion/prediccion.html",
            {"error": str(e)}
        )