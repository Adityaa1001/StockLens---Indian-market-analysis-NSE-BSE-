# 📈 HDFC Bank Price Action Analysis Dashboard

An end-to-end stock market data analysis project focused on HDFC Bank (NSE: HDFCBANK), 
built using Python and deployed as an interactive web dashboard.

## 🔍 Project Overview
This project performs comprehensive price action analysis on HDFC Bank stock data 
from 2020 to 2025, covering data collection, exploratory data analysis, statistical 
analysis, technical indicators, and candlestick pattern detection.

## 🛠️ Tech Stack
- **Data Collection** — yfinance (NSE real-time & historical data)
- **Data Analysis** — Pandas, NumPy, SciPy
- **Visualizations** — Matplotlib, Plotly, mplfinance
- **Technical Indicators** — SMA, EMA, RSI, MACD, Bollinger Bands
- **Dashboard** — Streamlit
- **Deployment** — Streamlit Cloud

## 📊 Features
- Interactive candlestick charts with volume
- Moving averages (SMA 20/50/200 and EMA 20)
- RSI and MACD indicators
- Bollinger Bands
- Candlestick pattern detection (Doji, Hammer, Engulfing)
- Support and resistance levels
- KPI cards (Current Price, 52W High/Low, RSI, Volume)
- Date range filter and chart type selector

## 📁 Project Structure
- **Phase 1** — Data Collection (yfinance API)
- **Phase 2** — Exploratory Data Analysis (EDA)
- **Phase 3** — Statistical Analysis
- **Phase 4** — Candlestick Pattern Detection
- **Phase 5** — Interactive Streamlit Dashboard
- **Phase 6** — Deployment on Streamlit Cloud

## 🚀 How to Run Locally
pip install -r requirements.txt
streamlit run hdfc_dashboard.py

## 📌 Data Source
NSE India via Yahoo Finance API (yfinance)
Ticker: HDFCBANK.NS
