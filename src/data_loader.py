from __future__ import annotations

import pandas as pd
import yfinance as yf


def get_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    data = yf.download(
        ticker,
        period=period,
        auto_adjust=False,
        progress=False,
        group_by="column",
    )

    if data is None or data.empty:
        return pd.DataFrame()

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.copy()
    data.columns = [str(col).title() for col in data.columns]

    expected_cols = ["Open", "High", "Low", "Close", "Volume"]
    keep_cols = [col for col in expected_cols if col in data.columns]
    data = data[keep_cols]

    data = data.dropna(subset=["Close"]).copy()

    if "Volume" in data.columns:
        data["Volume"] = pd.to_numeric(data["Volume"], errors="coerce").fillna(0)

    for col in ["Open", "High", "Low", "Close"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=["Close"]).copy()

    return data


def get_stock_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)

    try:
        info = stock.info or {}
    except Exception:
        info = {}

    return {
        "longName": info.get("longName", ticker),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "marketCap": info.get("marketCap"),
        "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
    }