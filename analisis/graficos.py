import plotly.graph_objects as go


# ==========================================
# 📈 PRECIO DE CIERRE
# ==========================================

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


# ==========================================
# 📊 MEDIAS MÓVILES
# ==========================================

def grafico_medias(df):

    fig = go.Figure()

    # PRECIO
    fig.add_trace(
        go.Scatter(
            x=df["fecha"],
            y=df["cierre"],
            mode="lines",
            name="Cierre",
            line=dict(color="#3b82f6", width=2)
        )
    )

    # SMA 10
    fig.add_trace(
        go.Scatter(
            x=df["fecha"],
            y=df["sma_10"],
            mode="lines",
            name="SMA 10",
            line=dict(color="#22c55e", width=2)
        )
    )

    # SMA 30
    fig.add_trace(
        go.Scatter(
            x=df["fecha"],
            y=df["sma_30"],
            mode="lines",
            name="SMA 30",
            line=dict(color="#ef4444", width=2)
        )
    )

    fig.update_layout(
        title="Análisis de Medias Móviles",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        template="plotly_dark",
        height=500
    )

    return fig.to_html(full_html=False)


# ==========================================
# 📉 RSI
# ==========================================

def grafico_rsi(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["fecha"],
            y=df["rsi"],
            mode="lines",
            name="RSI",
            line=dict(color="#f59e0b", width=2)
        )
    )

    # SOBRECOMPRA
    fig.add_shape(
        type="line",
        x0=df["fecha"].min(),
        x1=df["fecha"].max(),
        y0=70,
        y1=70,
        line=dict(color="red", dash="dash")
    )

    

    # SOBREVENTA
    fig.add_shape(
        type="line",
        x0=df["fecha"].min(),
        x1=df["fecha"].max(),
        y0=30,
        y1=30,
        line=dict(color="green", dash="dash")
    )

    fig.update_layout(
        title="Indicador RSI",
        xaxis_title="Fecha",
        yaxis_title="RSI",
        template="plotly_dark",
        height=400
    )

    return fig.to_html(full_html=False)


# ==========================================
# 📊 MACD
# ==========================================

def grafico_macd(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["fecha"],
            y=df["macd"],
            mode="lines",
            name="MACD",
            line=dict(color="#a855f7", width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["fecha"],
            y=df["signal"],
            mode="lines",
            name="Signal",
            line=dict(color="#f59e0b", width=2)
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["fecha"],
            y=df["histograma"],
            name="Histograma"
        )
    )

    fig.update_layout(
        title="Indicador MACD",
        xaxis_title="Fecha",
        yaxis_title="MACD",
        template="plotly_dark",
        height=400
    )

    return fig.to_html(full_html=False)