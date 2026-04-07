from __future__ import annotations

import datetime as dt
from urllib.parse import quote_plus

import feedparser
import pandas as pd


def get_news(ticker: str, company_name: str | None = None) -> pd.DataFrame:
    query_parts = [ticker]
    if company_name and company_name != ticker:
        query_parts.append(company_name)

    query = " OR ".join(query_parts)
    rss_url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"

    feed = feedparser.parse(rss_url)
    rows = []

    for entry in feed.entries[:15]:
        published = entry.get("published", "")
        title = entry.get("title", "")
        link = entry.get("link", "")
        source = "Google News RSS"

        rows.append(
            {
                "Published": published,
                "Headline": title,
                "Source": source,
                "URL": link,
            }
        )

    if not rows:
        return pd.DataFrame(columns=["Published", "Headline", "Source", "URL"])

    return pd.DataFrame(rows)