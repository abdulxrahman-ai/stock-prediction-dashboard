from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_prices(df: pd.DataFrame, forecast_days: int = 7) -> pd.DataFrame:
    if df.empty or "Close" not in df.columns:
        return pd.DataFrame(columns=["Date", "PredictedClose"])

    closes = df["Close"].dropna().copy()

    if len(closes) < 10:
        future_dates = pd.date_range(
            start=df.index[-1] + pd.Timedelta(days=1),
            periods=forecast_days,
            freq="B",
        )
        last_close = float(closes.iloc[-1]) if len(closes) else 0.0
        return pd.DataFrame(
            {
                "Date": future_dates,
                "PredictedClose": [last_close] * forecast_days,
            }
        )

    work = pd.DataFrame({"Close": closes})
    work["Lag1"] = work["Close"].shift(1)
    work["Lag2"] = work["Close"].shift(2)
    work["Lag3"] = work["Close"].shift(3)
    work = work.dropna()

    X = work[["Lag1", "Lag2", "Lag3"]]
    y = work["Close"]

    model = LinearRegression()
    model.fit(X, y)

    last_values = list(closes.iloc[-3:].values)
    predictions = []

    for _ in range(forecast_days):
        x_next = pd.DataFrame(
            [[last_values[-1], last_values[-2], last_values[-3]]],
            columns=["Lag1", "Lag2", "Lag3"],
        )
        next_pred = float(model.predict(x_next)[0])
        predictions.append(next_pred)
        last_values.append(next_pred)

    future_dates = pd.date_range(
        start=df.index[-1] + pd.Timedelta(days=1),
        periods=forecast_days,
        freq="B",
    )

    return pd.DataFrame(
        {
            "Date": future_dates,
            "PredictedClose": predictions,
        }
    )