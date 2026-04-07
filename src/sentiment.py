from __future__ import annotations

from collections import Counter

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_news_sentiment(news_df: pd.DataFrame):
    if news_df.empty:
        empty = news_df.copy()
        return empty, 0.0, {"Positive": 0, "Neutral": 0, "Negative": 0}

    analyzer = SentimentIntensityAnalyzer()
    out = news_df.copy()

    sentiments = []
    scores = []

    for headline in out["Headline"].fillna(""):
        score = analyzer.polarity_scores(str(headline))["compound"]
        scores.append(score)

        if score >= 0.05:
            sentiments.append("Positive")
        elif score <= -0.05:
            sentiments.append("Negative")
        else:
            sentiments.append("Neutral")

    out["Sentiment"] = sentiments
    out["Score"] = scores

    avg_sentiment = float(out["Score"].mean()) if not out.empty else 0.0
    counts = Counter(out["Sentiment"])

    sentiment_counts = {
        "Positive": counts.get("Positive", 0),
        "Neutral": counts.get("Neutral", 0),
        "Negative": counts.get("Negative", 0),
    }

    preferred_cols = ["Published", "Headline", "Source", "Sentiment", "Score", "URL"]
    existing_cols = [c for c in preferred_cols if c in out.columns]
    out = out[existing_cols]

    return out, avg_sentiment, sentiment_counts