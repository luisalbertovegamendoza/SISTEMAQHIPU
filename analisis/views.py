from django.contrib.auth.decorators import login_required
from cargar.utils import usuario_tiene_datos
from django.contrib import messages
from django.shortcuts import redirect, render


import pandas as pd

from cargar.models import StockData
from .indicadores import agregar_indicadores
from .graficos import (
    grafico_medias,
    grafico_rsi,
    grafico_macd
)






@login_required
def analisis_tecnico(request):
    if not usuario_tiene_datos(request.user):

        messages.warning(
            request,
            "Primero debe cargar datos históricos."
        )

        return redirect("cargar")
    

    tabla_indicadores = None
    grafico_sma = None
    grafico_rsi_html = None
    grafico_macd_html = None

    cantidad_registros = 0
    cantidad_columnas = 0
    error = None

    try:

        # =========================
        # 📂 1. CARGAR DATOS DESDE POSTGRESQL
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

        print("🔥 RAW DB:", df.shape)

        if df.empty:
            raise ValueError("Primero debe cargar un archivo CSV")

        # =========================
        # 🔧 2. LIMPIEZA MÍNIMA (SIN DUPLICAR PROCESOS)
        # =========================

        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

        numeric_cols = [
            'apertura',
            'cierre',
            'maximo',
            'minimo',
            'volumen'
        ]

        df[numeric_cols] = df[numeric_cols].apply(
            pd.to_numeric,
            errors='coerce'
        )

        df = df.dropna(subset=['fecha', 'cierre'])
        df = df.sort_values('fecha')

        print("📊 DESPUÉS LIMPIEZA:", df.shape)

        if df.empty:
            raise ValueError("Datos vacíos después de limpieza")

        # =========================
        # 📊 3. INDICADORES (PIPELINE OFICIAL ÚNICO)
        # =========================

        df = agregar_indicadores(df)

        # reset para IA futura (IMPORTANTE)
        df = df.copy()
        df.reset_index(drop=True, inplace=True)

        print("📈 DESPUÉS INDICADORES:", df.shape)

        if df.empty:
            raise ValueError("DataFrame vacío después de indicadores")

        # =========================
        # 📈 4. GRÁFICOS
        # =========================

        grafico_sma = grafico_medias(df)
        grafico_rsi_html = grafico_rsi(df)
        grafico_macd_html = grafico_macd(df)

        # =========================
        # 📄 5. TABLA INDICADORES (ULTIMOS 30 REGISTROS)
        # =========================

        columnas_tabla = [
            'fecha',
            'cierre',
            'sma_10',
            'sma_30',
            'ema_10',
            'rsi',
            'macd',
            'signal',
            'histograma',
            'volatilidad'
        ]

        columnas_existentes = [
            c for c in columnas_tabla
            if c in df.columns
        ]

        df = df.round(4)

        tabla_indicadores = (
            df[columnas_existentes]
            .tail(30)
            .to_html(
                classes='table table-dark table-striped',
                index=False
            )
        )

        # =========================
        # 📊 6. KPIs
        # =========================

        cantidad_registros = df.shape[0]
        cantidad_columnas = df.shape[1]

    except Exception as e:
        error = str(e)
        print("❌ ERROR ANALISIS:", error)

    return render(
        request,
        'analisis/analisis_tecnico.html',
        {
            'tabla_indicadores': tabla_indicadores,
            'grafico_sma': grafico_sma,
            'grafico_rsi': grafico_rsi_html,
            'grafico_macd': grafico_macd_html,
            'cantidad_registros': cantidad_registros,
            'cantidad_columnas': cantidad_columnas,
            'error': error,
        }
    )

