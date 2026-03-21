# 🔭 StockLens — Indian Market Analytics Platform

<div align="center">

![StockLens Banner](https://img.shields.io/badge/StockLens-Indian%20Market%20Analytics-1565c0?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQTEwIDEwIDAgMCAwIDIgMTJhMTAgMTAgMCAwIDAgMTAgMTAgMTAgMTAgMCAwIDAgMTAtMTBBMTAgMTAgMCAwIDAgMTIgMnoiLz48L3N2Zz4=)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.0-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A professional stock market analytics platform for Indian equities**
**NSE · BSE · Real-time Data · Technical Analysis · Portfolio Tracking**

[🚀 Live Demo](https://hdfc-price-action-dashboard.streamlit.app) · [📊 Dashboard](#dashboard) · [🔍 Screener](#screener) · [⚖️ Compare](#compare) · [💼 Portfolio](#portfolio)

</div>

---

## 📸 Screenshots

| Dashboard | Screener |
|-----------|----------|
| Full price action with indicators | Filter stocks by RSI, MACD & more |

| Comparison | Portfolio |
|------------|-----------|
| Side by side stock analysis | Track holdings & P&L |

---

## ✨ Features

### 📊 Dashboard
- **Live ticker bar** — Scrolling SENSEX, NIFTY 50, BANKNIFTY, FINNIFTY prices
- **Interactive price charts** — Candlestick, Line, OHLC with zoom and pan
- **6 KPI cards** — Current price, 52W High/Low, RSI, Total Return, Sharpe Ratio
- **5 trading signals** — RSI, MACD, SMA 200, Bollinger Bands, Overall signal
- **Technical indicators** — SMA (20/50/200), EMA 20, Bollinger Bands, VWAP
- **Candlestick patterns** — Doji, Hammer, Shooting Star, Bull/Bear Engulfing
- **Statistical analysis** — Mean, Std Dev, Skewness, Kurtosis, Max Drawdown
- **Monthly returns heatmap** — Year × Month grid with colour coding
- **Volume analysis** — Volume bars with 20-day MA overlay
- **Rolling volatility** — 20-day standard deviation chart
- **MACD chart** — Signal line, histogram with buy/sell crossovers
- **Data explorer** — Select any columns, adjust row count

### 🔍 Stock Screener
- Filter all 20 NSE stocks simultaneously
- Filters: RSI range, Return %, SMA 200 trend, MACD direction
- Results show price, RSI, return, and BUY/SELL/HOLD signal
- Progress bar while scanning

### ⚖️ Stock Comparison
- Compare any 2 NSE stocks side by side
- Normalised performance chart (Base 100)
- Full statistics comparison — Sharpe, Max DD, Volatility, Best/Worst day
- RSI comparison overlay chart
- Return correlation scatter plot with trendline

### 💼 Portfolio Tracker
- Add holdings with stock, quantity and buy price
- Live P&L calculation per holding
- Overall portfolio summary — Invested, Current Value, Total P&L, Return %
- Weight bar for each holding
- Portfolio allocation pie chart
- P&L by stock bar chart
- Normalised performance chart for all holdings

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.10+ |
| **Dashboard** | Streamlit 1.44 |
| **Charts** | Plotly, Plotly Express |
| **Data** | yfinance, Pandas, NumPy |
| **Indicators** | Custom (RSI, MACD, BB, SMA, EMA, VWAP, ATR) |
| **Deployment** | Streamlit Cloud |
| **Version Control** | GitHub |

---

## 📁 Project Structure
```
stocklens/
│
├── hdfc_dashboard.py       # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── stock_data/            # Pre-cached CSV data (NSE stocks)
│   ├── HDFCBANK.csv
│   ├── RELIANCE.csv
│   ├── TCS.csv
│   ├── INFY.csv
│   ├── ICICIBANK.csv
│   ├── SBIN.csv
│   ├── WIPRO.csv
│   ├── BHARTIARTL.csv
│   ├── KOTAKBANK.csv
│   ├── AXISBANK.csv
│   ├── ITC.csv
│   ├── MARUTI.csv
│   ├── BAJFINANCE.csv
│   ├── SUNPHARMA.csv
│   ├── TITAN.csv
│   ├── TATAMOTORS.csv
│   ├── POWERGRID.csv
│   ├── ADANIPORTS.csv
│   └── ASIANPAINT.csv
│
└── hdfc_data.csv          # Legacy HDFC Bank data (backup)
```

---

## 🚀 Run Locally

**Step 1 — Clone the repository**
```bash
git clone https://github.com/Adityaa1001/hdfc-price-action-dashboard.git
cd hdfc-price-action-dashboard
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Launch the app**
```bash
streamlit run hdfc_dashboard.py
```

**Step 4 — Open in browser**
```
http://localhost:8501
```

---

## 📦 Requirements
```
yfinance
pandas
numpy
plotly
streamlit==1.44.0
altair==4.2.2
mplfinance
scipy
```

---

## 📊 Supported Stocks

### NSE Stocks
| Stock | Ticker | Stock | Ticker |
|-------|--------|-------|--------|
| HDFC Bank | HDFCBANK.NS | Axis Bank | AXISBANK.NS |
| Reliance | RELIANCE.NS | ITC | ITC.NS |
| TCS | TCS.NS | Maruti | MARUTI.NS |
| Infosys | INFY.NS | Bajaj Finance | BAJFINANCE.NS |
| ICICI Bank | ICICIBANK.NS | Sun Pharma | SUNPHARMA.NS |
| SBI | SBIN.NS | Titan | TITAN.NS |
| Wipro | WIPRO.NS | Tata Motors | TATAMOTORS.NS |
| Bharti Airtel | BHARTIARTL.NS | Power Grid | POWERGRID.NS |
| Kotak Bank | KOTAKBANK.NS | Adani Ports | ADANIPORTS.NS |
| | | Asian Paints | ASIANPAINT.NS |

### BSE Stocks
HDFC Bank, Reliance, TCS, Infosys, ICICI Bank, SBI, Wipro, ITC, Maruti, Sun Pharma

### Custom Tickers
Enter any valid Yahoo Finance ticker (e.g. `TATASTEEL.NS`, `ONGC.NS`)

---

## 📈 Technical Indicators

| Indicator | Description |
|-----------|-------------|
| **SMA 20/50/200** | Simple Moving Average |
| **EMA 20** | Exponential Moving Average |
| **RSI (14)** | Relative Strength Index |
| **MACD (12,26,9)** | Moving Average Convergence Divergence |
| **Bollinger Bands** | 20-period, 2 standard deviations |
| **VWAP** | Volume Weighted Average Price |
| **ATR (14)** | Average True Range |
| **Volatility** | Rolling 20-day standard deviation |

---

## 🕯️ Candlestick Patterns

| Pattern | Signal | Description |
|---------|--------|-------------|
| **Doji** | Neutral | Open ≈ Close, indecision |
| **Hammer** | Bullish | Long lower shadow, small body |
| **Shooting Star** | Bearish | Long upper shadow, small body |
| **Bullish Engulfing** | Bullish | Green candle engulfs red candle |
| **Bearish Engulfing** | Bearish | Red candle engulfs green candle |

---

## 🌐 Live Deployment

The app is deployed on **Streamlit Cloud** and accessible at:

🔗 **[hdfc-price-action-dashboard.streamlit.app](https://hdfc-price-action-dashboard.streamlit.app)**

---

## 📌 Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Data Collection (yfinance) | ✅ Done |
| Phase 2 | Exploratory Data Analysis | ✅ Done |
| Phase 3 | Statistical Analysis | ✅ Done |
| Phase 4 | Candlestick Pattern Detection | ✅ Done |
| Phase 5 | Streamlit Dashboard | ✅ Done |
| Phase 6 | Multi-stock Support | ✅ Done |
| Phase 7 | Screener + Comparison + Portfolio | ✅ Done |
| Phase 8 | Streamlit Cloud Deployment | ✅ Done |

---

## ⚠️ Disclaimer

> This project is built for **educational purposes only**.
> StockLens does not provide financial advice.
> Do not make investment decisions based on this tool.
> Always consult a SEBI-registered financial advisor.

---

## 👨‍💻 Author

**Aditya Srivastava**
SRM Institute of Science and Technology

---

<div align="center">
Built with ❤️ using Python · Streamlit · Plotly
<br>
⭐ Star this repo if you found it helpful!
</div>
