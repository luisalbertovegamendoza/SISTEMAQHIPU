from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import pandas as pd
from sqlalchemy import create_engine, text

from .preprocessing import limpiar_datos
from .graficos import grafico_cierre
from .models import Empresa


@login_required
def cargar_datos(request):

    datos_original = None
    cantidad_registros = None
    cantidad_columnas = None
    grafico = None
    error = None
    reporte = None

    dataset_limpio = False

    if request.method == 'POST':

        try:

            archivo = request.FILES['archivo']

            # ====================================
            # 📦 LEER CSV
            # ====================================

            df_raw = pd.read_csv(
                archivo,
                sep=';',
                encoding='utf-8-sig'
            )

            # ====================================
            # 🧼 LIMPIAR DATOS
            # ====================================

            df_clean, reporte = limpiar_datos(df_raw)

            # ====================================
            # 📊 PREPARAR DATAFRAME
            # ====================================

            df_db = df_clean.copy()

            df_db = df_db.rename(columns={

                'Fecha': 'fecha',

                'Apertura': 'apertura',

                'Cierre': 'cierre',

                'Maximo': 'maximo',

                'Minimo': 'minimo',

                'Volumen': 'volumen',

            })

            # ====================================
            # 📅 FECHA
            # ====================================

            df_db['fecha'] = pd.to_datetime(
                df_db['fecha'],
                errors='coerce'
            )

            # ====================================
            # 🧹 LIMPIEZA FINAL
            # ====================================

            # eliminar solo filas críticas
            df_db.dropna(
            subset=[
                    'fecha',
                     'apertura',
                    'cierre',
                     'maximo',
                     'minimo',
                     'volumen'
    ],
             inplace=True
                )

            df_db.drop_duplicates(inplace=True)
            # ====================================
            # 👤 USUARIO
            # ====================================

            # 👤 USUARIO
            df_db['usuario_id'] = request.user.id

# 🏢 EMPRESA
            empresa = Empresa.objects.first()

            if not empresa:
                    raise ValueError(
                          "No existe ninguna empresa registrada en la tabla Empresa"
                )

            df_db['empresa_id'] = empresa.id
           








            # ====================================
            # ⏰ FECHA CREACIÓN
            # ====================================

            df_db['created_at'] = pd.Timestamp.now()

            # ====================================
            # 🔥 CONEXIÓN POSTGRESQL
            # ====================================

            engine = create_engine(
                'postgresql://postgres:12345678@localhost:5432/ferreycorp'
            )

            # ====================================
            # 🗑 BORRAR SOLO DATOS DEL USUARIO
            # ====================================

            with engine.begin() as conn:

                conn.execute(
                    text("""
                        DELETE FROM cargar_stockdata
                        WHERE usuario_id = :usuario_id
                    """),
                    {
                        "usuario_id": request.user.id
                    }
                )

            # ====================================
            # 💾 GUARDAR EN POSTGRESQL
            # ====================================

            df_db.to_sql(
                'cargar_stockdata',
                engine,
                if_exists='append',
                index=False
            )

            print("✅ DATOS GUARDADOS EN POSTGRESQL")

            # ====================================
            # 📈 GRÁFICO
            # ====================================


            grafico = grafico_cierre(df_db)

            # ====================================
            # 📋 TABLA HTML
            # ====================================

            datos_original = df_clean.head(20).to_html(
                classes='table table-dark table-striped',
                index=False
            )

            # ====================================
            # 📊 INFORMACIÓN DATASET
            # ====================================

            cantidad_registros = df_clean.shape[0]

            cantidad_columnas = df_clean.shape[1]

            dataset_limpio = True

        except Exception as e:

            print("❌ ERROR GENERAL:", e)

            error = str(e)

            dataset_limpio = False

    return render(
        request,
        'cargar/cargar_datos.html',
        {

            'datos_original': datos_original,

            'grafico': grafico,

            'cantidad_registros': cantidad_registros,

            'cantidad_columnas': cantidad_columnas,

            'error': error,

            'dataset_limpio': dataset_limpio,

            'reporte': reporte,

        }
    )