
import plotly.graph_objects as go

from .lstm import predecir_historico



def grafico_prediccion(df):

    df = df.tail(200)

    fechas_pred, predicciones = predecir_historico(df)

    fechas_pred = fechas_pred[-80:]
    predicciones = predicciones[-80:]

    df_real = df[df["fecha"].isin(fechas_pred)]

    fechas_reales = df_real["fecha"]
    precios_reales = df_real["cierre"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=fechas_reales,
            y=precios_reales,
            mode="lines",
            name="Precio Real",
            line=dict(
            color="#3B82F6",
            width=3
        )
    )
)

    fig.add_trace(
     go.Scatter(
        x=fechas_pred,
        y=predicciones,
        mode="lines",
        name="Predicción IA",
        line=dict(
            color="#10B981",
            width=3,
            dash="dash"
        )
    )
)
    

    fig.add_trace(
    go.Scatter(
        x=fechas_reales,
        y=precios_reales,
        fill="tozeroy",
        fillcolor="rgba(59,130,246,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        showlegend=False
    )
)
    

    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(step="all", label="Todo")
        ])
    )
)

    fig.update_layout(
        title={
        "text": "📈 Predicción LSTM vs Precio Real",
        "x": 0.5
     },

    template="plotly_dark",

    height=650,

    paper_bgcolor="#111827",
    plot_bgcolor="#111827",

    font=dict(
        color="white",
        size=13
    ),

    hovermode="x unified",

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    xaxis=dict(
        title="Fecha",
        showgrid=True,
        gridcolor="#374151",
        zeroline=False
    ),

    yaxis=dict(
        title="Precio",
        showgrid=True,
        gridcolor="#374151",
        zeroline=False
    )
)

    tabla = []

    for fecha, real, pred in zip(
        fechas_reales,
        precios_reales,
        predicciones
        ):
    
        error = abs(float(real) - float(pred))

        tabla.append({
            "fecha": fecha.strftime("%Y-%m-%d"),
            "real": round(float(real), 2),
            "predicho": round(float(pred), 2),
            "error": round(error, 4)
    })




    return (
        fig.to_html(
            full_html=False,
            include_plotlyjs="cdn"
        ),
        tabla
    )