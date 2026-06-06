import plotly.graph_objects as go

from .lstm import predecir_historico


def grafico_prediccion(df):

    fechas_pred, predicciones = predecir_historico(df)

    fechas_reales = df["fecha"].iloc[
        len(df)-len(predicciones):
    ]

    precios_reales = df["cierre"].iloc[
        len(df)-len(predicciones):
    ]

    fig = go.Figure()

    # REAL

    fig.add_trace(

        go.Scatter(

            x=fechas_reales,

            y=precios_reales,

            mode="lines",

            name="Real"
        )
    )

    # PREDICCIÓN

    fig.add_trace(

        go.Scatter(

            x=fechas_pred,

            y=predicciones,

            mode="lines",

            name="Predicción LSTM"
        )
    )

    fig.update_layout(

        title="Valores Reales vs Predicción",

        xaxis_title="Fecha",

        yaxis_title="Precio",

        hovermode="x unified",

        template="plotly_white",

        height=600
    )

    return fig.to_html(

        full_html=False,

        include_plotlyjs="cdn"
    )