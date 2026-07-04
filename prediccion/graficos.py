import plotly.graph_objects as go

from .lstm import predecir_historico



def grafico_prediccion(df):

    # últimos datos para visualización
    df = df.tail(200).copy()


    fechas_pred, predicciones = predecir_historico(df)


    fechas_pred = fechas_pred[-80:]
    predicciones = predicciones[-80:]


    df_real = df[
        df["fecha"].isin(fechas_pred)
    ]


    fechas_reales = df_real["fecha"]

    precios_reales = df_real["cierre"]



    fig = go.Figure()



    # ==========================
    # PRECIO REAL
    # ==========================

    fig.add_trace(

        go.Scatter(

            x=fechas_reales,

            y=precios_reales,

            mode="lines+markers",

            name="Precio Real",

            line=dict(
                width=3
            ),

            marker=dict(
                size=5
            ),

            hovertemplate=
            "<b>Fecha:</b> %{x}<br>" +
            "<b>Precio:</b> S/ %{y:.2f}<extra></extra>"

        )

    )



    # ==========================
    # PREDICCION IA
    # ==========================

    fig.add_trace(

        go.Scatter(

            x=fechas_pred,

            y=predicciones,

            mode="lines+markers",

            name="Predicción IA",

            line=dict(

                width=3,

                dash="dash"

            ),

            marker=dict(

                size=6

            ),

            hovertemplate=

            "<b>Fecha:</b> %{x}<br>" +

            "<b>IA:</b> S/ %{y:.2f}<extra></extra>"

        )

    )



    # ==========================
    # PUNTO ACTUAL
    # ==========================

    fig.add_trace(

        go.Scatter(

            x=[fechas_reales.iloc[-1]],

            y=[precios_reales.iloc[-1]],

            mode="markers",

            name="Último precio",

            marker=dict(

                size=12

            ),

            hovertemplate=

            "<b>Precio Actual</b><br>" +

            "S/ %{y:.2f}<extra></extra>"

        )

    )



    # ==========================
    # DISEÑO
    # ==========================

    fig.update_layout(

        title={

            "text":
            "🤖 Modelo LSTM - Precio Real vs Predicción IA",

            "x":0.5

        },


        template="plotly_dark",


        height=520,


        margin=dict(

            l=40,

            r=40,

            t=70,

            b=40

        ),


        paper_bgcolor="#111827",

        plot_bgcolor="#111827",


        font=dict(

            color="white",

            size=12

        ),



        hovermode="x unified",



        legend=dict(

            orientation="h",

            y=1.10,

            x=0.5,

            xanchor="center"

        ),



        xaxis=dict(

            title="Fecha",

            showgrid=True,

            gridcolor="#374151"

        ),



        yaxis=dict(

            title="Precio (S/)",

            showgrid=True,

            gridcolor="#374151"

        )

    )



    # ==========================
    # TABLA PARA EXCEL / HTML
    # ==========================

    tabla = []


    for fecha, real, pred in zip(

        fechas_reales,

        precios_reales,

        predicciones

    ):


        error = abs(

            float(real)-float(pred)

        )


        tabla.append({

            "fecha":

            fecha.strftime("%Y-%m-%d"),


            "real":

            round(float(real),2),


            "predicho":

            round(float(pred),2),


            "error":

            round(error,4)

        })



    return (

        fig.to_html(

            full_html=False,

            include_plotlyjs="cdn"

        ),

        tabla

    )