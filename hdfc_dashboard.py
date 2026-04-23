import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import yfinance as yf

st.set_page_config(
    page_title="StockLens",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f5f7fa; }
#MainMenu, footer { visibility: hidden; }
section[data-testid="stSidebar"] { background: #1a1a2e !important; }
section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
.topbar {
    background: #1a1a2e; padding: 14px 24px; border-radius: 12px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px;
}
.logo { font-size: 1.5rem; font-weight: 800; color: white; }
.logo span { color: #42a5f5; }
.ticker-bar {
    background: #0d47a1; border-radius: 8px; padding: 8px 16px;
    margin-bottom: 20px; overflow: hidden; white-space: nowrap;
}
.ticker-inner { display: inline-block; animation: scroll-left 25s linear infinite; }
@keyframes scroll-left {
    0%   { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}
.t-item { display: inline-block; margin: 0 30px; font-size: 0.82rem; color: white; }
.t-name { color: #90caf9; font-weight: 600; margin-right: 6px; }
.t-up { color: #69f0ae; }
.t-dn { color: #ff5252; }
.card {
    background: white; border-radius: 14px; padding: 20px;
    margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    border-left: 4px solid #1565c0;
}
.card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.kpi-val   { font-size: 1.6rem; font-weight: 800; color: #1a1a2e; }
.kpi-label { font-size: 0.72rem; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-top: 3px; }
.kpi-sub   { font-size: 0.78rem; font-weight: 600; margin-top: 6px; }
.pill { display:inline-block; padding:3px 12px; border-radius:20px; font-size:0.75rem; font-weight:700; }
.buy  { background:#e8f5e9; color:#2e7d32; }
.sell { background:#ffebee; color:#c62828; }
.hold { background:#fff8e1; color:#f57f17; }
.sec-title {
    font-size: 1rem; font-weight: 700; color: #1a1a2e;
    margin: 20px 0 12px; padding-bottom: 8px;
    border-bottom: 2px solid #f0f0f0;
}
.stat-row {
    display:flex; justify-content:space-between;
    padding: 9px 0; border-bottom: 1px solid #f5f5f5; font-size: 0.875rem;
}
.stat-row:last-child { border-bottom: none; }
.sk { color: #888; }
.sv { font-weight: 600; color: #1a1a2e; }
.pat-row {
    display:flex; justify-content:space-between; align-items:center;
    padding: 10px 14px; background: #f8f9fa;
    border-radius: 10px; margin-bottom: 8px;
}
.pat-row:hover { background: #e3f2fd; }
.scr-row {
    display:flex; align-items:center; padding: 12px 16px;
    background: #f8f9fa; border-radius: 12px; margin-bottom: 8px; transition: all 0.2s;
}
.scr-row:hover { background: #e3f2fd; transform: translateX(4px); }
</style>
""", unsafe_allow_html=True)

# ── Stock Universe ─────────────────────────────────────────────
NSE_STOCKS = {
    "HDFC Bank":      "HDFCBANK.NS",
    "Reliance":       "RELIANCE.NS",
    "TCS":            "TCS.NS",
    "Infosys":        "INFY.NS",
    "ICICI Bank":     "ICICIBANK.NS",
    "SBI":            "SBIN.NS",
    "Wipro":          "WIPRO.NS",
    "Bharti Airtel":  "BHARTIARTL.NS",
    "Kotak Bank":     "KOTAKBANK.NS",
    "Axis Bank":      "AXISBANK.NS",
    "ITC":            "ITC.NS",
    "Maruti":         "MARUTI.NS",
    "Bajaj Finance":  "BAJFINANCE.NS",
    "Sun Pharma":     "SUNPHARMA.NS",
    "Titan":          "TITAN.NS",
    "Tata Motors":    "TATAMOTORS.NS",
    "Power Grid":     "POWERGRID.NS",
    "Adani Ports":    "ADANIPORTS.NS",
    "Asian Paints":   "ASIANPAINT.NS",
    "UltraTech":      "ULTRACEMCO.NS",
}
BSE_STOCKS = {
    "BSE: HDFC Bank":  "HDFCBANK.BO",
    "BSE: Reliance":   "RELIANCE.BO",
    "BSE: TCS":        "TCS.BO",
    "BSE: Infosys":    "INFY.BO",
    "BSE: ICICI Bank": "ICICIBANK.BO",
    "BSE: SBI":        "SBIN.BO",
    "BSE: Wipro":      "WIPRO.BO",
    "BSE: ITC":        "ITC.BO",
    "BSE: Maruti":     "MARUTI.BO",
    "BSE: Sun Pharma": "SUNPHARMA.BO",
}
ALL_STOCKS = {**NSE_STOCKS, **BSE_STOCKS}

# ── Base path for CSV files ────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

TICKER_MAP = {
    "HDFCBANK.NS":   os.path.join(BASE, "stock_data", "HDFCBANK.csv"),
    "RELIANCE.NS":   os.path.join(BASE, "stock_data", "RELIANCE.csv"),
    "TCS.NS":        os.path.join(BASE, "stock_data", "TCS.csv"),
    "INFY.NS":       os.path.join(BASE, "stock_data", "INFY.csv"),
    "ICICIBANK.NS":  os.path.join(BASE, "stock_data", "ICICIBANK.csv"),
    "SBIN.NS":       os.path.join(BASE, "stock_data", "SBIN.csv"),
    "WIPRO.NS":      os.path.join(BASE, "stock_data", "WIPRO.csv"),
    "BHARTIARTL.NS": os.path.join(BASE, "stock_data", "BHARTIARTL.csv"),
    "KOTAKBANK.NS":  os.path.join(BASE, "stock_data", "KOTAKBANK.csv"),
    "AXISBANK.NS":   os.path.join(BASE, "stock_data", "AXISBANK.csv"),
    "ITC.NS":        os.path.join(BASE, "stock_data", "ITC.csv"),
    "MARUTI.NS":     os.path.join(BASE, "stock_data", "MARUTI.csv"),
    "BAJFINANCE.NS": os.path.join(BASE, "stock_data", "BAJFINANCE.csv"),
    "SUNPHARMA.NS":  os.path.join(BASE, "stock_data", "SUNPHARMA.csv"),
    "TITAN.NS":      os.path.join(BASE, "stock_data", "TITAN.csv"),
    "TATAMOTORS.NS": os.path.join(BASE, "stock_data", "TATAMOTORS.csv"),
    "POWERGRID.NS":  os.path.join(BASE, "stock_data", "POWERGRID.csv"),
    "ADANIPORTS.NS": os.path.join(BASE, "stock_data", "ADANIPORTS.csv"),
    "ASIANPAINT.NS": os.path.join(BASE, "stock_data", "ASIANPAINT.csv"),
    "ULTRACEMCO.NS": os.path.join(BASE, "stock_data", "ULTRACEMCO.csv"),
    "HDFCBANK.BO":   os.path.join(BASE, "stock_data", "HDFCBANK.csv"),
    "RELIANCE.BO":   os.path.join(BASE, "stock_data", "RELIANCE.csv"),
    "TCS.BO":        os.path.join(BASE, "stock_data", "TCS.csv"),
    "INFY.BO":       os.path.join(BASE, "stock_data", "INFY.csv"),
    "ICICIBANK.BO":  os.path.join(BASE, "stock_data", "ICICIBANK.csv"),
    "SBIN.BO":       os.path.join(BASE, "stock_data", "SBIN.csv"),
    "WIPRO.BO":      os.path.join(BASE, "stock_data", "WIPRO.csv"),
    "ITC.BO":        os.path.join(BASE, "stock_data", "ITC.csv"),
    "MARUTI.BO":     os.path.join(BASE, "stock_data", "MARUTI.csv"),
    "SUNPHARMA.BO":  os.path.join(BASE, "stock_data", "SUNPHARMA.csv"),
}

# ── Helpers ────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def get_indices():
    return {
        "SENSEX":    (73500.00, 0.42),
        "NIFTY 50":  (22300.00, 0.38),
        "BANKNIFTY": (47800.00, 0.21),
        "FINNIFTY":  (21200.00, 0.15),
    }

@st.cache_data(ttl=3600)
def fetch(ticker, start, end):
    # Load from CSV if available
    if ticker in TICKER_MAP:
        csv_path = TICKER_MAP[ticker]
        try:
            df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            df.index = pd.to_datetime(df.index)
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            df = df[(df.index >= pd.Timestamp(start)) &
                    (df.index <= pd.Timestamp(end))].copy()
            if not df.empty:
                return df
        except Exception:
            pass

    # Fallback to live fetch for custom tickers
    try:
        df = yf.download(ticker, start=str(start), end=str(end),
                         auto_adjust=True, progress=False)
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.index = pd.to_datetime(df.index)
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df.drop(columns=["Dividends","Stock Splits"],
                inplace=True, errors='ignore')
        return df
    except Exception:
        return pd.DataFrame()

def add_indicators(df, rsi_p=14, bb_p=20):
    df = df.copy()
    df['SMA_20']   = df['Close'].rolling(20).mean()
    df['SMA_50']   = df['Close'].rolling(50).mean()
    df['SMA_200']  = df['Close'].rolling(200).mean()
    df['EMA_20']   = df['Close'].ewm(span=20, adjust=False).mean()
    df['BB_Mid']   = df['Close'].rolling(bb_p).mean()
    df['BB_Std']   = df['Close'].rolling(bb_p).std()
    df['BB_Upper'] = df['BB_Mid'] + 2 * df['BB_Std']
    df['BB_Lower'] = df['BB_Mid'] - 2 * df['BB_Std']
    delta = df['Close'].diff()
    gain  = delta.where(delta > 0, 0).rolling(rsi_p).mean()
    loss  = -delta.where(delta < 0, 0).rolling(rsi_p).mean()
    df['RSI']         = 100 - (100 / (1 + gain / loss))
    e12 = df['Close'].ewm(span=12, adjust=False).mean()
    e26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD']        = e12 - e26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist']   = df['MACD'] - df['MACD_Signal']
    df['Daily_Return']= df['Close'].pct_change() * 100
    df['Volatility']  = df['Daily_Return'].rolling(20).std()
    df['VWAP']        = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    tr = pd.concat([
        df['High'] - df['Low'],
        abs(df['High'] - df['Close'].shift()),
        abs(df['Low']  - df['Close'].shift())
    ], axis=1).max(axis=1)
    df['ATR']  = tr.rolling(14).mean()
    df['Body'] = abs(df['Close'] - df['Open'])
    df['Range']= df['High'] - df['Low']
    df['US']   = df['High'] - df[['Close','Open']].max(axis=1)
    df['LS']   = df[['Close','Open']].min(axis=1) - df['Low']
    df['Doji']       = df['Body'] <= 0.1 * df['Range']
    df['Hammer']     = (df['LS']>=2*df['Body']) & (df['US']<=0.1*df['Range']) & (df['Body']>0)
    df['ShootingStar']  = (df['US']>=2*df['Body']) & (df['LS']<=0.1*df['Range']) & (df['Body']>0)
    df['BullEngulf'] = (df['Close']>df['Open']) & (df['Close'].shift(1)<df['Open'].shift(1)) & (df['Close']>df['Open'].shift(1)) & (df['Open']<df['Close'].shift(1))
    df['BearEngulf'] = (df['Close']<df['Open']) & (df['Close'].shift(1)>df['Open'].shift(1)) & (df['Close']<df['Open'].shift(1)) & (df['Open']>df['Close'].shift(1))
    df['Month'] = df.index.month
    df['Year']  = df.index.year
    return df

def vol_colors(df):
    return ['#4caf50' if float(c)>=float(o) else '#f44336'
            for c, o in zip(df['Close'], df['Open'])]

def plot_cfg(fig, h=400, title=""):
    fig.update_layout(
        height=h, template='plotly_white',
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='Inter', color='#1a1a2e', size=11),
        title=dict(text=title, font=dict(size=13, color='#1a1a2e')),
        margin=dict(l=0, r=0, t=40 if title else 10, b=0),
        legend=dict(orientation='h', y=1.08,
                    bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
        xaxis_rangeslider_visible=False
    )
    for i in range(1, 6):
        fig.update_xaxes(gridcolor='#f5f5f5', row=i, col=1)
        fig.update_yaxes(gridcolor='#f5f5f5', row=i, col=1)
    return fig

# ── Session defaults ───────────────────────────────────────────
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# ── Ticker Bar ─────────────────────────────────────────────────
idx = get_indices()
items = ""
for name, (price, chg) in idx.items():
    cls   = "t-up" if chg >= 0 else "t-dn"
    arrow = "▲" if chg >= 0 else "▼"
    items += f"""<span class='t-item'>
        <span class='t-name'>{name}</span>
        {price:,.2f}
        <span class='{cls}'>{arrow}{abs(chg):.2f}%</span>
    </span>"""

st.markdown(f"""
<div class='ticker-bar'>
    <div class='ticker-inner'>{items * 3}</div>
</div>
""", unsafe_allow_html=True)

# ── Top Bar ────────────────────────────────────────────────────
st.markdown("""
<div class='topbar'>
    <div class='logo'>🔭 Stock<span>Lens</span></div>
    <div style='color:#90caf9;font-size:0.85rem;'>
        Indian Market Analytics · NSE & BSE
    </div>
    <div style='background:#0d47a1;color:#90caf9;padding:4px 14px;
    border-radius:20px;font-size:0.8rem;font-weight:600;'>● Live</div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔭 StockLens")
    st.markdown("---")

    page = st.radio("📌 Navigate", [
        "📊 Dashboard",
        "🔍 Screener",
        "⚖️ Compare",
        "💼 Portfolio"
    ])

    st.markdown("---")
    st.markdown("**🔎 Stock**")
    exchange     = st.radio("Exchange", ["NSE","BSE"], horizontal=True)
    universe     = NSE_STOCKS if exchange == "NSE" else BSE_STOCKS
    stock_name   = st.selectbox("Select", list(universe.keys()))
    stock_ticker = universe[stock_name]

    custom = st.text_input("Custom ticker (e.g. TATASTEEL.NS)")
    if custom.strip():
        stock_name   = custom.strip().upper()
        stock_ticker = custom.strip().upper()

    st.markdown("**📅 Date Range**")
    start = st.date_input("From", pd.to_datetime("2020-01-01"))
    end   = st.date_input("To",   pd.to_datetime("2025-03-21"))

    st.markdown("**⚙️ Settings**")
    chart_type    = st.selectbox("Chart", ["Candlestick","Line","OHLC"])
    show_sma      = st.checkbox("SMA Lines",       value=True)
    show_ema      = st.checkbox("EMA 20",          value=False)
    show_bb       = st.checkbox("Bollinger Bands", value=True)
    show_vwap     = st.checkbox("VWAP",            value=False)
    show_patterns = st.checkbox("Patterns on Chart", value=True)
    rsi_p = st.slider("RSI Period", 7, 28, 14)
    bb_p  = st.slider("BB Period",  10, 50, 20)

    st.markdown("""
    <div style='background:#283593;border-radius:10px;padding:12px;
    font-size:0.75rem;color:#90caf9;margin-top:12px;'>
    📡 NSE & BSE Stocks<br>
    💾 CSV-cached · No rate limits<br>
    🔄 Custom tickers: live fetch
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "📊 Dashboard":

    with st.spinner(f"Loading {stock_name}..."):
        raw = fetch(stock_ticker, start, end)

    if raw.empty:
        st.error(f"❌ Could not load data for **{stock_ticker}**.")
        st.stop()

    df  = add_indicators(raw, rsi_p, bb_p)
    vc  = vol_colors(df)

    cur  = float(df['Close'].iloc[-1])
    prev = float(df['Close'].iloc[-2])
    chg  = cur - prev
    chgp = chg / prev * 100
    rsi  = float(df['RSI'].iloc[-1])
    macd = float(df['MACD'].iloc[-1])
    hi52 = float(df['High'].tail(252).max())
    lo52 = float(df['Low'].tail(252).min())
    ret  = ((cur / float(df['Close'].iloc[0])) - 1) * 100
    sh   = df['Daily_Return'].mean() / df['Daily_Return'].std() * np.sqrt(252)
    dd   = ((df['Close'] / df['Close'].cummax()) - 1).min() * 100

    # Stock Header
    st.markdown(f"""
    <div style='background:white;border-radius:14px;padding:20px 24px;
    margin-bottom:20px;box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
        <div style='display:flex;align-items:center;justify-content:space-between;'>
            <div>
                <div style='font-size:1.5rem;font-weight:800;color:#1a1a2e;'>
                    {stock_name}
                    <span style='font-size:0.85rem;font-weight:400;
                    color:#888;margin-left:8px;'>{stock_ticker}</span>
                </div>
                <div style='font-size:0.82rem;color:#aaa;margin-top:3px;'>
                    {df.index[0].strftime('%d %b %Y')} –
                    {df.index[-1].strftime('%d %b %Y')} ·
                    {len(df)} trading days
                </div>
            </div>
            <div style='text-align:right;'>
                <div style='font-size:2rem;font-weight:800;color:#1a1a2e;'>
                    ₹{cur:,.2f}
                </div>
                <div style='font-size:0.95rem;font-weight:600;
                color:{"#4caf50" if chg>=0 else "#f44336"}'>
                    {'▲' if chg>=0 else '▼'} ₹{abs(chg):.2f} ({chgp:+.2f}%)
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpis = [
        (k1, f"₹{cur:,.2f}",      "Current Price", f"{'▲' if chg>=0 else '▼'} {chgp:+.2f}%",   "#4caf50" if chg>=0 else "#f44336", "#1565c0"),
        (k2, f"₹{hi52:,.2f}",     "52W High",      f"{((cur/hi52)-1)*100:.1f}% from high",       "#f44336", "#e53935"),
        (k3, f"₹{lo52:,.2f}",     "52W Low",       f"{((cur/lo52)-1)*100:.1f}% above low",       "#4caf50", "#43a047"),
        (k4, f"{rsi:.1f}",        "RSI (14)",      "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral", "#4caf50" if rsi<=70 else "#f44336", "#7b1fa2"),
        (k5, f"{ret:.1f}%",       "Total Return",  f"Since {df.index[0].strftime('%b %Y')}",     "#4caf50" if ret>0 else "#f44336", "#0288d1"),
        (k6, f"{sh:.2f}",         "Sharpe Ratio",  "Risk-adjusted return",                       "#4caf50" if sh>1 else "#ff9800", "#00796b"),
    ]
    for col, val, label, sub, sub_color, border in kpis:
        col.markdown(f"""
        <div class='card' style='border-left-color:{border};'>
            <div class='kpi-val'>{val}</div>
            <div class='kpi-label'>{label}</div>
            <div class='kpi-sub' style='color:{sub_color};'>{sub}</div>
        </div>""", unsafe_allow_html=True)

    # Signals
    st.markdown("<div class='sec-title'>🚦 Technical Signals</div>",
                unsafe_allow_html=True)
    rsi_s  = ("BUY","buy")   if rsi<30  else ("SELL","sell") if rsi>70 else ("HOLD","hold")
    macd_s = ("BUY","buy")   if macd>0  else ("SELL","sell")
    sma_s  = ("BUY","buy")   if cur>float(df['SMA_200'].iloc[-1]) else ("SELL","sell")
    bb_lo  = float(df['BB_Lower'].iloc[-1])
    bb_hi  = float(df['BB_Upper'].iloc[-1])
    bb_pct = (cur - bb_lo) / (bb_hi - bb_lo)
    bb_s   = ("BUY","buy")   if bb_pct<0.2 else ("SELL","sell") if bb_pct>0.8 else ("HOLD","hold")
    buy_ct = sum(1 for s in [rsi_s,macd_s,sma_s,bb_s] if s[0]=="BUY")
    sel_ct = sum(1 for s in [rsi_s,macd_s,sma_s,bb_s] if s[0]=="SELL")
    ov_s   = ("BUY","buy") if buy_ct>=3 else ("SELL","sell") if sel_ct>=3 else ("HOLD","hold")

    sg1,sg2,sg3,sg4,sg5 = st.columns(5)
    for col, label, sig in [
        (sg1, f"RSI ({rsi:.0f})",  rsi_s),
        (sg2, "MACD",             macd_s),
        (sg3, "SMA 200",          sma_s),
        (sg4, "Bollinger",        bb_s),
        (sg5, "Overall Signal",   ov_s),
    ]:
        col.markdown(f"""
        <div style='background:white;border-radius:12px;padding:14px;
        text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.06);'>
            <div style='font-size:0.78rem;color:#888;margin-bottom:8px;'>{label}</div>
            <span class='pill {sig[1]}'>{sig[0]}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Chart
    st.markdown("<div class='sec-title'>💹 Price Chart</div>",
                unsafe_allow_html=True)

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        row_heights=[0.6,0.2,0.2], vertical_spacing=0.02)

    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name=stock_name,
            increasing_line_color='#4caf50',
            decreasing_line_color='#f44336'
        ), row=1, col=1)
    elif chart_type == "OHLC":
        fig.add_trace(go.Ohlc(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name=stock_name
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'], name=stock_name,
            line=dict(color='#1565c0', width=2),
            fill='tozeroy', fillcolor='rgba(21,101,192,0.05)'
        ), row=1, col=1)

    if show_sma:
        for cn, color, nm in [
            ('SMA_20','#ff9800','SMA 20'),
            ('SMA_50','#4caf50','SMA 50'),
            ('SMA_200','#f44336','SMA 200')
        ]:
            fig.add_trace(go.Scatter(x=df.index, y=df[cn], name=nm,
                line=dict(color=color, width=1.2)), row=1, col=1)

    if show_ema:
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], name='EMA 20',
            line=dict(color='#7b1fa2', width=1.2, dash='dot')), row=1, col=1)

    if show_vwap:
        fig.add_trace(go.Scatter(x=df.index, y=df['VWAP'], name='VWAP',
            line=dict(color='#00796b', width=1.2, dash='dash')), row=1, col=1)

    if show_bb:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper',
            line=dict(color='rgba(100,100,100,0.35)', width=0.8)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower',
            line=dict(color='rgba(100,100,100,0.35)', width=0.8),
            fill='tonexty', fillcolor='rgba(100,100,100,0.04)'), row=1, col=1)

    if show_patterns:
        for pat, sym, color, use_low in [
            ('Doji',       'circle-open', '#ff9800', False),
            ('Hammer',     'triangle-up', '#4caf50', True),
            ('BullEngulf', 'star',        '#4caf50', True),
            ('BearEngulf', 'star',        '#f44336', False),
        ]:
            pf = df[df[pat]]
            yv = pf['Low']*0.985 if use_low else pf['High']*1.015
            fig.add_trace(go.Scatter(
                x=pf.index, y=yv, mode='markers', name=pat,
                marker=dict(symbol=sym, color=color, size=9)
            ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=df.index, y=df['Volume'],
        marker_color=vc, opacity=0.6, name='Volume'
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df['RSI'], name='RSI',
        line=dict(color='#1565c0', width=1.5)
    ), row=3, col=1)
    fig.add_hrect(y0=70, y1=100,
                  fillcolor='rgba(244,67,54,0.05)', line_width=0, row=3, col=1)
    fig.add_hrect(y0=0,  y1=30,
                  fillcolor='rgba(76,175,80,0.05)',  line_width=0, row=3, col=1)
    fig.add_hline(y=70, line_dash='dash',
                  line_color='#f44336', line_width=1, row=3, col=1)
    fig.add_hline(y=30, line_dash='dash',
                  line_color='#4caf50', line_width=1, row=3, col=1)

    plot_cfg(fig, h=580)
    st.plotly_chart(fig, use_container_width=True)

    # Stats + MACD
    left, right = st.columns(2)
    with left:
        st.markdown("<div class='sec-title'>📐 Statistics</div>",
                    unsafe_allow_html=True)
        html = "<div style='background:white;border-radius:14px;padding:16px;box-shadow:0 1px 4px rgba(0,0,0,0.07);'>"
        for k, v in [
            ("Mean Price",   f"₹{df['Close'].mean():.2f}"),
            ("Std Dev",      f"₹{df['Close'].std():.2f}"),
            ("Best Day",     f"+{df['Daily_Return'].max():.2f}%"),
            ("Worst Day",    f"{df['Daily_Return'].min():.2f}%"),
            ("Max Drawdown", f"{dd:.2f}%"),
            ("+ve Days",     f"{(df['Daily_Return']>0).mean()*100:.1f}%"),
            ("Avg Volume",   f"{df['Volume'].mean()/1e6:.1f}M"),
        ]:
            html += f"<div class='stat-row'><span class='sk'>{k}</span><span class='sv'>{v}</span></div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

    with right:
        st.markdown("<div class='sec-title'>📉 MACD</div>",
                    unsafe_allow_html=True)
        fig_m = go.Figure()
        fig_m.add_trace(go.Bar(
            x=df.index, y=df['MACD_Hist'], name='Histogram',
            marker_color=['#4caf50' if v>=0 else '#f44336'
                          for v in df['MACD_Hist']], opacity=0.7))
        fig_m.add_trace(go.Scatter(x=df.index, y=df['MACD'],
            name='MACD', line=dict(color='#1565c0', width=1.5)))
        fig_m.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'],
            name='Signal', line=dict(color='#f44336', width=1.5)))
        plot_cfg(fig_m, h=280)
        st.plotly_chart(fig_m, use_container_width=True)

    # Heatmap
    st.markdown("<div class='sec-title'>🗓️ Monthly Returns Heatmap</div>",
                unsafe_allow_html=True)
    mn = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
          7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    monthly = df.groupby(['Year','Month'])['Daily_Return'].sum().unstack()
    monthly.columns = [mn[m] for m in monthly.columns]
    fig_h = px.imshow(monthly, color_continuous_scale='RdYlGn',
                      aspect='auto', text_auto='.1f')
    plot_cfg(fig_h, h=260)
    st.plotly_chart(fig_h, use_container_width=True)

    # Patterns
    st.markdown("<div class='sec-title'>🕯️ Candlestick Patterns</div>",
                unsafe_allow_html=True)
    p1,p2,p3,p4,p5 = st.columns(5)
    for col, icon, name, cnt, color in [
        (p1,"🟡","Doji",          int(df['Doji'].sum()),        "#ff9800"),
        (p2,"🟢","Hammer",        int(df['Hammer'].sum()),      "#4caf50"),
        (p3,"🔴","Shooting Star", int(df['ShootingStar'].sum()),"#f44336"),
        (p4,"🟢","Bull Engulf",   int(df['BullEngulf'].sum()),  "#4caf50"),
        (p5,"🔴","Bear Engulf",   int(df['BearEngulf'].sum()),  "#f44336"),
    ]:
        col.markdown(f"""
        <div style='background:white;border-radius:14px;padding:18px;
        text-align:center;border-top:4px solid {color};
        box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
            <div style='font-size:1.6rem;'>{icon}</div>
            <div style='font-size:1.5rem;font-weight:800;color:{color};'>{cnt}</div>
            <div style='font-size:0.75rem;color:#888;margin-top:4px;'>{name}</div>
        </div>""", unsafe_allow_html=True)

    # Volume + Volatility
    st.markdown("<div class='sec-title'>📦 Volume & Volatility</div>",
                unsafe_allow_html=True)
    v1, v2 = st.columns(2)
    with v1:
        df['VolMA'] = df['Volume'].rolling(20).mean()
        fig_v = go.Figure()
        fig_v.add_trace(go.Bar(x=df.index, y=df['Volume'],
            marker_color=vc, opacity=0.5, name='Volume'))
        fig_v.add_trace(go.Scatter(x=df.index, y=df['VolMA'],
            name='MA 20', line=dict(color='#1565c0', width=2)))
        plot_cfg(fig_v, h=260, title="Volume")
        st.plotly_chart(fig_v, use_container_width=True)

    with v2:
        fig_vo = go.Figure()
        fig_vo.add_trace(go.Scatter(
            x=df.index, y=df['Volatility'], fill='tozeroy',
            fillcolor='rgba(123,31,162,0.07)',
            line=dict(color='#7b1fa2', width=2), name='Volatility'))
        fig_vo.add_hline(
            y=float(df['Volatility'].mean()), line_dash='dash',
            line_color='#ff9800', annotation_text="Mean",
            annotation_font_color='#ff9800')
        plot_cfg(fig_vo, h=260, title="Rolling Volatility (20d)")
        st.plotly_chart(fig_vo, use_container_width=True)

    # Data Explorer
    st.markdown("<div class='sec-title'>📋 Data Explorer</div>",
                unsafe_allow_html=True)
    all_cols = ['Open','High','Low','Close','Volume','RSI','MACD',
                'BB_Upper','BB_Lower','SMA_20','SMA_50','SMA_200',
                'EMA_20','ATR','Volatility','Daily_Return','VWAP']
    e1, e2 = st.columns([3,1])
    with e1:
        sel_cols = st.multiselect("Columns", all_cols,
            default=['Open','High','Low','Close','Volume','RSI','MACD'])
    with e2:
        n = st.slider("Rows", 10, 100, 30)
    st.dataframe(
        df[sel_cols].tail(n).round(2).sort_index(ascending=False),
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════
# SCREENER
# ══════════════════════════════════════════════════════════════
elif page == "🔍 Screener":
    st.markdown("""
    <div style='font-size:1.6rem;font-weight:800;color:#1a1a2e;margin-bottom:4px;'>
    🔍 Stock Screener</div>
    <div style='color:#888;margin-bottom:20px;'>
    Filter NSE stocks by technical criteria</div>
    """, unsafe_allow_html=True)

    f1,f2,f3,f4 = st.columns(4)
    with f1:
        rsi_min = st.slider("RSI Min", 0, 100, 0)
        rsi_max = st.slider("RSI Max", 0, 100, 100)
    with f2:
        ret_min = st.slider("Return % Min", -100, 300, -100)
        ret_max = st.slider("Return % Max", -100, 300, 300)
    with f3:
        trend_f = st.selectbox("Trend Filter",
                               ["All","Above SMA200","Below SMA200"])
        macd_f  = st.selectbox("MACD Filter",
                               ["All","Bullish","Bearish"])
    with f4:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        run = st.button("🔍 Run Screener",
                        use_container_width=True, type="primary")

    if run:
        results = []
        bar = st.progress(0)
        items_list = list(NSE_STOCKS.items())
        for i, (nm, tk) in enumerate(items_list):
            bar.progress((i+1)/len(items_list), text=f"Scanning {nm}...")
            try:
                r = fetch(tk, start, end)
                if r.empty or len(r) < 50:
                    continue
                d   = add_indicators(r)
                cp  = float(d['Close'].iloc[-1])
                rv  = float(d['RSI'].iloc[-1])
                mv  = float(d['MACD'].iloc[-1])
                ret = ((cp / float(d['Close'].iloc[0])) - 1) * 100
                s2  = float(d['SMA_200'].iloc[-1])
                if not (rsi_min<=rv<=rsi_max): continue
                if not (ret_min<=ret<=ret_max): continue
                if trend_f=="Above SMA200" and cp<=s2: continue
                if trend_f=="Below SMA200" and cp>=s2: continue
                if macd_f=="Bullish" and mv<=0: continue
                if macd_f=="Bearish" and mv>=0: continue
                sig = ("BUY","buy")   if rv<40 and mv>0 \
                 else ("SELL","sell") if rv>60 and mv<0 \
                 else ("HOLD","hold")
                results.append(dict(name=nm, ticker=tk, price=cp,
                                    rsi=rv, macd=mv, ret=ret, sig=sig))
            except Exception:
                continue
        bar.empty()

        if results:
            st.success(f"✅ {len(results)} stocks matched your criteria")
            for r in results:
                rc = "#4caf50" if r['ret']>=0 else "#f44336"
                st.markdown(f"""
                <div class='scr-row'>
                    <div style='flex:2;'>
                        <div style='font-weight:700;color:#1a1a2e;'>{r['name']}</div>
                        <div style='color:#888;font-size:0.75rem;'>{r['ticker']}</div>
                    </div>
                    <div style='flex:1;text-align:center;font-weight:700;color:#1a1a2e;'>
                        ₹{r['price']:,.2f}
                    </div>
                    <div style='flex:1;text-align:center;color:#555;'>
                        RSI: {r['rsi']:.1f}
                    </div>
                    <div style='flex:1;text-align:center;font-weight:600;color:{rc};'>
                        {"+" if r['ret']>=0 else ""}{r['ret']:.1f}%
                    </div>
                    <div style='flex:1;text-align:right;'>
                        <span class='pill {r["sig"][1]}'>{r["sig"][0]}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.warning("No stocks matched. Try widening your filters.")

# ══════════════════════════════════════════════════════════════
# COMPARE
# ══════════════════════════════════════════════════════════════
elif page == "⚖️ Compare":
    st.markdown("""
    <div style='font-size:1.6rem;font-weight:800;color:#1a1a2e;margin-bottom:4px;'>
    ⚖️ Stock Comparison</div>
    <div style='color:#888;margin-bottom:20px;'>
    Compare two stocks side by side</div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        n1 = st.selectbox("Stock 1", list(NSE_STOCKS.keys()), index=0)
        t1 = NSE_STOCKS[n1]
    with c2:
        n2 = st.selectbox("Stock 2", list(NSE_STOCKS.keys()), index=1)
        t2 = NSE_STOCKS[n2]

    with st.spinner("Loading..."):
        r1 = fetch(t1, start, end)
        r2 = fetch(t2, start, end)

    if r1.empty or r2.empty:
        st.error("Could not load one or both stocks.")
        st.stop()

    d1 = add_indicators(r1)
    d2 = add_indicators(r2)

    norm1 = (d1['Close'] / float(d1['Close'].iloc[0])) * 100
    norm2 = (d2['Close'] / float(d2['Close'].iloc[0])) * 100
    fig_n = go.Figure()
    fig_n.add_trace(go.Scatter(x=d1.index, y=norm1, name=n1,
                               line=dict(color='#1565c0', width=2)))
    fig_n.add_trace(go.Scatter(x=d2.index, y=norm2, name=n2,
                               line=dict(color='#f44336', width=2)))
    plot_cfg(fig_n, h=360, title="Normalised Performance (Base 100)")
    st.plotly_chart(fig_n, use_container_width=True)

    m1, m2 = st.columns(2)
    def make_stat(d, nm):
        cp  = float(d['Close'].iloc[-1])
        ret = ((cp/float(d['Close'].iloc[0]))-1)*100
        rv  = float(d['RSI'].iloc[-1])
        sh  = d['Daily_Return'].mean()/d['Daily_Return'].std()*np.sqrt(252)
        ddv = ((d['Close']/d['Close'].cummax())-1).min()*100
        vv  = float(d['Volatility'].iloc[-1])
        rc  = "#4caf50" if ret>=0 else "#f44336"
        html = f"""
        <div style='background:white;border-radius:14px;padding:20px;
        box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
        <div style='font-size:1rem;font-weight:700;color:#1a1a2e;
        margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid #f0f0f0;'>
        {nm}</div>"""
        for k, v, vc2 in [
            ("Price",      f"₹{cp:,.2f}",  "#1a1a2e"),
            ("Return",     f"{'+'if ret>=0 else ''}{ret:.2f}%", rc),
            ("RSI",        f"{rv:.1f}",     "#1a1a2e"),
            ("Sharpe",     f"{sh:.2f}",     "#1a1a2e"),
            ("Max DD",     f"{ddv:.2f}%",   "#f44336"),
            ("Volatility", f"{vv:.2f}%",    "#1a1a2e"),
            ("Best Day",   f"+{d['Daily_Return'].max():.2f}%", "#4caf50"),
            ("Worst Day",  f"{d['Daily_Return'].min():.2f}%",  "#f44336"),
        ]:
            html += f"""<div class='stat-row'>
            <span class='sk'>{k}</span>
            <span class='sv' style='color:{vc2};'>{v}</span></div>"""
        html += "</div>"
        return html

    m1.markdown(make_stat(d1, n1), unsafe_allow_html=True)
    m2.markdown(make_stat(d2, n2), unsafe_allow_html=True)

    fig_r2 = go.Figure()
    fig_r2.add_trace(go.Scatter(x=d1.index, y=d1['RSI'], name=n1,
                                line=dict(color='#1565c0', width=1.5)))
    fig_r2.add_trace(go.Scatter(x=d2.index, y=d2['RSI'], name=n2,
                                line=dict(color='#f44336', width=1.5)))
    fig_r2.add_hline(y=70, line_dash='dash', line_color='#f44336', line_width=1)
    fig_r2.add_hline(y=30, line_dash='dash', line_color='#4caf50', line_width=1)
    plot_cfg(fig_r2, h=260, title="RSI Comparison")
    fig_r2.update_yaxes(range=[0,100])
    st.plotly_chart(fig_r2, use_container_width=True)

    comb = pd.DataFrame({
        n1: d1['Daily_Return'],
        n2: d2['Daily_Return']
    }).dropna()
    corr = comb.corr().iloc[0,1]
    fig_c = px.scatter(comb, x=n1, y=n2, trendline="ols",
                       title=f"Return Correlation: {corr:.3f}",
                       color_discrete_sequence=['#1565c0'])
    plot_cfg(fig_c, h=300)
    st.plotly_chart(fig_c, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PORTFOLIO
# ══════════════════════════════════════════════════════════════
elif page == "💼 Portfolio":
    st.markdown("""
    <div style='font-size:1.6rem;font-weight:800;color:#1a1a2e;margin-bottom:4px;'>
    💼 Portfolio Tracker</div>
    <div style='color:#888;margin-bottom:20px;'>
    Track and analyse your holdings</div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div style='background:white;border-radius:14px;padding:20px;
        margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
        <div style='font-weight:700;color:#1a1a2e;margin-bottom:14px;'>
        ➕ Add Holding</div>""", unsafe_allow_html=True)

        pa, pb, pc, pd_col = st.columns([3,2,2,1])
        with pa:
            ps = st.selectbox("Stock", list(NSE_STOCKS.keys()), key="ps")
        with pb:
            pq = st.number_input("Quantity", min_value=1, value=10, key="pq")
        with pc:
            pp = st.number_input("Buy Price ₹", min_value=1.0,
                                 value=1000.0, key="pp")
        with pd_col:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Add ➕", use_container_width=True):
                st.session_state.portfolio.append({
                    "name":   ps,
                    "ticker": NSE_STOCKS[ps],
                    "qty":    pq,
                    "buy":    pp
                })
                st.success(f"✅ Added {ps}!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    col_clear, _ = st.columns([1,4])
    with col_clear:
        if st.button("🗑️ Clear Portfolio"):
            st.session_state.portfolio = []
            st.rerun()

    if not st.session_state.portfolio:
        st.info("👆 Add stocks above to get started!")
    else:
        total_inv = 0.0
        total_cur = 0.0
        rows = []

        with st.spinner("Fetching prices..."):
            for h in st.session_state.portfolio:
                try:
                    r  = fetch(h['ticker'], start, end)
                    if r.empty: continue
                    cp = float(r['Close'].iloc[-1])
                    iv = h['qty'] * h['buy']
                    cv = h['qty'] * cp
                    pn = cv - iv
                    pp2= (pn / iv) * 100
                    total_inv += iv
                    total_cur += cv
                    rows.append({**h, 'cmp':cp, 'inv':iv,
                                  'cur':cv, 'pnl':pn,
                                  'pct':pp2, 'raw':r})
                except Exception:
                    continue

        if not rows:
            st.warning("Could not fetch prices. Try again.")
            st.stop()

        tp  = total_cur - total_inv
        tpp = (tp / total_inv) * 100
        tc  = "#4caf50" if tp>=0 else "#f44336"

        s1,s2,s3,s4 = st.columns(4)
        for col, val, label, color in [
            (s1, f"₹{total_inv:,.0f}", "Total Invested",  "#1565c0"),
            (s2, f"₹{total_cur:,.0f}", "Current Value",   "#4caf50" if total_cur>=total_inv else "#f44336"),
            (s3, f"{'+'if tp>=0 else ''}₹{tp:,.0f}", "Total P&L", tc),
            (s4, f"{'+'if tpp>=0 else ''}{tpp:.2f}%", "Return",   tc),
        ]:
            col.markdown(f"""
            <div class='card' style='border-left-color:{color};'>
                <div class='kpi-val' style='color:{color};'>{val}</div>
                <div class='kpi-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:white;border-radius:14px;padding:20px;
        margin:16px 0;box-shadow:0 1px 4px rgba(0,0,0,0.07);'>
        <div style='font-weight:700;color:#1a1a2e;margin-bottom:14px;'>
        📋 Holdings</div>""", unsafe_allow_html=True)

        for h in rows:
            w   = (h['cur'] / total_cur) * 100
            pc2 = "#4caf50" if h['pnl']>=0 else "#f44336"
            st.markdown(f"""
            <div class='scr-row'>
                <div style='flex:2;'>
                    <div style='font-weight:700;color:#1a1a2e;'>{h['name']}</div>
                    <div style='color:#888;font-size:0.75rem;'>
                    Qty: {h['qty']} · Avg: ₹{h['buy']:.2f}</div>
                </div>
                <div style='flex:1;text-align:center;'>
                    <div style='font-weight:700;color:#1a1a2e;'>
                    ₹{h['cmp']:,.2f}</div>
                    <div style='color:#888;font-size:0.72rem;'>CMP</div>
                </div>
                <div style='flex:1;text-align:center;'>
                    <div style='font-weight:700;color:{pc2};'>
                    {"+"if h['pnl']>=0 else ""}₹{h['pnl']:,.0f}</div>
                    <div style='color:{pc2};font-size:0.72rem;'>
                    {"+"if h['pct']>=0 else ""}{h['pct']:.2f}%</div>
                </div>
                <div style='flex:1;text-align:right;'>
                    <div style='font-size:0.78rem;color:#888;'>{w:.1f}%</div>
                    <div style='background:#f0f0f0;border-radius:4px;
                    height:4px;margin-top:5px;'>
                        <div style='background:#1565c0;
                        width:{min(w,100):.0f}%;height:4px;
                        border-radius:4px;'></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        ch1, ch2 = st.columns(2)
        with ch1:
            fp = px.pie(
                values=[h['cur'] for h in rows],
                names=[h['name'] for h in rows],
                title="Portfolio Allocation",
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            plot_cfg(fp, h=300, title="Portfolio Allocation")
            fp.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fp, use_container_width=True)

        with ch2:
            fb = px.bar(
                x=[h['name'] for h in rows],
                y=[h['pnl']  for h in rows],
                color=[h['pnl'] for h in rows],
                color_continuous_scale=['#f44336','#ffeb3b','#4caf50'],
                title="P&L by Stock"
            )
            plot_cfg(fb, h=300, title="P&L by Stock")
            fb.update_layout(coloraxis_showscale=False, showlegend=False)
            st.plotly_chart(fb, use_container_width=True)

        fp2 = go.Figure()
        cols_l = ['#1565c0','#f44336','#4caf50',
                  '#ff9800','#7b1fa2','#00796b','#c62828']
        for i, h in enumerate(rows):
            n = (h['raw']['Close'] / float(h['raw']['Close'].iloc[0])) * 100
            fp2.add_trace(go.Scatter(
                x=h['raw'].index, y=n, name=h['name'],
                line=dict(color=cols_l[i % len(cols_l)], width=1.5)
            ))
        plot_cfg(fp2, h=320, title="Performance (Base 100)")
        st.plotly_chart(fp2, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div style='background:#1a1a2e;border-radius:14px;padding:18px 24px;
margin-top:30px;display:flex;justify-content:space-between;align-items:center;'>
    <div style='font-weight:700;color:#90caf9;font-size:1rem;'>
    🔭 StockLens</div>
    <div style='color:#5c6bc0;font-size:0.8rem;'>
    NSE · BSE · CSV-cached data · Educational use only</div>
</div>
""", unsafe_allow_html=True)
