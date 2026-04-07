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

# 🔥 UPDATED VISUAL CSS (SAFE VERSION)
st.markdown("""
<style>

/* Smooth scroll */
html { scroll-behavior: smooth; }

/* ===== AMBIENT BACKGROUND (SAFE) ===== */
[data-testid="stAppViewContainer"] {
    position: relative;
    overflow: hidden;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(circle at 20% 25%, rgba(59,130,246,0.08), transparent 25%),
        radial-gradient(circle at 80% 20%, rgba(14,165,233,0.07), transparent 22%),
        radial-gradient(circle at 70% 80%, rgba(56,189,248,0.05), transparent 20%);
    filter: blur(40px);
    animation: floatLights 18s ease-in-out infinite alternate;
}

/* Keep content above */
.block-container { position: relative; z-index: 1; }

/* ===== ANIMATIONS ===== */
.fade-up {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeUp 0.7s ease forwards;
}

.fade-delay-1 { animation-delay: 0.08s; }
.fade-delay-2 { animation-delay: 0.16s; }
.fade-delay-3 { animation-delay: 0.24s; }
.fade-delay-4 { animation-delay: 0.32s; }
.fade-delay-5 { animation-delay: 0.40s; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes floatLights {
    0% { transform: translate(0px,0px); }
    50% { transform: translate(20px,-10px); }
    100% { transform: translate(-15px,15px); }
}

/* ===== GLASS EFFECT ===== */
.hero-shell,
.kpi-strip,
.chart-panel,
.summary-card,
.table-panel,
.about-panel {
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

/* ===== HOVER ===== */
.summary-card:hover,
.chart-panel:hover,
.table-panel:hover,
.about-panel:hover,
.hero-shell:hover,
.kpi-strip:hover {
    transform: translateY(-2px);
}

/* ===== BUTTON GLOW ===== */
div[data-testid="stButton"] button {
    transition: all 0.3s ease !important;
    box-shadow: 0 0 12px rgba(59,130,246,0.15);
}

div[data-testid="stButton"] button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 0 20px rgba(59,130,246,0.3),
        0 0 30px rgba(34,211,238,0.15);
}

/* ===== DARK MODE ===== */
@media (prefers-color-scheme: dark) {
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #0b1220 !important;
        color: #e5e7eb !important;
    }

    .hero-shell,
    .kpi-strip,
    .chart-panel,
    .summary-card,
    .table-panel,
    .about-panel {
        background: rgba(17,24,39,0.85) !important;
        border-color: #243041 !important;
        box-shadow:
            0 10px 30px rgba(0,0,0,0.35),
            0 0 20px rgba(59,130,246,0.05) !important;
    }
}

/* ===== LIGHT MODE ===== */
@media (prefers-color-scheme: light) {
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #f8fafc !important;
    }

    .hero-shell,
    .kpi-strip,
    .chart-panel,
    .summary-card,
    .table-panel,
    .about-panel {
        background: rgba(255,255,255,0.8) !important;
        box-shadow:
            0 10px 25px rgba(0,0,0,0.05),
            0 0 10px rgba(59,130,246,0.05) !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ===== REST OF YOUR CODE (UNCHANGED) =====

DARK_MODE = st.context.theme and st.context.theme.type == "dark"

def apply_plotly_theme(fig, dark_mode=False):
    if dark_mode:
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    else:
        fig.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0)")
    return fig

@st.dialog("Contact Abdul")
def show_contact_dialog():
    st.markdown("**Email:** abdulxrahman.ai@gmail.com")
    st.markdown("**Phone:** +1 (773) 996-2993")

st.markdown("""
<div class="hero-shell fade-up fade-delay-1">
<div class="hero-title">AI Stock Prediction + News Sentiment Dashboard</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns([2,2,2,3,2])

with c1:
    ticker = st.text_input("Ticker","AAPL")

with c2:
    period = st.selectbox("History Period",["6mo","1y","2y"],index=1)

with c3:
    forecast_days = st.slider("Forecast Days",1,30,7)

with c4:
    uploaded_file = st.file_uploader("Upload Screenshot")

with c5:
    run = st.button("Run Analysis",use_container_width=True)
    contact = st.button("Contact Abdul",use_container_width=True)

if contact:
    show_contact_dialog()

if run:
    df = get_stock_data(ticker, period)

    if df is None or df.empty:
        st.error("No data found.")
        st.stop()

    df = add_indicators(df)
    forecast_df = forecast_prices(df, forecast_days)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close"))
    fig = apply_plotly_theme(fig, DARK_MODE)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="about-panel fade-up fade-delay-5">
<div class="about-title">ABOUT PROJECT</div>
</div>
""", unsafe_allow_html=True)
