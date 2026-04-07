import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.data_loader import get_stock_data, get_stock_info
from src.indicators import add_indicators
from src.forecasting import forecast_prices
from src.news_fetcher import get_news
from src.sentiment import analyze_news_sentiment
from src.utils import format_large_number, format_price

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

with open("assets/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.dialog("Contact Abdul")
def show_contact_dialog():
    st.markdown("**Email:** abdulxrahman.ai@gmail.com")
    st.markdown("**Phone:** +1 (773) 996-2993")
    st.markdown("**GitHub:** [View Profile](https://github.com/abdulxrahman-ai)")

st.markdown(
    """
    <div class="hero-shell">
        <div class="eyebrow">NEXT-GEN MARKET INTELLIGENCE</div>
        <div class="hero-title">AI Stock Prediction + News Sentiment Dashboard</div>
        <div class="hero-subtitle">
            Professional market review workspace for price trend analysis, short-term forecasting,
            news sentiment monitoring, and optional candlestick screenshot interpretation with High-accuracy models.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
# ✅ DISCLAIMER FIRST
st.markdown(
"""
<div style="
background: #fef2f2;
border: 1px solid #fecaca;
color: #991b1b;
padding: 0.9rem 1.1rem;
border-radius: 14px;
font-size: 0.92rem;
margin-top: 1rem;
margin-bottom: 0.5rem;
line-height: 1.6;
">
<strong>Disclaimer:</strong> This tool provides analytical insights and should not be considered financial advice.
Always consult a qualified financial advisor before making investment decisions.
</div>
""",
unsafe_allow_html=True
)

# ✅ NOTE SECOND
st.markdown(
"""
<div style="
background: #fff7ed;
border: 1px solid #fed7aa;
color: #9a3412;
padding: 0.9rem 1.1rem;
border-radius: 14px;
font-size: 0.95rem;
margin-top: 0.5rem;
margin-bottom: 0.6rem;
">
<strong>Note:</strong> Analysis works when Stock Name is entered in Ticker NOT the Company Name.
</div>
""",
unsafe_allow_html=True
)
st.markdown('<div class="section-label">ANALYSIS CONTROLS</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 3, 2])

with c1:
    ticker = st.text_input("Ticker", "AAPL")

with c2:
    period = st.selectbox("History Period", ["6mo", "1y", "2y"], index=1)

with c3:
    forecast_days = st.slider("Forecast Days", 1, 30, 7)

with c4:
    uploaded_file = st.file_uploader("Upload Candlestick Screenshot (optional)")

with c5:
    st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)
    run = st.button("Run Analysis", use_container_width=True)
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    contact = st.button("Contact Abdul", use_container_width=True)

if contact:
    show_contact_dialog()

if run:
    df = get_stock_data(ticker, period)

    if df is None or df.empty:
        st.error("No data found.")
        st.stop()

    df = add_indicators(df)
    info = get_stock_info(ticker)

    news_df = get_news(ticker)
    news_df, avg_sentiment, sentiment_counts = analyze_news_sentiment(news_df)

    forecast_df = forecast_prices(df, forecast_days)

    latest = df.iloc[-1]

    current_price = float(latest["Close"])
    volume = float(latest["Volume"])
    daily_change = (
        (float(df["Close"].iloc[-1]) - float(df["Close"].iloc[-2]))
        / float(df["Close"].iloc[-2])
        * 100
        if len(df) > 1
        else 0.0
    )

    ma20 = float(latest["MA20"]) if "MA20" in df.columns and not pd.isna(latest["MA20"]) else 0.0
    ma50 = float(latest["MA50"]) if "MA50" in df.columns and not pd.isna(latest["MA50"]) else 0.0
    rsi = float(latest["RSI"]) if "RSI" in df.columns and not pd.isna(latest["RSI"]) else 0.0
    volatility = float(df["Close"].pct_change().std()) if len(df) > 1 else 0.0

    bullish = 0
    bearish = 0

    if current_price > ma20:
        bullish += 1
    else:
        bearish += 1

    if ma20 > ma50:
        bullish += 1
    else:
        bearish += 1

    if avg_sentiment > 0.05:
        bullish += 1
    elif avg_sentiment < -0.05:
        bearish += 1

    if bullish > bearish:
        signal = "Bullish"
        signal_class = "bullish"
    elif bearish > bullish:
        signal = "Bearish"
        signal_class = "bearish"
    else:
        signal = "Neutral"
        signal_class = "neutral"

    st.markdown(f"""<div class="kpi-strip">

<div class="kpi-item">
    <div class="kpi-label">CURRENT PRICE</div>
    <div class="kpi-value">{format_price(current_price)}</div>
</div>

<div class="kpi-divider"></div>

<div class="kpi-item">
    <div class="kpi-label">DAILY CHANGE</div>
    <div class="kpi-value">{daily_change:.2f}%</div>
</div>

<div class="kpi-divider"></div>

<div class="kpi-item">
    <div class="kpi-label">VOLUME</div>
    <div class="kpi-value">{format_large_number(volume)}</div>
</div>

<div class="kpi-divider"></div>

<div class="kpi-item">
    <div class="kpi-label">SIGNAL</div>
    <div class="kpi-value {signal_class}">{signal}</div>
</div>

<div class="kpi-divider"></div>

<div class="kpi-item">
    <div class="kpi-label">AVERAGE SENTIMENT</div>
    <div class="kpi-value">{avg_sentiment:.3f}</div>
</div>

</div>
""", unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close"))
    fig.add_trace(go.Scatter(x=df.index, y=df["MA20"], name="MA20"))
    fig.add_trace(go.Scatter(x=df.index, y=df["MA50"], name="MA50"))
    st.plotly_chart(fig, use_container_width=True)

    if not forecast_df.empty:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Forecast</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-subtitle">Short-term directional support layer based on recent price behavior.</div>',
            unsafe_allow_html=True,
        )

        ffig = go.Figure()
        recent_df = df.tail(40)
        ffig.add_trace(go.Scatter(x=recent_df.index, y=recent_df["Close"], name="Recent Close"))
        ffig.add_trace(
            go.Scatter(
                x=forecast_df["Date"],
                y=forecast_df["PredictedClose"],
                name="Predicted Close",
                mode="lines+markers",
            )
        )
        st.plotly_chart(ffig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Key Stats</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="data-list">
                <div><span>Sector</span><strong>{info.get('sector', 'N/A')}</strong></div>
                <div><span>Industry</span><strong>{info.get('industry', 'N/A')}</strong></div>
                <div><span>Market Cap</span><strong>{format_large_number(info.get('marketCap', 0))}</strong></div>
                <div><span>52W High</span><strong>{info.get('fiftyTwoWeekHigh', 'N/A')}</strong></div>
                <div><span>52W Low</span><strong>{info.get('fiftyTwoWeekLow', 'N/A')}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Technical Snapshot</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="data-list">
                <div><span>RSI (14)</span><strong>{rsi:.2f}</strong></div>
                <div><span>20-Day MA</span><strong>{ma20:.2f}</strong></div>
                <div><span>50-Day MA</span><strong>{ma50:.2f}</strong></div>
                <div><span>Volatility</span><strong>{volatility:.4f}</strong></div>
                <div><span>Close vs MA20</span><strong>{(current_price - ma20):.2f}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">News Sentiment Summary</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="data-list">
                <div><span>Average Sentiment</span><strong>{avg_sentiment:.3f}</strong></div>
                <div><span>Market Mood</span><strong class="{signal_class}">{signal}</strong></div>
                <div><span>Positive</span><strong>{sentiment_counts.get('Positive', 0)}</strong></div>
                <div><span>Neutral</span><strong>{sentiment_counts.get('Neutral', 0)}</strong></div>
                <div><span>Negative</span><strong>{sentiment_counts.get('Negative', 0)}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if not news_df.empty:
        st.markdown('<div class="table-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Latest News & Sentiment</div>', unsafe_allow_html=True)
        news_display = news_df.copy()
        if "URL" in news_display.columns:
            news_display = news_display.drop(columns=["URL"])
        st.dataframe(news_display, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="about-panel">

<div class="about-title">ABOUT PROJECT</div>

<div class="about-text">
An AI-powered market intelligence system designed to analyze stock price behavior,
generate short-term forecasts, and interpret market sentiment using real-time news data.
</div>

<div class="about-subtitle">Core Capabilities</div>
<div class="about-bullet">Time-series forecasting for short-term price trends</div>
<div class="about-bullet"> Technical indicator analysis (RSI, Moving Averages, Volatility)</div>
<div class="about-bullet"> Real-time news sentiment classification using NLP</div>
<div class="about-bullet"> Integrated signal generation (Bullish / Bearish / Neutral)</div>

<div class="about-subtitle">Technology Stack</div>
<div class="about-bullet"> Python, Streamlit, Pandas, Plotly</div>
<div class="about-bullet"> Scikit-learn for predictive modeling</div>
<div class="about-bullet"> yFinance for market data extraction</div>
<div class="about-bullet"> NLP (VADER) for sentiment analysis</div>

<div class="about-subtitle">How It Works</div>
<div class="about-text">
It combines historical price dynamics, technical indicators and sentiment intelligence. The platform delivers short-term market forecasts with structured and data-driven analytical perspective.
</div>

</div>
""", unsafe_allow_html=True)