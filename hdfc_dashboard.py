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
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background-color: #ffffff; }

.stApp > header { display: none; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }

/* ── Ticker Bar ── */
.ticker-wrapper {
    background: #1a1a2e;
    padding: 8px 0;
    overflow: hidden;
    white-space: nowrap;
    width: 100%;
    position: relative;
}

.ticker-track {
    display: inline-block;
    animation: ticker-scroll 30s linear infinite;
    white-space: nowrap;
}

@keyframes ticker-scroll {
    0%   { transform: translateX(100vw); }
    100% { transform: translateX(-100%); }
}

.ticker-item {
    display: inline-block;
    margin: 0 40px;
    font-size: 0.82rem;
    font-weight: 500;
    color: #e0e0e0;
}

.ticker-name  { color: #90caf9; margin-right: 6px; }
.ticker-price { color: #ffffff; font-weight: 600; margin-right: 4px; }
.ticker-up    { color: #4caf50; }
.ticker-down  { color: #f44336; }

/* ── Top Nav ── */
.topnav {
    background: #ffffff;
    border-bottom: 2px solid #f0f0f0;
    padding: 14px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.logo-section {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-icon {
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #1565c0, #42a5f5);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.logo-text {
    font-size: 1.4rem;
    font-weight: 800;
    color: #1a1a2e;
    letter-spacing: -0.5px;
}

.logo-dot { color: #1565c0; }

.nav-links {
    display: flex;
    gap: 32px;
    font-size: 0.9rem;
    font-weight: 500;
    color: #555;
}

.nav-link-active {
    color: #1565c0;
    border-bottom: 2px solid #1565c0;
    padding-bottom: 2px;
}

.nav-badge {
    background: #e3f2fd;
    color: #1565c0;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ── Landing Page ── */
.landing-hero {
    text-align: center;
    padding: 60px 40px 40px;
    animation: fadeInDown 0.7s ease;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    color: #1a1a2e;
    letter-spacing: -1px;
    margin-bottom: 12px;
}

.hero-title span { color: #1565c0; }

.hero-subtitle {
    font-size: 1.1rem;
    color: #666;
    max-width: 600px;
    margin: 0 auto 40px;
    line-height: 1.7;
}

/* ── Stock Cards on Landing ── */
.stock-select-card {
    background: #ffffff;
    border: 2px solid #e8e8e8;
    border-radius: 16px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.25s ease;
    text-align: left;
    margin-bottom: 12px;
    animation: fadeInUp 0.5s ease;
}

.stock-select-card:hover {
    border-color: #1565c0;
    box-shadow: 0 6px 24px rgba(21,101,192,0.15);
    transform: translateY(-3px);
}

.stock-select-card.selected {
    border-color: #1565c0;
    background: #e3f2fd;
}

/* ── Analysis Type Cards ── */
.analysis-card {
    background: #ffffff;
    border: 2px solid #e8e8e8;
    border-radius: 16px;
    padding: 24px 20px;
    cursor: pointer;
    transition: all 0.25s ease;
    text-align: center;
    animation: fadeInUp 0.6s ease;
}

.analysis-card:hover {
    border-color: #1565c0;
    box-shadow: 0 6px 24px rgba(21,101,192,0.15);
    transform: translateY(-3px);
}

.analysis-icon {
    font-size: 2rem;
    margin-bottom: 10px;
}

.analysis-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 6px;
}

.analysis-desc {
    font-size: 0.78rem;
    color: #888;
    line-height: 1.5;
}

/* ── Dashboard Cards ── */
.metric-card {
    background: #ffffff;
    border: 1.5px solid #eeeeee;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
    transition: all 0.2s ease;
    border-left: 4px solid #1565c0;
}

.metric-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}

.metric-value {
    font-size: 1.7rem;
    font-weight: 800;
    color: #1a1a2e;
    line-height: 1;
}

.metric-label {
    font-size: 0.75rem;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

.metric-change-pos { color: #4caf50; font-size: 0.82rem; font-weight: 600; margin-top: 6px; }
.metric-change-neg { color: #f44336; font-size: 0.82rem; font-weight: 600; margin-top: 6px; }

/* ── Section Headers ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #f0f0f0;
    animation: fadeIn 0.5s ease;
}

/* ── Pillar Cards (like EverythingMoney) ── */
.pillar-card {
    background: #ffffff;
    border: 1.5px solid #eeeeee;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
    animation: fadeInUp 0.5s ease;
}

.pillar-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}

.pillar-title {
    font-size: 0.8rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}

.pillar-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: #1a1a2e;
}

.pillar-sub {
    font-size: 0.75rem;
    color: #aaa;
    margin-top: 4px;
}

.progress-bg {
    background: #f0f0f0;
    border-radius: 6px;
    height: 7px;
    margin-top: 10px;
    overflow: hidden;
}

.progress-fill-green { background: #4caf50; height: 7px; border-radius: 6px; transition: width 0.8s ease; }
.progress-fill-red   { background: #f44336; height: 7px; border-radius: 6px; transition: width 0.8s ease; }
.progress-fill-blue  { background: #1565c0; height: 7px; border-radius: 6px; transition: width 0.8s ease; }

/* ── Signal Pills ── */
.pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.pill-buy  { background: #e8f5e9; color: #2e7d32; }
.pill-sell { background: #ffebee; color: #c62828; }
.pill-hold { background: #fff8e1; color: #f57f17; }

/* ── Stat Row ── */
.stat-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #f5f5f5;
    font-size: 0.875rem;
}
.stat-row:last-child { border-bottom: none; }
.stat-key   { color: #888; }
.stat-value { font-weight: 600; color: #1a1a2e; }

/* ── Pattern Row ── */
.pat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 14px;
    background: #f8f9fa;
    border-radius: 10px;
    margin-bottom: 8px;
    transition: background 0.2s;
}
.pat-row:hover { background: #e3f2fd; }

/* ── Screener Row ── */
.scr-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    background: #f8f9fa;
    border-radius: 12px;
    margin-bottom: 8px;
    transition: all 0.2s;
}
.scr-row:hover { background: #e3f2fd; transform: translateX(4px); }

/* ── CTA Button ── */
.cta-btn {
    background: linear-gradient(135deg, #1565c0, #42a5f5);
    color: white;
    border: none;
    padding: 14px 40px;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(21,101,192,0.3);
}
.cta-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(21,101,192,0.4);
}

/* ── Footer ── */
.footer {
    background: #1a1a2e;
    color: #90caf9;
    padding: 20px 40px;
    text-align: center;
    font-size: 0.82rem;
    margin-top: 40px;
    border-radius: 16px 16px 0 0;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #555;
    font-weight: 500;
    font-size: 0.875rem;
}

.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #1565c0 !important;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Streamlit widget styling */
div[data-testid="stSelectbox"] > div,
div[data-testid="stMultiSelect"] > div {
    border-radius: 10px;
    border-color: #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# ── Stock Universe ─────────────────────────────────────────────
NSE_STOCKS = {
    "HDFC Bank":          "HDFCBANK.NS",
    "Reliance":           "RELIANCE.NS",
    "TCS":                "TCS.NS",
    "Infosys":            "INFY.NS",
    "ICICI Bank":         "ICICIBANK.NS",
    "SBI":                "SBIN.NS",
    "Wipro":              "WIPRO.NS",
    "Bharti Airtel":      "BHARTIARTL.NS",
    "Kotak Bank":         "KOTAKBANK.NS",
    "Axis Bank":          "AXISBANK.NS",
    "ITC":                "ITC.NS",
    "Maruti":             "MARUTI.NS",
    "Bajaj Finance":      "BAJFINANCE.NS",
    "Sun Pharma":         "SUNPHARMA.NS",
    "Titan":              "TITAN.NS",
    "Asian Paints":       "ASIANPAINT.NS",
    "UltraTech Cement":   "ULTRACEMCO.NS",
    "Tata Motors":        "TATAMOTORS.NS",
    "Adani Ports":        "ADANIPORTS.NS",
    "Power Grid":         "POWERGRID.NS",
}

BSE_STOCKS = {
    "BSE: HDFC Bank":     "HDFCBANK.BO",
    "BSE: Reliance":      "RELIANCE.BO",
    "BSE: TCS":           "TCS.BO",
    "BSE: Infosys":       "INFY.BO",
    "BSE: ICICI Bank":    "ICICIBANK.BO",
    "BSE: SBI":           "SBIN.BO",
    "BSE: Wipro":         "WIPRO.BO",
    "BSE: ITC":           "ITC.BO",
    "BSE: Maruti":        "MARUTI.BO",
    "BSE: Sun Pharma":    "SUNPHARMA.BO",
}

ALL_STOCKS = {**NSE_STOCKS, **BSE_STOCKS}

ANALYSIS_TYPES = {
    "📊 Dashboard":       "Full price action dashboard with all indicators",
    "🔍 Stock Screener":  "Filter stocks by RSI, MACD and other indicators",
    "⚖️ Comparison":      "Compare two stocks side by side",
    "💼 Portfolio":       "Track and analyse your portfolio P&L",
}

# ── Data Fetchers ──────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_index_prices():
    indices = {
        "SENSEX":   "^BSESN",
        "NIFTY 50": "^NSEI",
        "FINNIFTY": "NIFTY_FIN_SERVICE.NS",
        "BANKNIFTY":"^NSEBANK",
    }
    results = {}
    for name, ticker in indices.items():
        try:
            d = yf.download(ticker, period="2d", interval="1d",
                           auto_adjust=True, progress=False)
            if not d.empty and len(d) >= 2:
                if isinstance(d.columns, pd.MultiIndex):
                    d.columns = d.columns.get_level_values(0)
                cur  = float(d['Close'].iloc[-1])
                prev = float(d['Close'].iloc[-2])
                chg  = ((cur - prev) / prev) * 100
                results[name] = (cur, chg)
        except Exception:
            results[name] = (0, 0)
    return results

@st.cache_data(ttl=3600)
def fetch_stock(ticker, start, end):
    try:
        df = yf.download(ticker, start=start, end=end,
                        auto_adjust=True, progress=False)
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.index = pd.to_datetime(df.index)
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df.drop(columns=["Dividends","Stock Splits"], inplace=True, errors='ignore')
        return df
    except Exception:
        return pd.DataFrame()

def compute_indicators(df, rsi_p=14, bb_p=20):
    df = df.copy()
    df['SMA_20']   = df['Close'].rolling(20).mean()
    df['SMA_50']   = df['Close'].rolling(50).mean()
    df['SMA_200']  = df['Close'].rolling(200).mean()
    df['EMA_20']   = df['Close'].ewm(span=20, adjust=False).mean()
    df['BB_Mid']   = df['Close'].rolling(bb_p).mean()
    df['BB_Std']   = df['Close'].rolling(bb_p).std()
    df['BB_Upper'] = df['BB_Mid'] + 2 * df['BB_Std']
    df['BB_Lower'] = df['BB_Mid'] - 2 * df['BB_Std']
    df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Mid'] * 100
    delta = df['Close'].diff()
    gain  = delta.where(delta > 0, 0).rolling(rsi_p).mean()
    loss  = -delta.where(delta < 0, 0).rolling(rsi_p).mean()
    df['RSI']         = 100 - (100 / (1 + gain / loss))
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD']        = ema12 - ema26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist']   = df['MACD'] - df['MACD_Signal']
    df['Daily_Return']= df['Close'].pct_change() * 100
    df['Volatility']  = df['Daily_Return'].rolling(20).std()
    df['VWAP']        = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    tr1 = df['High'] - df['Low']
    tr2 = abs(df['High'] - df['Close'].shift())
    tr3 = abs(df['Low']  - df['Close'].shift())
    df['ATR']           = pd.concat([tr1,tr2,tr3], axis=1).max(axis=1).rolling(14).mean()
    df['Body']          = abs(df['Close'] - df['Open'])
    df['Body_Range']    = df['High'] - df['Low']
    df['Upper_Shadow']  = df['High'] - df[['Close','Open']].max(axis=1)
    df['Lower_Shadow']  = df[['Close','Open']].min(axis=1) - df['Low']
    df['Doji']              = df['Body'] <= 0.1 * df['Body_Range']
    df['Hammer']            = (df['Lower_Shadow']>=2*df['Body']) & (df['Upper_Shadow']<=0.1*df['Body_Range']) & (df['Body']>0)
    df['Shooting_Star']     = (df['Upper_Shadow']>=2*df['Body']) & (df['Lower_Shadow']<=0.1*df['Body_Range']) & (df['Body']>0)
    df['Bullish_Engulfing'] = (df['Close']>df['Open']) & (df['Close'].shift(1)<df['Open'].shift(1)) & (df['Close']>df['Open'].shift(1)) & (df['Open']<df['Close'].shift(1))
    df['Bearish_Engulfing'] = (df['Close']<df['Open']) & (df['Close'].shift(1)>df['Open'].shift(1)) & (df['Close']<df['Open'].shift(1)) & (df['Open']>df['Close'].shift(1))
    df['Month'] = df.index.month
    df['Year']  = df.index.year
    return df

# ── Session State ──────────────────────────────────────────────
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = 'HDFC Bank'
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = 'HDFCBANK.NS'
if 'analysis_type' not in st.session_state:
    st.session_state.analysis_type = '📊 Dashboard'
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# ── Ticker Bar ─────────────────────────────────────────────────
index_data = get_index_prices()
ticker_items = ""
for name, (price, chg) in index_data.items():
    arrow = "▲" if chg >= 0 else "▼"
    color_cls = "ticker-up" if chg >= 0 else "ticker-down"
    ticker_items += f"""
    <span class='ticker-item'>
        <span class='ticker-name'>{name}</span>
        <span class='ticker-price'>{price:,.2f}</span>
        <span class='{color_cls}'>{arrow} {abs(chg):.2f}%</span>
    </span>
    """

st.markdown(f"""
<div class='ticker-wrapper'>
    <div class='ticker-track'>
        {ticker_items * 4}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Top Nav ────────────────────────────────────────────────────
nav_tabs = {
    "landing":   "Home",
    "dashboard": "Dashboard",
    "screener":  "Screener",
    "compare":   "Compare",
    "portfolio": "Portfolio",
}

active_page = st.session_state.page
nav_html = "".join([
    f"<span class='nav-link-active'>{label}</span>" if key == active_page
    else f"<span style='cursor:pointer;color:#555;'>{label}</span>"
    for key, label in nav_tabs.items()
])

st.markdown(f"""
<div class='topnav'>
    <div class='logo-section'>
        <div class='logo-icon'>🔭</div>
        <div class='logo-text'>Stock<span class='logo-dot'>Lens</span></div>
    </div>
    <div class='nav-links'>
        {nav_html}
    </div>
    <div class='nav-badge'>Indian Markets</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════
if st.session_state.page == 'landing':

    st.markdown("""
    <div class='landing-hero'>
        <h1 class='hero-title'>Analyse Indian Stocks<br>Like a <span>Pro</span></h1>
        <p class='hero-subtitle'>
            Real-time price action, technical indicators, pattern detection
            and portfolio tracking — all in one place.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Step 1 — Select Stock
    st.markdown("""
    <div style='max-width:900px;margin:0 auto;padding:0 20px;'>
        <div style='font-size:0.8rem;font-weight:700;color:#1565c0;
        text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>
        Step 1 — Select a stock
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 4, 1])
    with center:
        exchange = st.radio("Exchange", ["NSE", "BSE"], horizontal=True, label_visibility="collapsed")
        stock_universe = NSE_STOCKS if exchange == "NSE" else BSE_STOCKS

        cols = st.columns(4)
        for i, (name, ticker) in enumerate(stock_universe.items()):
            with cols[i % 4]:
                is_selected = st.session_state.selected_stock == name
                border_color = "#1565c0" if is_selected else "#e8e8e8"
                bg_color     = "#e3f2fd" if is_selected else "#ffffff"
                if st.button(f"{'✅ ' if is_selected else ''}{name}",
                             key=f"stock_{name}",
                             use_container_width=True):
                    st.session_state.selected_stock  = name
                    st.session_state.selected_ticker = ticker
                    st.rerun()

        # Custom ticker
        st.markdown("<br>", unsafe_allow_html=True)
        custom_col1, custom_col2 = st.columns([3,1])
        with custom_col1:
            custom = st.text_input("Or enter a custom ticker (e.g. TATASTEEL.NS)",
                                   placeholder="TATASTEEL.NS",
                                   label_visibility="visible")
        with custom_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Use Ticker", use_container_width=True) and custom.strip():
                st.session_state.selected_stock  = custom.strip().upper()
                st.session_state.selected_ticker = custom.strip().upper()
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Step 2 — Analysis Type
    st.markdown("""
    <div style='max-width:900px;margin:0 auto;padding:0 20px;'>
        <div style='font-size:0.8rem;font-weight:700;color:#1565c0;
        text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;'>
        Step 2 — Choose analysis type
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, center2, _ = st.columns([1, 4, 1])
    with center2:
        a1, a2, a3, a4 = st.columns(4)
        analysis_map = {
            a1: ("📊", "Dashboard",      "Full price action with all indicators",  "dashboard"),
            a2: ("🔍", "Stock Screener", "Filter stocks by RSI, MACD & more",      "screener"),
            a3: ("⚖️", "Comparison",     "Compare two stocks side by side",         "compare"),
            a4: ("💼", "Portfolio",      "Track your holdings & P&L",              "portfolio"),
        }
        for col, (icon, title, desc, page_key) in analysis_map.items():
            with col:
                is_sel = st.session_state.analysis_type == title
                bg     = "#e3f2fd" if is_sel else "#ffffff"
                border = "#1565c0" if is_sel else "#e8e8e8"
                st.markdown(f"""
                <div class='analysis-card' style='border-color:{border};background:{bg};'>
                    <div class='analysis-icon'>{icon}</div>
                    <div class='analysis-title'>{title}</div>
                    <div class='analysis-desc'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {title}", key=f"analysis_{page_key}", use_container_width=True):
                    st.session_state.analysis_type = title
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Step 3 — Date Range
    st.markdown("""
    <div style='max-width:900px;margin:0 auto;padding:0 20px;'>
        <div style='font-size:0.8rem;font-weight:700;color:#1565c0;
        text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>
        Step 3 — Set date range
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, center3, _ = st.columns([1, 4, 1])
    with center3:
        d1, d2 = st.columns(2)
        with d1:
            st.session_state.start_date = st.date_input(
                "From", pd.to_datetime("2020-01-01"))
        with d2:
            st.session_state.end_date = st.date_input(
                "To", pd.to_datetime("2025-03-21"))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Launch Button
    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        sel_stock    = st.session_state.selected_stock
        sel_analysis = st.session_state.analysis_type
        page_map = {
            "Dashboard":      "dashboard",
            "Stock Screener": "screener",
            "Comparison":     "compare",
            "Portfolio":      "portfolio",
        }
        if st.button(
            f"🚀 Analyse {sel_stock} →",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.page = page_map.get(sel_analysis, "dashboard")
            st.rerun()

    # Stats row
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display:flex;justify-content:center;gap:60px;padding:30px;
    background:#f8f9fa;border-radius:16px;max-width:700px;margin:0 auto;
    animation: fadeInUp 0.8s ease;'>
        <div style='text-align:center;'>
            <div style='font-size:1.8rem;font-weight:800;color:#1565c0;'>30+</div>
            <div style='font-size:0.8rem;color:#888;margin-top:4px;'>NSE & BSE Stocks</div>
        </div>
        <div style='text-align:center;'>
            <div style='font-size:1.8rem;font-weight:800;color:#1565c0;'>10+</div>
            <div style='font-size:0.8rem;color:#888;margin-top:4px;'>Technical Indicators</div>
        </div>
        <div style='text-align:center;'>
            <div style='font-size:1.8rem;font-weight:800;color:#1565c0;'>5</div>
            <div style='font-size:0.8rem;color:#888;margin-top:4px;'>Candlestick Patterns</div>
        </div>
        <div style='text-align:center;'>
            <div style='font-size:1.8rem;font-weight:800;color:#1565c0;'>Live</div>
            <div style='font-size:0.8rem;color:#888;margin-top:4px;'>Market Data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == 'dashboard':

    start = getattr(st.session_state, 'start_date', pd.to_datetime("2020-01-01"))
    end   = getattr(st.session_state, 'end_date',   pd.to_datetime("2025-03-21"))

    # Back button
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()

    with st.spinner(f"Loading {st.session_state.selected_stock}..."):
        raw = fetch_stock(st.session_state.selected_ticker, start, end)

    if raw.empty:
        st.error(f"Could not fetch data for {st.session_state.selected_ticker}")
        st.stop()

    df = compute_indicators(raw)

    cur       = float(df['Close'].iloc[-1])
    prev      = float(df['Close'].iloc[-2])
    chg       = cur - prev
    chgp      = chg / prev * 100
    rsi       = float(df['RSI'].iloc[-1])
    macd      = float(df['MACD'].iloc[-1])
    hi52      = float(df['High'].tail(252).max())
    lo52      = float(df['Low'].tail(252).min())
    total_ret = ((cur / float(df['Close'].iloc[0])) - 1) * 100
    sharpe    = df['Daily_Return'].mean() / df['Daily_Return'].std() * np.sqrt(252)
    max_dd    = ((df['Close'] / df['Close'].cummax()) - 1).min() * 100
    vol_colors= ['#4caf50' if float(c)>=float(o) else '#f44336'
                 for c, o in zip(df['Close'], df['Open'])]

    # Stock Header
    st.markdown(f"""
    <div style='padding:20px 0;animation:fadeInDown 0.5s ease;'>
        <div style='display:flex;align-items:center;gap:16px;'>
            <div style='width:52px;height:52px;background:linear-gradient(135deg,#1565c0,#42a5f5);
            border-radius:14px;display:flex;align-items:center;justify-content:center;
            font-size:1.4rem;'>📈</div>
            <div>
                <div style='font-size:1.6rem;font-weight:800;color:#1a1a2e;'>
                    {st.session_state.selected_stock}
                    <span style='font-size:0.9rem;font-weight:400;color:#888;margin-left:8px;'>
                    {st.session_state.selected_ticker}</span>
                </div>
                <div style='font-size:0.85rem;color:#888;'>
                    {df.index[0].strftime('%d %b %Y')} — {df.index[-1].strftime('%d %b %Y')}
                    &nbsp;·&nbsp; {len(df)} trading days
                </div>
            </div>
            <div style='margin-left:auto;text-align:right;'>
                <div style='font-size:2rem;font-weight:800;color:#1a1a2e;'>₹{cur:,.2f}</div>
                <div style='font-size:1rem;font-weight:600;color:{"#4caf50" if chg>=0 else "#f44336"}'>
                    {'▲' if chg>=0 else '▼'} ₹{abs(chg):.2f} ({chgp:+.2f}%)
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "📈 Indicators", "🕯️ Patterns", "📦 Volume & Volatility", "📋 Data"
    ])

    with tab1:
        # KPI Cards
        k1,k2,k3,k4,k5,k6 = st.columns(6)
        kpis = [
            (k1, f"₹{cur:,.2f}",        "Current Price",  f"{'▲' if chg>=0 else '▼'} {chgp:+.2f}%",    chg>=0,   "#1565c0"),
            (k2, f"₹{hi52:,.2f}",        "52W High",       f"{((cur/hi52)-1)*100:.1f}% from high",       False,    "#e53935"),
            (k3, f"₹{lo52:,.2f}",        "52W Low",        f"{((cur/lo52)-1)*100:.1f}% above low",       True,     "#43a047"),
            (k4, f"{rsi:.1f}",           "RSI (14)",       "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral", rsi<=70, "#7b1fa2"),
            (k5, f"{total_ret:.1f}%",    "Total Return",   f"Since {df.index[0].strftime('%b %Y')}",     total_ret>0, "#0288d1"),
            (k6, f"{sharpe:.2f}",        "Sharpe Ratio",   "Risk-adjusted return",                       sharpe>1, "#00796b"),
        ]
        for col, val, label, sub, pos, border in kpis:
            color = "#4caf50" if pos else "#f44336"
            col.markdown(f"""
            <div class='metric-card' style='border-left-color:{border};'>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div>
                <div style='color:{color};font-size:0.78rem;font-weight:600;margin-top:6px;'>{sub}</div>
            </div>""", unsafe_allow_html=True)

        # Signals Row
        st.markdown("<div class='section-header'>🚦 Technical Signals</div>", unsafe_allow_html=True)
        rsi_sig  = ("BUY","pill-buy")   if rsi<30   else ("SELL","pill-sell") if rsi>70  else ("HOLD","pill-hold")
        macd_sig = ("BUY","pill-buy")   if macd>0   else ("SELL","pill-sell")
        sma_sig  = ("BUY","pill-buy")   if cur>float(df['SMA_200'].iloc[-1]) else ("SELL","pill-sell")
        bb_low   = float(df['BB_Lower'].iloc[-1])
        bb_up    = float(df['BB_Upper'].iloc[-1])
        bb_pos   = (cur - bb_low) / (bb_up - bb_low)
        bb_sig   = ("BUY","pill-buy")   if bb_pos<0.2 else ("SELL","pill-sell") if bb_pos>0.8 else ("HOLD","pill-hold")

        sig1,sig2,sig3,sig4,sig5 = st.columns(5)
        signals = [
            (sig1, f"RSI ({rsi:.0f})",    rsi_sig),
            (sig2, "MACD",               macd_sig),
            (sig3, "SMA 200 Trend",      sma_sig),
            (sig4, "Bollinger Position", bb_sig),
            (sig5, "Overall",            ("BUY","pill-buy") if sum([rsi_sig[0]=="BUY", macd_sig[0]=="BUY", sma_sig[0]=="BUY"])>=2 else ("SELL","pill-sell") if sum([rsi_sig[0]=="SELL", macd_sig[0]=="SELL", sma_sig[0]=="SELL"])>=2 else ("HOLD","pill-hold")),
        ]
        for col, label, sig in signals:
            col.markdown(f"""
            <div style='background:#f8f9fa;border-radius:12px;padding:16px;text-align:center;'>
                <div style='font-size:0.78rem;color:#888;margin-bottom:8px;'>{label}</div>
                <span class='pill {sig[1]}'>{sig[0]}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Main Chart
        st.markdown("<div class='section-header'>💹 Price Chart</div>", unsafe_allow_html=True)
        chart_type = st.selectbox("Chart Type", ["Candlestick","Line","OHLC"], label_visibility="collapsed")
        show_sma   = st.checkbox("SMA (20/50/200)", value=True)
        show_bb    = st.checkbox("Bollinger Bands", value=True)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.75, 0.25], vertical_spacing=0.02)

        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'], name=st.session_state.selected_stock,
                increasing_line_color='#4caf50', decreasing_line_color='#f44336'
            ), row=1, col=1)
        elif chart_type == "OHLC":
            fig.add_trace(go.Ohlc(
                x=df.index, open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close']
            ), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['Close'],
                line=dict(color='#1565c0', width=2),
                fill='tozeroy', fillcolor='rgba(21,101,192,0.06)'
            ), row=1, col=1)

        if show_sma:
            for cn, color, nm in [('SMA_20','#ff9800','SMA 20'),('SMA_50','#4caf50','SMA 50'),('SMA_200','#f44336','SMA 200')]:
                fig.add_trace(go.Scatter(x=df.index, y=df[cn], name=nm,
                                         line=dict(color=color, width=1.2)), row=1, col=1)
        if show_bb:
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'],
                                     line=dict(color='rgba(100,100,100,0.3)', width=0.8), name='BB Upper'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'],
                                     line=dict(color='rgba(100,100,100,0.3)', width=0.8),
                                     fill='tonexty', fillcolor='rgba(100,100,100,0.04)', name='BB Lower'), row=1, col=1)

        fig.add_trace(go.Bar(x=df.index, y=df['Volume'],
                             marker_color=vol_colors, opacity=0.6, name='Volume'), row=2, col=1)

        fig.update_layout(
            height=560, template='plotly_white',
            xaxis_rangeslider_visible=False,
            paper_bgcolor='white', plot_bgcolor='white',
            font=dict(family='Inter', color='#1a1a2e', size=11),
            legend=dict(orientation='h', yanchor='bottom', y=1.01,
                        bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=10, b=0)
        )
        for i in range(1,3):
            fig.update_xaxes(gridcolor='#f5f5f5', row=i, col=1)
            fig.update_yaxes(gridcolor='#f5f5f5', row=i, col=1)
        st.plotly_chart(fig, use_container_width=True)

        # Stats Grid
        st.markdown("<div class='section-header'>📐 Statistical Summary</div>", unsafe_allow_html=True)
        sg1, sg2, sg3 = st.columns(3)

        with sg1:
            st.markdown("""<div style='background:#f8f9fa;border-radius:14px;padding:20px;'>
            <div class='section-header'>Price Stats</div>""", unsafe_allow_html=True)
            for k, v in [
                ("Mean Price",   f"₹{df['Close'].mean():.2f}"),
                ("Median",       f"₹{df['Close'].median():.2f}"),
                ("Std Dev",      f"₹{df['Close'].std():.2f}"),
                ("Skewness",     f"{df['Close'].skew():.3f}"),
                ("Kurtosis",     f"{df['Close'].kurt():.3f}"),
            ]:
                st.markdown(f"<div class='stat-row'><span class='stat-key'>{k}</span><span class='stat-value'>{v}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with sg2:
            st.markdown("""<div style='background:#f8f9fa;border-radius:14px;padding:20px;'>
            <div class='section-header'>Return Analysis</div>""", unsafe_allow_html=True)
            for k, v, pos in [
                ("Total Return",    f"{total_ret:.2f}%",                               total_ret>0),
                ("Best Day",        f"+{df['Daily_Return'].max():.2f}%",               True),
                ("Worst Day",       f"{df['Daily_Return'].min():.2f}%",                False),
                ("Avg Daily",       f"{df['Daily_Return'].mean():.3f}%",               df['Daily_Return'].mean()>0),
                ("Max Drawdown",    f"{max_dd:.2f}%",                                  False),
                ("Sharpe Ratio",    f"{sharpe:.2f}",                                   sharpe>1),
            ]:
                color = "#4caf50" if pos else "#f44336"
                st.markdown(f"<div class='stat-row'><span class='stat-key'>{k}</span><span class='stat-value' style='color:{color};'>{v}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with sg3:
            st.markdown("""<div style='background:#f8f9fa;border-radius:14px;padding:20px;'>
            <div class='section-header'>Technical Levels</div>""", unsafe_allow_html=True)
            for k, v in [
                ("52W High",       f"₹{hi52:,.2f}"),
                ("52W Low",        f"₹{lo52:,.2f}"),
                ("SMA 20",         f"₹{float(df['SMA_20'].iloc[-1]):,.2f}"),
                ("SMA 50",         f"₹{float(df['SMA_50'].iloc[-1]):,.2f}"),
                ("SMA 200",        f"₹{float(df['SMA_200'].iloc[-1]):,.2f}"),
                ("BB Upper",       f"₹{bb_up:,.2f}"),
                ("BB Lower",       f"₹{bb_low:,.2f}"),
            ]:
                st.markdown(f"<div class='stat-row'><span class='stat-key'>{k}</span><span class='stat-value'>{v}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='section-header'>📈 Technical Indicators</div>", unsafe_allow_html=True)

        # RSI Chart
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI',
                                     line=dict(color='#1565c0', width=2),
                                     fill='tozeroy', fillcolor='rgba(21,101,192,0.06)'))
        fig_rsi.add_hrect(y0=70, y1=100, fillcolor='rgba(244,67,54,0.06)', line_width=0)
        fig_rsi.add_hrect(y0=0,  y1=30,  fillcolor='rgba(76,175,80,0.06)', line_width=0)
        fig_rsi.add_hline(y=70, line_dash='dash', line_color='#f44336', line_width=1.2,
                          annotation_text="Overbought (70)", annotation_font_color='#f44336')
        fig_rsi.add_hline(y=30, line_dash='dash', line_color='#4caf50', line_width=1.2,
                          annotation_text="Oversold (30)", annotation_font_color='#4caf50')
        fig_rsi.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                              height=280, title="RSI (14)", font=dict(family='Inter', color='#1a1a2e'),
                              margin=dict(l=0,r=0,t=40,b=0), showlegend=False)
        fig_rsi.update_xaxes(gridcolor='#f5f5f5')
        fig_rsi.update_yaxes(gridcolor='#f5f5f5', range=[0,100])
        st.plotly_chart(fig_rsi, use_container_width=True)

        # MACD Chart
        fig_macd = make_subplots(rows=1, cols=1)
        fig_macd.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'], name='Histogram',
                                  marker_color=['#4caf50' if v>=0 else '#f44336' for v in df['MACD_Hist']], opacity=0.7))
        fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD',
                                      line=dict(color='#1565c0', width=1.5)))
        fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal',
                                      line=dict(color='#f44336', width=1.5)))
        fig_macd.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                               height=280, title="MACD (12,26,9)", font=dict(family='Inter', color='#1a1a2e'),
                               margin=dict(l=0,r=0,t=40,b=0),
                               legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
        fig_macd.update_xaxes(gridcolor='#f5f5f5')
        fig_macd.update_yaxes(gridcolor='#f5f5f5')
        st.plotly_chart(fig_macd, use_container_width=True)

        # Bollinger Bands
        fig_bb = go.Figure()
        fig_bb.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='Upper Band',
                                    line=dict(color='#f44336', width=1, dash='dot')))
        fig_bb.add_trace(go.Scatter(x=df.index, y=df['BB_Mid'], name='Middle Band',
                                    line=dict(color='#1565c0', width=1.5)))
        fig_bb.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='Lower Band',
                                    line=dict(color='#4caf50', width=1, dash='dot'),
                                    fill='tonexty', fillcolor='rgba(21,101,192,0.05)'))
        fig_bb.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close',
                                    line=dict(color='#1a1a2e', width=1), opacity=0.8))
        fig_bb.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                             height=300, title="Bollinger Bands (20, 2σ)",
                             font=dict(family='Inter', color='#1a1a2e'),
                             margin=dict(l=0,r=0,t=40,b=0),
                             legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
        fig_bb.update_xaxes(gridcolor='#f5f5f5')
        fig_bb.update_yaxes(gridcolor='#f5f5f5')
        st.plotly_chart(fig_bb, use_container_width=True)

        # Monthly Heatmap
        st.markdown("<div class='section-header'>🗓️ Monthly Returns Heatmap</div>", unsafe_allow_html=True)
        month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
        monthly = df.groupby(['Year','Month'])['Daily_Return'].sum().unstack()
        monthly.columns = [month_names[m] for m in monthly.columns]
        fig_heat = px.imshow(monthly, color_continuous_scale='RdYlGn',
                             aspect='auto', text_auto='.1f')
        fig_heat.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                               height=280, margin=dict(l=0,r=0,t=0,b=0),
                               font=dict(family='Inter', color='#1a1a2e'),
                               coloraxis_showscale=True)
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab3:
        st.markdown("<div class='section-header'>🕯️ Candlestick Pattern Detection</div>", unsafe_allow_html=True)

        # Pattern Chart
        fig_pat = go.Figure()
        fig_pat.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            increasing_line_color='#4caf50', decreasing_line_color='#f44336',
            name='Price'
        ))
        for pat, sym, color, pos in [
            ('Doji',             'circle-open',  '#ff9800', 'high'),
            ('Hammer',           'triangle-up',  '#4caf50', 'low'),
            ('Shooting_Star',    'triangle-down','#f44336', 'high'),
            ('Bullish_Engulfing','star',          '#4caf50', 'low'),
            ('Bearish_Engulfing','star',          '#f44336', 'high'),
        ]:
            pat_df = df[df[pat]]
            y_vals = pat_df['Low']*0.985 if pos=='low' else pat_df['High']*1.015
            fig_pat.add_trace(go.Scatter(
                x=pat_df.index, y=y_vals, mode='markers', name=pat,
                marker=dict(symbol=sym, color=color, size=10)
            ))
        fig_pat.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                              height=450, xaxis_rangeslider_visible=False,
                              font=dict(family='Inter', color='#1a1a2e'),
                              legend=dict(orientation='h', y=1.01, bgcolor='rgba(0,0,0,0)'),
                              margin=dict(l=0,r=0,t=10,b=0))
        fig_pat.update_xaxes(gridcolor='#f5f5f5')
        fig_pat.update_yaxes(gridcolor='#f5f5f5')
        st.plotly_chart(fig_pat, use_container_width=True)

        # Pattern Summary Cards
        pc1,pc2,pc3,pc4,pc5 = st.columns(5)
        pats = [
            (pc1, "🟡", "Doji",              int(df['Doji'].sum()),              "#ff9800"),
            (pc2, "🟢", "Hammer",            int(df['Hammer'].sum()),            "#4caf50"),
            (pc3, "🔴", "Shooting Star",     int(df['Shooting_Star'].sum()),     "#f44336"),
            (pc4, "🟢", "Bull Engulfing",    int(df['Bullish_Engulfing'].sum()), "#4caf50"),
            (pc5, "🔴", "Bear Engulfing",    int(df['Bearish_Engulfing'].sum()), "#f44336"),
        ]
        for col, icon, name, count, color in pats:
            col.markdown(f"""
            <div style='background:#f8f9fa;border-radius:14px;padding:20px;text-align:center;
            border-top:4px solid {color};'>
                <div style='font-size:1.8rem;'>{icon}</div>
                <div style='font-size:1.6rem;font-weight:800;color:{color};'>{count}</div>
                <div style='font-size:0.75rem;color:#888;margin-top:4px;'>{name}</div>
            </div>""", unsafe_allow_html=True)

    with tab4:
        st.markdown("<div class='section-header'>📦 Volume & Volatility Analysis</div>", unsafe_allow_html=True)

        v1, v2 = st.columns(2)
        with v1:
            df['Vol_MA20'] = df['Volume'].rolling(20).mean()
            fig_v = go.Figure()
            fig_v.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
                                   marker_color=vol_colors, opacity=0.5))
            fig_v.add_trace(go.Scatter(x=df.index, y=df['Vol_MA20'], name='MA 20',
                                       line=dict(color='#1565c0', width=2)))
            fig_v.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                                height=280, title="Volume with MA 20",
                                font=dict(family='Inter', color='#1a1a2e'), margin=dict(l=0,r=0,t=40,b=0),
                                legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
            fig_v.update_xaxes(gridcolor='#f5f5f5')
            fig_v.update_yaxes(gridcolor='#f5f5f5')
            st.plotly_chart(fig_v, use_container_width=True)

        with v2:
            fig_vola = go.Figure()
            fig_vola.add_trace(go.Scatter(x=df.index, y=df['Volatility'], name='Volatility',
                                          fill='tozeroy', fillcolor='rgba(123,31,162,0.08)',
                                          line=dict(color='#7b1fa2', width=2)))
            fig_vola.add_hline(y=float(df['Volatility'].mean()), line_dash='dash',
                               line_color='#ff9800', annotation_text="Mean",
                               annotation_font_color='#ff9800')
            fig_vola.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                                   height=280, title="Rolling 20-day Volatility",
                                   font=dict(family='Inter', color='#1a1a2e'), margin=dict(l=0,r=0,t=40,b=0),
                                   showlegend=False)
            fig_vola.update_xaxes(gridcolor='#f5f5f5')
            fig_vola.update_yaxes(gridcolor='#f5f5f5')
            st.plotly_chart(fig_vola, use_container_width=True)

        # Returns Distribution
        fig_ret = px.histogram(df['Daily_Return'].dropna(), nbins=60,
                               color_discrete_sequence=['#1565c0'],
                               title="Daily Returns Distribution")
        fig_ret.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                              height=280, font=dict(family='Inter', color='#1a1a2e'),
                              showlegend=False, margin=dict(l=0,r=0,t=40,b=0))
        fig_ret.update_xaxes(gridcolor='#f5f5f5', title="Daily Return (%)")
        fig_ret.update_yaxes(gridcolor='#f5f5f5')
        st.plotly_chart(fig_ret, use_container_width=True)

    with tab5:
        st.markdown("<div class='section-header'>📋 Raw Data Explorer</div>", unsafe_allow_html=True)
        e1, e2 = st.columns([3,1])
        with e1:
            show_cols = st.multiselect("Select columns",
                options=['Open','High','Low','Close','Volume','RSI','MACD','BB_Upper',
                         'BB_Lower','SMA_20','SMA_50','SMA_200','EMA_20','ATR','Volatility','Daily_Return'],
                default=['Open','High','Low','Close','Volume','RSI','MACD'])
        with e2:
            n_rows = st.slider("Rows", 10, 100, 30)
        st.dataframe(df[show_cols].tail(n_rows).round(2).sort_index(ascending=False),
                     use_container_width=True)

# ══════════════════════════════════════════════════════════════
# SCREENER PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == 'screener':
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()

    start = getattr(st.session_state, 'start_date', pd.to_datetime("2020-01-01"))
    end   = getattr(st.session_state, 'end_date',   pd.to_datetime("2025-03-21"))

    st.markdown("""
    <div style='padding:20px 0 10px;animation:fadeInDown 0.5s ease;'>
        <h2 style='font-size:1.8rem;font-weight:800;color:#1a1a2e;margin:0;'>🔍 Stock Screener</h2>
        <p style='color:#888;margin-top:4px;'>Filter NSE stocks by technical indicators</p>
    </div>
    """, unsafe_allow_html=True)

    sc1,sc2,sc3,sc4 = st.columns(4)
    with sc1:
        rsi_min = st.slider("RSI Min", 0, 100, 0)
        rsi_max = st.slider("RSI Max", 0, 100, 100)
    with sc2:
        ret_min = st.slider("Min Return %", -100, 200, -100)
        ret_max = st.slider("Max Return %", -100, 200, 200)
    with sc3:
        trend_filter = st.selectbox("Trend", ["All","Above SMA200","Below SMA200"])
        macd_filter  = st.selectbox("MACD",  ["All","Bullish","Bearish"])
    with sc4:
        st.markdown("<br><br>", unsafe_allow_html=True)
        run_screen = st.button("🔍 Run Screener", use_container_width=True, type="primary")

    if run_screen:
        results = []
        progress = st.progress(0)
        nse_list = list(NSE_STOCKS.items())
        for i, (name, ticker) in enumerate(nse_list):
            progress.progress((i+1)/len(nse_list), text=f"Scanning {name}...")
            try:
                raw = fetch_stock(ticker, start, end)
                if raw.empty or len(raw) < 50:
                    continue
                d = compute_indicators(raw)
                cur_p  = float(d['Close'].iloc[-1])
                rsi_v  = float(d['RSI'].iloc[-1])
                macd_v = float(d['MACD'].iloc[-1])
                ret_v  = ((cur_p / float(d['Close'].iloc[0])) - 1) * 100
                sma200 = float(d['SMA_200'].iloc[-1])
                vol_v  = float(d['Volatility'].iloc[-1])
                if not (rsi_min<=rsi_v<=rsi_max):  continue
                if not (ret_min<=ret_v<=ret_max):   continue
                if trend_filter=="Above SMA200" and cur_p<=sma200: continue
                if trend_filter=="Below SMA200" and cur_p>=sma200: continue
                if macd_filter=="Bullish" and macd_v<=0: continue
                if macd_filter=="Bearish" and macd_v>=0: continue
                signal = "BUY" if rsi_v<40 and macd_v>0 else "SELL" if rsi_v>60 and macd_v<0 else "HOLD"
                results.append({
                    "name": name, "ticker": ticker, "price": cur_p,
                    "rsi": rsi_v, "macd": macd_v, "ret": ret_v,
                    "vol": vol_v, "signal": signal
                })
            except Exception:
                continue
        progress.empty()

        if results:
            st.markdown(f"""
            <div style='background:#e3f2fd;border-radius:12px;padding:12px 20px;margin-bottom:16px;'>
                <span style='font-weight:700;color:#1565c0;'>✅ {len(results)} stocks matched your criteria</span>
            </div>""", unsafe_allow_html=True)
            for r in results:
                sig_cls   = "pill-buy" if r['signal']=="BUY" else "pill-sell" if r['signal']=="SELL" else "pill-hold"
                ret_color = "#4caf50" if r['ret']>=0 else "#f44336"
                st.markdown(f"""
                <div class='scr-row'>
                    <div style='flex:2;'>
                        <div style='font-weight:700;color:#1a1a2e;font-size:0.95rem;'>{r['name']}</div>
                        <div style='color:#888;font-size:0.75rem;'>{r['ticker']}</div>
                    </div>
                    <div style='flex:1;text-align:center;'>
                        <div style='font-weight:700;color:#1a1a2e;'>₹{r['price']:,.2f}</div>
                    </div>
                    <div style='flex:1;text-align:center;color:#555;'>RSI: {r['rsi']:.1f}</div>
                    <div style='flex:1;text-align:center;font-weight:600;color:{ret_color};'>
                        {"+" if r['ret']>=0 else ""}{r['ret']:.1f}%
                    </div>
                    <div style='flex:1;text-align:right;'>
                        <span class='pill {sig_cls}'>{r['signal']}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.warning("No stocks matched. Try widening your filters.")

# ══════════════════════════════════════════════════════════════
# COMPARE PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == 'compare':
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()

    start = getattr(st.session_state, 'start_date', pd.to_datetime("2020-01-01"))
    end   = getattr(st.session_state, 'end_date',   pd.to_datetime("2025-03-21"))

    st.markdown("""
    <div style='padding:20px 0 10px;animation:fadeInDown 0.5s ease;'>
        <h2 style='font-size:1.8rem;font-weight:800;color:#1a1a2e;margin:0;'>⚖️ Stock Comparison</h2>
        <p style='color:#888;margin-top:4px;'>Compare two stocks side by side</p>
    </div>
    """, unsafe_allow_html=True)

    cmp1, cmp2 = st.columns(2)
    with cmp1:
        s1_name   = st.selectbox("Stock 1", list(NSE_STOCKS.keys()), index=0)
        s1_ticker = NSE_STOCKS[s1_name]
    with cmp2:
        s2_name   = st.selectbox("Stock 2", list(NSE_STOCKS.keys()), index=1)
        s2_ticker = NSE_STOCKS[s2_name]

    with st.spinner("Loading comparison..."):
        r1 = fetch_stock(s1_ticker, start, end)
        r2 = fetch_stock(s2_ticker, start, end)

    if r1.empty or r2.empty:
        st.error("Could not load one or both stocks.")
        st.stop()

    d1 = compute_indicators(r1)
    d2 = compute_indicators(r2)

    # Normalised Chart
    norm1 = (d1['Close'] / float(d1['Close'].iloc[0])) * 100
    norm2 = (d2['Close'] / float(d2['Close'].iloc[0])) * 100
    fig_n = go.Figure()
    fig_n.add_trace(go.Scatter(x=d1.index, y=norm1, name=s1_name, line=dict(color='#1565c0', width=2)))
    fig_n.add_trace(go.Scatter(x=d2.index, y=norm2, name=s2_name, line=dict(color='#f44336', width=2)))
    fig_n.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                        height=350, title="Normalised Performance (Base 100)",
                        font=dict(family='Inter', color='#1a1a2e'), margin=dict(l=0,r=0,t=40,b=0),
                        legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
    fig_n.update_xaxes(gridcolor='#f5f5f5')
    fig_n.update_yaxes(gridcolor='#f5f5f5')
    st.plotly_chart(fig_n, use_container_width=True)

    # Side by side stats
    m1, m2 = st.columns(2)

    def make_stat_card(d, name):
        cur   = float(d['Close'].iloc[-1])
        ret   = ((cur / float(d['Close'].iloc[0])) - 1) * 100
        rsi   = float(d['RSI'].iloc[-1])
        sh    = d['Daily_Return'].mean() / d['Daily_Return'].std() * np.sqrt(252)
        dd    = ((d['Close'] / d['Close'].cummax()) - 1).min() * 100
        vol   = float(d['Volatility'].iloc[-1])
        ret_c = "#4caf50" if ret>=0 else "#f44336"
        return f"""
        <div style='background:#f8f9fa;border-radius:14px;padding:20px;'>
            <div style='font-size:1.1rem;font-weight:700;color:#1a1a2e;margin-bottom:16px;
            padding-bottom:10px;border-bottom:2px solid #eeeeee;'>{name}</div>
            <div class='stat-row'><span class='stat-key'>Price</span><span class='stat-value'>₹{cur:,.2f}</span></div>
            <div class='stat-row'><span class='stat-key'>Return</span>
                <span class='stat-value' style='color:{ret_c};'>{"+" if ret>=0 else ""}{ret:.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>RSI</span><span class='stat-value'>{rsi:.1f}</span></div>
            <div class='stat-row'><span class='stat-key'>Sharpe</span><span class='stat-value'>{sh:.2f}</span></div>
            <div class='stat-row'><span class='stat-key'>Max DD</span>
                <span class='stat-value' style='color:#f44336;'>{dd:.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>Volatility</span><span class='stat-value'>{vol:.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>Best Day</span>
                <span class='stat-value' style='color:#4caf50;'>+{d['Daily_Return'].max():.2f}%</span></div>
        </div>"""

    m1.markdown(make_stat_card(d1, s1_name), unsafe_allow_html=True)
    m2.markdown(make_stat_card(d2, s2_name), unsafe_allow_html=True)

    # RSI Comparison
    fig_rsi2 = go.Figure()
    fig_rsi2.add_trace(go.Scatter(x=d1.index, y=d1['RSI'], name=s1_name, line=dict(color='#1565c0', width=1.5)))
    fig_rsi2.add_trace(go.Scatter(x=d2.index, y=d2['RSI'], name=s2_name, line=dict(color='#f44336', width=1.5)))
    fig_rsi2.add_hline(y=70, line_dash='dash', line_color='#f44336', line_width=1)
    fig_rsi2.add_hline(y=30, line_dash='dash', line_color='#4caf50', line_width=1)
    fig_rsi2.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                           height=260, title="RSI Comparison",
                           font=dict(family='Inter', color='#1a1a2e'), margin=dict(l=0,r=0,t=40,b=0),
                           legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
    fig_rsi2.update_xaxes(gridcolor='#f5f5f5')
    fig_rsi2.update_yaxes(gridcolor='#f5f5f5', range=[0,100])
    st.plotly_chart(fig_rsi2, use_container_width=True)

    # Correlation
    combined = pd.DataFrame({
        s1_name: d1['Daily_Return'],
        s2_name: d2['Daily_Return']
    }).dropna()
    corr = combined.corr().iloc[0,1]
    fig_corr = px.scatter(combined, x=s1_name, y=s2_name, trendline="ols",
                          title=f"Return Correlation: {corr:.3f}",
                          color_discrete_sequence=['#1565c0'])
    fig_corr.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                           height=300, font=dict(family='Inter', color='#1a1a2e'),
                           margin=dict(l=0,r=0,t=40,b=0))
    fig_corr.update_xaxes(gridcolor='#f5f5f5')
    fig_corr.update_yaxes(gridcolor='#f5f5f5')
    st.plotly_chart(fig_corr, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PORTFOLIO PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == 'portfolio':
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()

    start = getattr(st.session_state, 'start_date', pd.to_datetime("2020-01-01"))
    end   = getattr(st.session_state, 'end_date',   pd.to_datetime("2025-03-21"))

    st.markdown("""
    <div style='padding:20px 0 10px;animation:fadeInDown 0.5s ease;'>
        <h2 style='font-size:1.8rem;font-weight:800;color:#1a1a2e;margin:0;'>💼 Portfolio Tracker</h2>
        <p style='color:#888;margin-top:4px;'>Track and analyse your holdings</p>
    </div>
    """, unsafe_allow_html=True)

    # Add holding form
    st.markdown("""<div style='background:#f8f9fa;border-radius:16px;padding:24px;margin-bottom:20px;'>
    <div style='font-size:1rem;font-weight:700;color:#1a1a2e;margin-bottom:16px;'>➕ Add Holding</div>
    """, unsafe_allow_html=True)

    p1,p2,p3,p4 = st.columns([3,2,2,1])
    with p1:
        port_stock = st.selectbox("Stock", list(NSE_STOCKS.keys()), key="ps")
    with p2:
        port_qty   = st.number_input("Quantity", min_value=1, value=10, key="pq")
    with p3:
        port_price = st.number_input("Buy Price (₹)", min_value=1.0, value=1000.0, key="pp")
    with p4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Add ➕", use_container_width=True):
            st.session_state.portfolio.append({
                "name": port_stock, "ticker": NSE_STOCKS[port_stock],
                "qty": port_qty, "buy": port_price
            })
            st.success(f"✅ Added {port_stock}!")

    if st.button("🗑️ Clear All"):
        st.session_state.portfolio = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.portfolio:
        total_inv = 0
        total_cur = 0
        holdings  = []

        with st.spinner("Fetching portfolio prices..."):
            for h in st.session_state.portfolio:
                try:
                    raw = fetch_stock(h['ticker'], start, end)
                    if raw.empty: continue
                    cp       = float(raw['Close'].iloc[-1])
                    invested = h['qty'] * h['buy']
                    current  = h['qty'] * cp
                    pnl      = current - invested
                    pnl_pct  = (pnl / invested) * 100
                    total_inv += invested
                    total_cur += current
                    holdings.append({**h, 'cmp': cp, 'invested': invested,
                                     'current': current, 'pnl': pnl,
                                     'pnl_pct': pnl_pct, 'raw': raw})
                except Exception:
                    continue

        if holdings:
            total_pnl     = total_cur - total_inv
            total_pnl_pct = (total_pnl / total_inv) * 100

            ps1,ps2,ps3,ps4 = st.columns(4)
            summary = [
                (ps1, "💰", f"₹{total_inv:,.0f}",  "Total Invested",  "#1565c0"),
                (ps2, "📈", f"₹{total_cur:,.0f}",  "Current Value",   "#4caf50" if total_cur>=total_inv else "#f44336"),
                (ps3, "📊", f"{'+'if total_pnl>=0 else ''}₹{total_pnl:,.0f}", "Total P&L", "#4caf50" if total_pnl>=0 else "#f44336"),
                (ps4, "🎯", f"{'+'if total_pnl_pct>=0 else ''}{total_pnl_pct:.2f}%", "Overall Return", "#4caf50" if total_pnl_pct>=0 else "#f44336"),
            ]
            for col, icon, val, label, color in summary:
                col.markdown(f"""
                <div class='metric-card' style='border-left-color:{color};'>
                    <div style='font-size:1.4rem;margin-bottom:8px;'>{icon}</div>
                    <div class='metric-value' style='color:{color};'>{val}</div>
                    <div class='metric-label'>{label}</div>
                </div>""", unsafe_allow_html=True)

            # Holdings Table
            st.markdown("""<div style='background:#f8f9fa;border-radius:16px;padding:20px;margin:16px 0;'>
            <div style='font-size:1rem;font-weight:700;color:#1a1a2e;margin-bottom:16px;'>📋 Holdings</div>
            """, unsafe_allow_html=True)

            for h in holdings:
                weight    = (h['current'] / total_cur) * 100
                pnl_color = "#4caf50" if h['pnl']>=0 else "#f44336"
                st.markdown(f"""
                <div class='scr-row'>
                    <div style='flex:2;'>
                        <div style='font-weight:700;color:#1a1a2e;'>{h['name']}</div>
                        <div style='color:#888;font-size:0.75rem;'>Qty: {h['qty']} · Avg: ₹{h['buy']:.2f}</div>
                    </div>
                    <div style='flex:1;text-align:center;'>
                        <div style='font-weight:700;color:#1a1a2e;'>₹{h['cmp']:,.2f}</div>
                        <div style='color:#888;font-size:0.75rem;'>CMP</div>
                    </div>
                    <div style='flex:1;text-align:center;'>
                        <div style='font-weight:700;color:{pnl_color};'>
                        {"+" if h['pnl']>=0 else ""}₹{h['pnl']:,.0f}</div>
                        <div style='color:{pnl_color};font-size:0.75rem;'>
                        {"+" if h['pnl_pct']>=0 else ""}{h['pnl_pct']:.2f}%</div>
                    </div>
                    <div style='flex:1;text-align:right;'>
                        <div style='font-size:0.8rem;color:#888;'>{weight:.1f}% weight</div>
                        <div style='background:#e0e0e0;border-radius:4px;height:4px;margin-top:6px;'>
                            <div style='background:#1565c0;width:{min(weight,100)}%;height:4px;border-radius:4px;'></div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Charts
            ch1, ch2 = st.columns(2)
            with ch1:
                fig_pie = px.pie(
                    values=[h['current'] for h in holdings],
                    names=[h['name'] for h in holdings],
                    title="Portfolio Allocation",
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                fig_pie.update_layout(template='plotly_white', paper_bgcolor='white',
                                      height=300, margin=dict(l=0,r=0,t=40,b=0),
                                      font=dict(family='Inter', color='#1a1a2e'),
                                      legend=dict(bgcolor='rgba(0,0,0,0)'))
                st.plotly_chart(fig_pie, use_container_width=True)

            with ch2:
                fig_pnl = px.bar(
                    x=[h['name'] for h in holdings],
                    y=[h['pnl'] for h in holdings],
                    title="P&L by Stock",
                    color=[h['pnl'] for h in holdings],
                    color_continuous_scale=['#f44336','#ffeb3b','#4caf50']
                )
                fig_pnl.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                                      height=300, margin=dict(l=0,r=0,t=40,b=0),
                                      font=dict(family='Inter', color='#1a1a2e'),
                                      showlegend=False, coloraxis_showscale=False)
                fig_pnl.update_xaxes(gridcolor='#f5f5f5')
                fig_pnl.update_yaxes(gridcolor='#f5f5f5')
                st.plotly_chart(fig_pnl, use_container_width=True)

            # Performance chart
            fig_perf = go.Figure()
            colors_l = ['#1565c0','#f44336','#4caf50','#ff9800','#7b1fa2','#00796b','#c62828']
            for i, h in enumerate(holdings):
                norm = (h['raw']['Close'] / float(h['raw']['Close'].iloc[0])) * 100
                fig_perf.add_trace(go.Scatter(x=h['raw'].index, y=norm,
                                              name=h['name'],
                                              line=dict(color=colors_l[i%len(colors_l)], width=1.5)))
            fig_perf.update_layout(template='plotly_white', paper_bgcolor='white', plot_bgcolor='white',
                                   height=320, title="Individual Stock Performance (Base 100)",
                                   font=dict(family='Inter', color='#1a1a2e'),
                                   margin=dict(l=0,r=0,t=40,b=0),
                                   legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
            fig_perf.update_xaxes(gridcolor='#f5f5f5')
            fig_perf.update_yaxes(gridcolor='#f5f5f5')
            st.plotly_chart(fig_perf, use_container_width=True)
    else:
        st.info("👆 Add stocks to your portfolio using the form above to get started!")

# ── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    <strong style='color:#90caf9;'>🔭 StockLens</strong>
    &nbsp;—&nbsp; Indian Market Analytics Platform
    &nbsp;·&nbsp; NSE & BSE
    &nbsp;·&nbsp; Yahoo Finance API
    &nbsp;·&nbsp; ⚠️ For educational purposes only. Not financial advice.
</div>
""", unsafe_allow_html=True)
