from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required

import pandas as pd
from sqlalchemy import create_engine, text

from .preprocessing import limpiar_datos
from .graficos import grafico_cierre
from .models import Empresa
from django.http import FileResponse
import os


@login_required
def cargar_datos(request):

    datos_original = None
    cantidad_registros = None
    cantidad_columnas = None
    grafico = None
    error = None
    reporte = None
    ruta_excel = None

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

            print(df_raw.columns.tolist())


            # ==========================
# ADAPTAR CSV DE LA BVL
# ==========================

            df_raw.columns = df_raw.columns.str.strip()

            df_raw.rename(columns={
                 'Fecha de cotización': 'Fecha',
                 'Fecha de cotizaciÃ³n': 'Fecha',

                 'Máximo': 'Maximo',
                 'MÃ¡ximo': 'Maximo',

                 'Mínimo': 'Minimo',
                 'MÃ­nimo': 'Minimo',

                 'Cantidad negociada': 'Volumen'
                    }, inplace=True)

# Conservar solo las columnas necesarias
            df_raw = df_raw[
                 [
                  'Fecha',
                  'Apertura',
                  'Cierre',
                  'Maximo',
                  'Minimo',
                  'Volumen'
    ]
]


            # ====================================
            # 🧼 LIMPIAR DATOS
            # ====================================

            df_clean, reporte = limpiar_datos(df_raw)


            df_clean['fecha'] = pd.to_datetime(
                    df_clean['fecha'],
                    errors='coerce'
)

            df_clean = df_clean.sort_values(
                    by='fecha',
                    ascending=False
)




            ruta_excel = f"media/dataset_limpio_{request.user.id}.xlsx"

            df_clean.to_excel(
                ruta_excel,
                index=False
)


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
# 📅 ORDENAR POR FECHA MÁS RECIENTE
# ====================================

            df_db = df_db.sort_values(
                 by='fecha',
                 ascending=False
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

            request.session["datos_cargados"] = True

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

        

            'ruta_excel': ruta_excel if dataset_limpio else None,


        }
    )




@login_required
def descargar_dataset_limpio(request):

    archivo = f"media/dataset_limpio_{request.user.id}.xlsx"

    if os.path.exists(archivo):

        return FileResponse(
            open(archivo, 'rb'),
            as_attachment=True,
            filename='dataset_limpio.xlsx'
        )

    return redirect('cargar_datos')