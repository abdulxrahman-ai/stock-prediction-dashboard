# AI Stock Prediction + News Sentiment Dashboard

A professional Streamlit dashboard for stock trend analysis, short-term forecasting, headline sentiment review, and optional candlestick screenshot interpretation.

## Features

On-page controls with no sidebar
Full-width trend and forecast charts
Premium stat-strip layout instead of default Streamlit cards
Key stats, technical snapshot, and news sentiment summary panels
Full-width sentiment table
Optional candlestick screenshot upload and AI interpretation

## Optional image analysis

Candlestick screenshot interpretation uses the OpenAI API **only if** you set `OPENAI_API_KEY` in your environment.

Without that key:
the dashboard still works
market data, forecast, and news sentiment remain available
only the image-analysis section becomes informational

## Run locally

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Environment variable for candlestick image analysis

PowerShell:

```powershell
$env:OPENAI_API_KEY="your_key_here"
python -m streamlit run app.py
```

Command Prompt:

```cmd
set OPENAI_API_KEY=your_key_here
python -m streamlit run app.py
```

## Notes

Forecasting uses a simple lag-based linear regression model for demo and educational purposes.
News data is sourced from Google News RSS.
This project is for educational and portfolio use only.
