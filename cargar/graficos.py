import plotly.graph_objects as go

def grafico_cierre(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["fecha"],
            y=df["cierre"],
            mode="lines",
            name="Cierre",
            line=dict(color="#3b82f6", width=2)
        )
    )

    fig.update_layout(
        title="Precio de Cierre",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        template="plotly_dark",
        height=500
    )

    return fig.to_html(full_html=False)