import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import yfinance as yf

st.set_page_config(
    page_title="StockLens — Indian Market Analytics",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #1a237e; }
section[data-testid="stSidebar"] { background: #0d1257 !important; border-right: 1px solid #283593; }
section[data-testid="stSidebar"] * { color: #90caf9 !important; }
.sidebar-brand { padding: 24px 16px 32px; border-bottom: 1px solid #283593; margin-bottom: 16px; }
.brand-logo { font-size: 1.6rem; font-weight: 700; color: #90caf9 !important; }
.brand-sub { font-size: 0.75rem; color: #5c6bc0 !important; margin-top: 2px; }
.nav-item { padding: 10px 16px; border-radius: 10px; margin: 4px 0; cursor: pointer; color: #7986cb !important; font-size: 0.9rem; }
.nav-item-active { background: #283593; color: #90caf9 !important; font-weight: 600; }
.page-title { font-size: 1.8rem; font-weight: 700; color: #ffffff; margin: 0; }
.page-subtitle { font-size: 0.85rem; color: #90caf9; margin-top: 4px; margin-bottom: 20px; }
.card { background: #1e2a9a; border-radius: 16px; padding: 20px; box-shadow: 0 1px 8px rgba(0,0,0,0.3); margin-bottom: 16px; transition: all 0.2s; }
.card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.4); transform: translateY(-2px); }
.metric-card { background: #1e2a9a; border-radius: 16px; padding: 20px 20px 16px; box-shadow: 0 1px 8px rgba(0,0,0,0.3); margin-bottom: 16px; border-left: 4px solid transparent; transition: all 0.2s; }
.metric-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.4); transform: translateY(-2px); }
.metric-card-blue   { border-left-color: #64b5f6; }
.metric-card-green  { border-left-color: #81c784; }
.metric-card-red    { border-left-color: #e57373; }
.metric-card-purple { border-left-color: #ce93d8; }
.metric-card-yellow { border-left-color: #fff176; }
.metric-card-teal   { border-left-color: #80cbc4; }
.metric-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; margin-bottom: 12px; }
.icon-blue   { background: #1565c0; }
.icon-green  { background: #1b5e20; }
.icon-red    { background: #b71c1c; }
.icon-purple { background: #4a148c; }
.icon-yellow { background: #f57f17; }
.icon-teal   { background: #004d40; }
.metric-value { font-size: 1.6rem; font-weight: 700; color: #ffffff; line-height: 1; }
.metric-label { font-size: 0.78rem; color: #90caf9; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }
.signal-pill { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.pill-buy  { background: #1b5e20; color: #81c784; }
.pill-sell { background: #b71c1c; color: #ef9a9a; }
.pill-hold { background: #f57f17; color: #fff176; }
.section-title { font-size: 1rem; font-weight: 600; color: #ffffff; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #283593; }
.stat-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #283593; font-size: 0.875rem; }
.stat-row:last-child { border-bottom: none; }
.stat-key   { color: #90caf9; }
.stat-value { font-weight: 600; color: #ffffff; }
.pattern-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: #283593; border-radius: 10px; margin-bottom: 8px; transition: background 0.2s; }
.pattern-row:hover { background: #303f9f; }
.footer-card { background: #0d1257; border-radius: 16px; padding: 20px 24px; color: #90caf9; font-size: 0.82rem; margin-top: 8px; display: flex; justify-content: space-between; align-items: center; }
.screener-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: #283593; border-radius: 10px; margin-bottom: 8px; transition: all 0.2s; }
.screener-row:hover { background: #303f9f; transform: translateX(4px); }
</style>
""", unsafe_allow_html=True)

# ── Stock Universe ─────────────────────────────────────────────
NSE_STOCKS = {
    "HDFC Bank":         "HDFCBANK.NS",
    "Reliance":          "RELIANCE.NS",
    "TCS":               "TCS.NS",
    "Infosys":           "INFY.NS",
    "ICICI Bank":        "ICICIBANK.NS",
    "SBI":               "SBIN.NS",
    "Wipro":             "WIPRO.NS",
    "Bharti Airtel":     "BHARTIARTL.NS",
    "Kotak Bank":        "KOTAKBANK.NS",
    "Axis Bank":         "AXISBANK.NS",
    "ITC":               "ITC.NS",
    "HUL":               "HINDUNILVR.NS",
    "Maruti":            "MARUTI.NS",
    "Bajaj Finance":     "BAJFINANCE.NS",
    "Sun Pharma":        "SUNPHARMA.NS",
    "Titan":             "TITAN.NS",
    "Asian Paints":      "ASIANPAINT.NS",
    "UltraTech Cement":  "ULTRACEMCO.NS",
    "Tata Motors":       "TATAMOTORS.NS",
    "Adani Ports":       "ADANIPORTS.NS",
}

BSE_STOCKS = {
    "BSE: HDFC Bank":    "HDFCBANK.BO",
    "BSE: Reliance":     "RELIANCE.BO",
    "BSE: TCS":          "TCS.BO",
    "BSE: Infosys":      "INFY.BO",
    "BSE: ICICI Bank":   "ICICIBANK.BO",
    "BSE: SBI":          "SBIN.BO",
    "BSE: Wipro":        "WIPRO.BO",
    "BSE: ITC":          "ITC.BO",
    "BSE: Maruti":       "MARUTI.BO",
    "BSE: Sun Pharma":   "SUNPHARMA.BO",
}

ALL_STOCKS = {**NSE_STOCKS, **BSE_STOCKS}

# ── Data Fetcher ───────────────────────────────────────────────
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
    df['SMA_20']  = df['Close'].rolling(20).mean()
    df['SMA_50']  = df['Close'].rolling(50).mean()
    df['SMA_200'] = df['Close'].rolling(200).mean()
    df['EMA_20']  = df['Close'].ewm(span=20, adjust=False).mean()
    df['BB_Mid']  = df['Close'].rolling(bb_p).mean()
    df['BB_Std']  = df['Close'].rolling(bb_p).std()
    df['BB_Upper']= df['BB_Mid'] + 2 * df['BB_Std']
    df['BB_Lower']= df['BB_Mid'] - 2 * df['BB_Std']
    df['BB_Width']= (df['BB_Upper'] - df['BB_Lower']) / df['BB_Mid'] * 100
    delta = df['Close'].diff()
    gain  = delta.where(delta > 0, 0).rolling(rsi_p).mean()
    loss  = -delta.where(delta < 0, 0).rolling(rsi_p).mean()
    df['RSI'] = 100 - (100 / (1 + gain / loss))
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD']        = ema12 - ema26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist']   = df['MACD'] - df['MACD_Signal']
    df['Daily_Return'] = df['Close'].pct_change() * 100
    df['Volatility']   = df['Daily_Return'].rolling(20).std()
    df['VWAP']         = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    tr1 = df['High'] - df['Low']
    tr2 = abs(df['High'] - df['Close'].shift())
    tr3 = abs(df['Low']  - df['Close'].shift())
    df['ATR'] = pd.concat([tr1,tr2,tr3], axis=1).max(axis=1).rolling(14).mean()
    df['Body']         = abs(df['Close'] - df['Open'])
    df['Body_Range']   = df['High'] - df['Low']
    df['Upper_Shadow'] = df['High'] - df[['Close','Open']].max(axis=1)
    df['Lower_Shadow'] = df[['Close','Open']].min(axis=1) - df['Low']
    df['Doji']              = df['Body'] <= 0.1 * df['Body_Range']
    df['Hammer']            = (df['Lower_Shadow']>=2*df['Body']) & (df['Upper_Shadow']<=0.1*df['Body_Range']) & (df['Body']>0)
    df['Shooting_Star']     = (df['Upper_Shadow']>=2*df['Body']) & (df['Lower_Shadow']<=0.1*df['Body_Range']) & (df['Body']>0)
    df['Bullish_Engulfing'] = (df['Close']>df['Open']) & (df['Close'].shift(1)<df['Open'].shift(1)) & (df['Close']>df['Open'].shift(1)) & (df['Open']<df['Close'].shift(1))
    df['Bearish_Engulfing'] = (df['Close']<df['Open']) & (df['Close'].shift(1)>df['Open'].shift(1)) & (df['Close']<df['Open'].shift(1)) & (df['Open']>df['Close'].shift(1))
    df['Month'] = df.index.month
    df['Year']  = df.index.year
    return df

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <div class='brand-logo'>🔭 StockLens</div>
        <div class='brand-sub'>Indian Market Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigate", [
        "📊 Dashboard",
        "🔍 Stock Screener",
        "⚖️ Stock Comparison",
        "💼 Portfolio Tracker"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**🔎 Select Stock**")
    selected_name   = st.selectbox("Stock", list(ALL_STOCKS.keys()), label_visibility="collapsed")
    selected_ticker = ALL_STOCKS[selected_name]

    custom = st.text_input("Or enter custom ticker (e.g. TATASTEEL.NS)")
    if custom.strip():
        selected_ticker = custom.strip().upper()
        selected_name   = custom.strip().upper()

    st.markdown("**📅 Date Range**")
    start_date = st.date_input("From", pd.to_datetime("2020-01-01"), label_visibility="collapsed")
    end_date   = st.date_input("To",   pd.to_datetime("2025-03-21"), label_visibility="collapsed")

    st.markdown("**📊 Chart**")
    chart_type = st.selectbox("Type", ["Candlestick","Line","OHLC"], label_visibility="collapsed")

    st.markdown("**📈 Overlays**")
    show_sma      = st.checkbox("Moving Averages",  value=True)
    show_ema      = st.checkbox("EMA 20",           value=True)
    show_bb       = st.checkbox("Bollinger Bands",  value=True)
    show_vwap     = st.checkbox("VWAP",             value=False)
    show_patterns = st.checkbox("Show Patterns",    value=True)

    st.markdown("**🔢 Periods**")
    rsi_period = st.slider("RSI", 7, 28, 14)
    bb_period  = st.slider("BB",  10, 50, 20)

    st.markdown("""
    <div style='background:#283593;border-radius:10px;padding:12px;margin-top:16px;
    font-size:0.75rem;color:#7986cb;'>
    📡 NSE (.NS) · BSE (.BO)<br>
    🌐 Yahoo Finance API<br>
    🔄 1hr cache · Live data
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "📊 Dashboard":

    with st.spinner(f"Loading {selected_name}..."):
        raw = fetch_stock(selected_ticker, start_date, end_date)

    if raw.empty:
        st.error(f"Could not fetch data for {selected_ticker}. Please check the ticker symbol.")
        st.stop()

    df = compute_indicators(raw, rsi_period, bb_period)

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
    vol_colors= ['#81c784' if float(c) >= float(o) else '#e57373'
                 for c, o in zip(df['Close'], df['Open'])]

    st.markdown(f"""
    <h1 class='page-title'>{selected_name}
        <span style='font-size:0.85rem;font-weight:400;color:#90caf9;margin-left:12px;'>
        {selected_ticker} &nbsp;·&nbsp;
        {df.index[0].strftime('%d %b %Y')} — {df.index[-1].strftime('%d %b %Y')}
        </span>
    </h1>
    <p class='page-subtitle'>
        {'🟢' if chg>=0 else '🔴'} ₹{cur:.2f} &nbsp;
        <strong style='color:{"#81c784" if chg>=0 else "#e57373"}'>
        {'▲' if chg>=0 else '▼'} ₹{abs(chg):.2f} ({chgp:+.2f}%)
        </strong>
        &nbsp;·&nbsp; {len(df)} trading days loaded
    </p>
    """, unsafe_allow_html=True)

    # KPI Cards
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    cards = [
        (c1,"💰","icon-blue",  "metric-card-blue",  f"₹{cur:.2f}",       "Current Price", f"{'▲' if chg>=0 else '▼'} {chgp:+.2f}% today",      chg>=0),
        (c2,"📈","icon-green", "metric-card-green", f"₹{hi52:.2f}",      "52W High",      f"{((cur/hi52)-1)*100:.1f}% below high",               False),
        (c3,"📉","icon-red",   "metric-card-red",   f"₹{lo52:.2f}",      "52W Low",       f"{((cur/lo52)-1)*100:.1f}% above low",                True),
        (c4,"⚡","icon-purple","metric-card-purple",f"{rsi:.1f}",        "RSI (14)",      "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral", rsi<=70),
        (c5,"📊","icon-yellow","metric-card-yellow",f"{total_ret:.1f}%", "Total Return",  f"Since {df.index[0].strftime('%b %Y')}",              total_ret>0),
        (c6,"🎯","icon-teal",  "metric-card-teal",  f"{sharpe:.2f}",     "Sharpe Ratio",  "Risk-adjusted return",                                sharpe>1),
    ]
    for col, icon, icon_cls, card_cls, val, label, sub, pos in cards:
        color = "#81c784" if pos else "#e57373"
        col.markdown(f"""
        <div class='metric-card {card_cls}'>
            <div class='metric-icon {icon_cls}'>{icon}</div>
            <div class='metric-value'>{val}</div>
            <div class='metric-label'>{label}</div>
            <div style='color:{color};font-size:0.78rem;font-weight:500;margin-top:6px;'>{sub}</div>
        </div>""", unsafe_allow_html=True)

    # Chart + Signals
    chart_col, signal_col = st.columns([3, 1])

    with chart_col:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'>💹 {selected_name} Price Action</div>", unsafe_allow_html=True)

        fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                            row_heights=[0.6,0.2,0.2], vertical_spacing=0.02)

        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                          low=df['Low'], close=df['Close'], name=selected_name,
                                          increasing_line_color='#81c784',
                                          decreasing_line_color='#e57373'), row=1, col=1)
        elif chart_type == "OHLC":
            fig.add_trace(go.Ohlc(x=df.index, open=df['Open'], high=df['High'],
                                  low=df['Low'], close=df['Close'], name=selected_name), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name=selected_name,
                                     line=dict(color='#64b5f6', width=2),
                                     fill='tozeroy', fillcolor='rgba(100,181,246,0.1)'), row=1, col=1)

        if show_sma:
            for cn, color, nm in [('SMA_20','#fff176','SMA 20'),('SMA_50','#81c784','SMA 50'),('SMA_200','#e57373','SMA 200')]:
                fig.add_trace(go.Scatter(x=df.index, y=df[cn], name=nm,
                                         line=dict(color=color, width=1.2)), row=1, col=1)
        if show_ema:
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], name='EMA 20',
                                     line=dict(color='#ce93d8', width=1.2, dash='dot')), row=1, col=1)
        if show_vwap:
            fig.add_trace(go.Scatter(x=df.index, y=df['VWAP'], name='VWAP',
                                     line=dict(color='#80cbc4', width=1.2, dash='dash')), row=1, col=1)
        if show_bb:
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper',
                                     line=dict(color='rgba(144,202,249,0.4)', width=0.8)), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower',
                                     line=dict(color='rgba(144,202,249,0.4)', width=0.8),
                                     fill='tonexty', fillcolor='rgba(144,202,249,0.05)'), row=1, col=1)
        if show_patterns:
            for pat, sym, col_m in [('Doji','circle-open','#fff176'),
                                     ('Hammer','triangle-up','#81c784'),
                                     ('Bullish_Engulfing','star','#81c784'),
                                     ('Bearish_Engulfing','star','#e57373')]:
                pat_df = df[df[pat]]
                y_vals = pat_df['Low']*0.99 if 'Bullish' in pat or pat=='Hammer' else pat_df['High']*1.01
                fig.add_trace(go.Scatter(x=pat_df.index, y=y_vals, mode='markers',
                                         name=pat, marker=dict(symbol=sym, color=col_m, size=9)), row=1, col=1)

        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
                             marker_color=vol_colors, opacity=0.6), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI',
                                 line=dict(color='#fff176', width=1.5)), row=3, col=1)
        fig.add_hrect(y0=70, y1=100, fillcolor='rgba(229,115,115,0.1)', line_width=0, row=3, col=1)
        fig.add_hrect(y0=0,  y1=30,  fillcolor='rgba(129,199,132,0.1)', line_width=0, row=3, col=1)
        fig.add_hline(y=70, line_dash='dash', line_color='#e57373', line_width=1, row=3, col=1)
        fig.add_hline(y=30, line_dash='dash', line_color='#81c784', line_width=1, row=3, col=1)

        fig.update_layout(height=560, template='plotly_dark',
                          xaxis_rangeslider_visible=False,
                          paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                          legend=dict(orientation='h', yanchor='bottom', y=1.01,
                                      bgcolor='rgba(0,0,0,0)', font=dict(size=11,color='#90caf9')),
                          font=dict(family='Inter', color='#90caf9'),
                          margin=dict(l=0,r=0,t=30,b=0))
        for i in range(1, 4):
            fig.update_xaxes(gridcolor='#283593', row=i, col=1)
            fig.update_yaxes(gridcolor='#283593', row=i, col=1)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with signal_col:
        rsi_sig  = ("BUY","pill-buy")  if rsi<30 else ("SELL","pill-sell") if rsi>70 else ("HOLD","pill-hold")
        macd_sig = ("BUY","pill-buy")  if macd>0 else ("SELL","pill-sell")
        sma_sig  = ("BUY","pill-buy")  if cur>float(df['SMA_200'].iloc[-1]) else ("SELL","pill-sell")
        bb_pos   = (cur - float(df['BB_Lower'].iloc[-1])) / (float(df['BB_Upper'].iloc[-1]) - float(df['BB_Lower'].iloc[-1]))
        bb_sig   = ("BUY","pill-buy")  if bb_pos<0.2 else ("SELL","pill-sell") if bb_pos>0.8 else ("HOLD","pill-hold")

        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>🚦 Signals</div>
            <div class='pattern-row'><span style='color:#90caf9;font-size:0.85rem;'>RSI ({rsi:.0f})</span>
                <span class='signal-pill {rsi_sig[1]}'>{rsi_sig[0]}</span></div>
            <div class='pattern-row'><span style='color:#90caf9;font-size:0.85rem;'>MACD</span>
                <span class='signal-pill {macd_sig[1]}'>{macd_sig[0]}</span></div>
            <div class='pattern-row'><span style='color:#90caf9;font-size:0.85rem;'>SMA 200</span>
                <span class='signal-pill {sma_sig[1]}'>{sma_sig[0]}</span></div>
            <div class='pattern-row'><span style='color:#90caf9;font-size:0.85rem;'>Bollinger</span>
                <span class='signal-pill {bb_sig[1]}'>{bb_sig[0]}</span></div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>📐 Statistics</div>
            <div class='stat-row'><span class='stat-key'>Mean</span><span class='stat-value'>₹{df['Close'].mean():.2f}</span></div>
            <div class='stat-row'><span class='stat-key'>Std Dev</span><span class='stat-value'>₹{df['Close'].std():.2f}</span></div>
            <div class='stat-row'><span class='stat-key'>Best Day</span><span class='stat-value' style='color:#81c784;'>+{df['Daily_Return'].max():.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>Worst Day</span><span class='stat-value' style='color:#e57373;'>{df['Daily_Return'].min():.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>Max DD</span><span class='stat-value' style='color:#e57373;'>{max_dd:.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>+ve Days</span><span class='stat-value'>{(df['Daily_Return']>0).mean()*100:.1f}%</span></div>
        </div>""", unsafe_allow_html=True)

        total_patterns = int(df['Doji'].sum()+df['Hammer'].sum()+df['Bullish_Engulfing'].sum()+df['Bearish_Engulfing'].sum())
        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>🕯️ Patterns</div>
            <div class='pattern-row'><span style='color:#fff;font-size:0.85rem;'>🟡 Doji</span><span style='color:#fff176;font-weight:700;'>{int(df['Doji'].sum())}</span></div>
            <div class='pattern-row'><span style='color:#fff;font-size:0.85rem;'>🟢 Hammer</span><span style='color:#81c784;font-weight:700;'>{int(df['Hammer'].sum())}</span></div>
            <div class='pattern-row'><span style='color:#fff;font-size:0.85rem;'>🔴 Shoot Star</span><span style='color:#e57373;font-weight:700;'>{int(df['Shooting_Star'].sum())}</span></div>
            <div class='pattern-row'><span style='color:#fff;font-size:0.85rem;'>🟢 Bull Engulf</span><span style='color:#81c784;font-weight:700;'>{int(df['Bullish_Engulfing'].sum())}</span></div>
            <div class='pattern-row'><span style='color:#fff;font-size:0.85rem;'>🔴 Bear Engulf</span><span style='color:#e57373;font-weight:700;'>{int(df['Bearish_Engulfing'].sum())}</span></div>
            <div style='margin-top:12px;padding-top:12px;border-top:2px solid #283593;text-align:center;font-size:0.8rem;color:#90caf9;'>
                {total_patterns} patterns · {len(df)} days
            </div>
        </div>""", unsafe_allow_html=True)

    # Distribution + Heatmap
    d1, d2 = st.columns([1, 2])
    with d1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📊 Returns Distribution</div>", unsafe_allow_html=True)
        fig_ret = px.histogram(df['Daily_Return'].dropna(), nbins=50, color_discrete_sequence=['#64b5f6'])
        fig_ret.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                              height=260, showlegend=False, margin=dict(l=0,r=0,t=0,b=0),
                              font=dict(color='#90caf9'))
        fig_ret.update_xaxes(gridcolor='#283593')
        fig_ret.update_yaxes(gridcolor='#283593')
        st.plotly_chart(fig_ret, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with d2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🗓️ Monthly Returns Heatmap</div>", unsafe_allow_html=True)
        month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
        monthly = df.groupby(['Year','Month'])['Daily_Return'].sum().unstack()
        monthly.columns = [month_names[m] for m in monthly.columns]
        fig_heat = px.imshow(monthly, color_continuous_scale='RdYlGn', aspect='auto', text_auto='.1f')
        fig_heat.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                               height=260, margin=dict(l=0,r=0,t=0,b=0),
                               font=dict(color='#90caf9'), coloraxis_showscale=False)
        st.plotly_chart(fig_heat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Volume + Volatility
    v1, v2 = st.columns(2)
    with v1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📦 Volume Analysis</div>", unsafe_allow_html=True)
        df['Vol_MA20'] = df['Volume'].rolling(20).mean()
        fig_v = go.Figure()
        fig_v.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color=vol_colors, opacity=0.5))
        fig_v.add_trace(go.Scatter(x=df.index, y=df['Vol_MA20'], name='MA 20', line=dict(color='#64b5f6', width=2)))
        fig_v.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                            height=240, showlegend=True, margin=dict(l=0,r=0,t=0,b=0),
                            font=dict(color='#90caf9'), legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
        fig_v.update_xaxes(gridcolor='#283593')
        fig_v.update_yaxes(gridcolor='#283593')
        st.plotly_chart(fig_v, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with v2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🌊 Rolling Volatility</div>", unsafe_allow_html=True)
        fig_vola = go.Figure()
        fig_vola.add_trace(go.Scatter(x=df.index, y=df['Volatility'], fill='tozeroy',
                                      fillcolor='rgba(206,147,216,0.15)', line=dict(color='#ce93d8', width=2)))
        fig_vola.add_hline(y=df['Volatility'].mean(), line_dash='dash', line_color='#fff176',
                           annotation_text="Mean", annotation_position="right",
                           annotation_font_color='#fff176')
        fig_vola.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                               height=240, showlegend=False, margin=dict(l=0,r=0,t=0,b=0),
                               font=dict(color='#90caf9'))
        fig_vola.update_xaxes(gridcolor='#283593')
        fig_vola.update_yaxes(gridcolor='#283593')
        st.plotly_chart(fig_vola, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Data Explorer
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📋 Data Explorer</div>", unsafe_allow_html=True)
    e1, e2 = st.columns([3,1])
    with e1:
        show_cols = st.multiselect("Columns",
            options=['Open','High','Low','Close','Volume','RSI','MACD','BB_Upper','BB_Lower',
                     'SMA_20','SMA_50','SMA_200','EMA_20','ATR','Volatility','Daily_Return','VWAP'],
            default=['Open','High','Low','Close','Volume','RSI','MACD'])
    with e2:
        n_rows = st.slider("Rows", 10, 100, 25)
    st.dataframe(df[show_cols].tail(n_rows).round(2).sort_index(ascending=False), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 2 — STOCK SCREENER
# ══════════════════════════════════════════════════════════════
elif page == "🔍 Stock Screener":
    st.markdown("<h1 class='page-title'>🔍 Stock Screener</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Filter NSE stocks by technical indicators</p>", unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        rsi_min = st.slider("RSI Min", 0,  100, 0)
        rsi_max = st.slider("RSI Max", 0,  100, 100)
    with sc2:
        ret_min = st.slider("Min Return %", -100, 100, -100)
        ret_max = st.slider("Max Return %", -100, 100, 100)
    with sc3:
        trend_filter = st.selectbox("Trend Filter", ["All","Above SMA200","Below SMA200"])
        macd_filter  = st.selectbox("MACD Filter",  ["All","Bullish","Bearish"])

    if st.button("🔍 Run Screener", use_container_width=True):
        results = []
        progress = st.progress(0)
        nse_stocks = list(NSE_STOCKS.items())

        for i, (name, ticker) in enumerate(nse_stocks):
            progress.progress((i+1)/len(nse_stocks), text=f"Scanning {name}...")
            try:
                raw = fetch_stock(ticker, start_date, end_date)
                if raw.empty or len(raw) < 50:
                    continue
                d = compute_indicators(raw)
                cur_p  = float(d['Close'].iloc[-1])
                rsi_v  = float(d['RSI'].iloc[-1])
                macd_v = float(d['MACD'].iloc[-1])
                ret_v  = ((cur_p / float(d['Close'].iloc[0])) - 1) * 100
                sma200 = float(d['SMA_200'].iloc[-1])
                vol_v  = float(d['Volatility'].iloc[-1])

                if not (rsi_min <= rsi_v <= rsi_max): continue
                if not (ret_min <= ret_v <= ret_max):  continue
                if trend_filter == "Above SMA200" and cur_p <= sma200: continue
                if trend_filter == "Below SMA200" and cur_p >= sma200: continue
                if macd_filter == "Bullish" and macd_v <= 0: continue
                if macd_filter == "Bearish" and macd_v >= 0: continue

                signal = "BUY" if rsi_v<40 and macd_v>0 else "SELL" if rsi_v>60 and macd_v<0 else "HOLD"
                results.append({
                    "Stock": name, "Ticker": ticker,
                    "Price": f"₹{cur_p:.2f}", "RSI": f"{rsi_v:.1f}",
                    "MACD": f"{macd_v:.2f}", "Return": f"{ret_v:.1f}%",
                    "Volatility": f"{vol_v:.2f}%", "Signal": signal
                })
            except Exception:
                continue

        progress.empty()

        if results:
            st.markdown(f"<div class='card'><div class='section-title'>✅ {len(results)} Stocks Found</div>", unsafe_allow_html=True)
            for r in results:
                sig_cls = "pill-buy" if r['Signal']=="BUY" else "pill-sell" if r['Signal']=="SELL" else "pill-hold"
                ret_color = "#81c784" if "+" in r['Return'] or not r['Return'].startswith("-") else "#e57373"
                st.markdown(f"""
                <div class='screener-row'>
                    <div style='flex:2;'>
                        <div style='color:#fff;font-weight:600;font-size:0.9rem;'>{r['Stock']}</div>
                        <div style='color:#90caf9;font-size:0.75rem;'>{r['Ticker']}</div>
                    </div>
                    <div style='flex:1;text-align:center;color:#fff;font-weight:700;'>{r['Price']}</div>
                    <div style='flex:1;text-align:center;color:#90caf9;'>RSI: {r['RSI']}</div>
                    <div style='flex:1;text-align:center;color:{ret_color};font-weight:600;'>{r['Return']}</div>
                    <div style='flex:1;text-align:center;'><span class='signal-pill {sig_cls}'>{r['Signal']}</span></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No stocks matched your filters. Try widening the criteria.")

# ══════════════════════════════════════════════════════════════
# PAGE 3 — STOCK COMPARISON
# ══════════════════════════════════════════════════════════════
elif page == "⚖️ Stock Comparison":
    st.markdown("<h1 class='page-title'>⚖️ Stock Comparison</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Compare two stocks side by side</p>", unsafe_allow_html=True)

    cmp1, cmp2 = st.columns(2)
    with cmp1:
        stock1_name   = st.selectbox("Stock 1", list(NSE_STOCKS.keys()), index=0)
        stock1_ticker = NSE_STOCKS[stock1_name]
    with cmp2:
        stock2_name   = st.selectbox("Stock 2", list(NSE_STOCKS.keys()), index=1)
        stock2_ticker = NSE_STOCKS[stock2_name]

    with st.spinner("Loading comparison data..."):
        raw1 = fetch_stock(stock1_ticker, start_date, end_date)
        raw2 = fetch_stock(stock2_ticker, start_date, end_date)

    if raw1.empty or raw2.empty:
        st.error("Could not fetch data for one or both stocks.")
        st.stop()

    df1 = compute_indicators(raw1)
    df2 = compute_indicators(raw2)

    # Normalised price comparison
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📈 Normalised Price Performance (Base 100)</div>", unsafe_allow_html=True)
    norm1 = (df1['Close'] / float(df1['Close'].iloc[0])) * 100
    norm2 = (df2['Close'] / float(df2['Close'].iloc[0])) * 100
    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Scatter(x=df1.index, y=norm1, name=stock1_name, line=dict(color='#64b5f6', width=2)))
    fig_cmp.add_trace(go.Scatter(x=df2.index, y=norm2, name=stock2_name, line=dict(color='#81c784', width=2)))
    fig_cmp.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                          height=350, font=dict(color='#90caf9'), margin=dict(l=0,r=0,t=10,b=0),
                          legend=dict(orientation='h', y=1.05, bgcolor='rgba(0,0,0,0)'))
    fig_cmp.update_xaxes(gridcolor='#283593')
    fig_cmp.update_yaxes(gridcolor='#283593')
    st.plotly_chart(fig_cmp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Side by side stats
    m1, m2 = st.columns(2)

    def stat_card(df, name, ticker):
        cur   = float(df['Close'].iloc[-1])
        ret   = ((cur / float(df['Close'].iloc[0])) - 1) * 100
        rsi   = float(df['RSI'].iloc[-1])
        sharpe= df['Daily_Return'].mean() / df['Daily_Return'].std() * np.sqrt(252)
        maxdd = ((df['Close'] / df['Close'].cummax()) - 1).min() * 100
        vol   = float(df['Volatility'].iloc[-1])
        return f"""
        <div class='card'>
            <div class='section-title'>📊 {name}</div>
            <div class='stat-row'><span class='stat-key'>Price</span><span class='stat-value'>₹{cur:.2f}</span></div>
            <div class='stat-row'><span class='stat-key'>Total Return</span>
                <span class='stat-value' style='color:{"#81c784" if ret>0 else "#e57373"};'>{ret:.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>RSI</span><span class='stat-value'>{rsi:.1f}</span></div>
            <div class='stat-row'><span class='stat-key'>Sharpe</span><span class='stat-value'>{sharpe:.2f}</span></div>
            <div class='stat-row'><span class='stat-key'>Max Drawdown</span>
                <span class='stat-value' style='color:#e57373;'>{maxdd:.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>Volatility</span><span class='stat-value'>{vol:.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>Best Day</span>
                <span class='stat-value' style='color:#81c784;'>+{df['Daily_Return'].max():.2f}%</span></div>
            <div class='stat-row'><span class='stat-key'>Worst Day</span>
                <span class='stat-value' style='color:#e57373;'>{df['Daily_Return'].min():.2f}%</span></div>
        </div>"""

    m1.markdown(stat_card(df1, stock1_name, stock1_ticker), unsafe_allow_html=True)
    m2.markdown(stat_card(df2, stock2_name, stock2_ticker), unsafe_allow_html=True)

    # RSI Comparison
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚡ RSI Comparison</div>", unsafe_allow_html=True)
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df1.index, y=df1['RSI'], name=stock1_name, line=dict(color='#64b5f6', width=1.5)))
    fig_rsi.add_trace(go.Scatter(x=df2.index, y=df2['RSI'], name=stock2_name, line=dict(color='#81c784', width=1.5)))
    fig_rsi.add_hline(y=70, line_dash='dash', line_color='#e57373', line_width=1)
    fig_rsi.add_hline(y=30, line_dash='dash', line_color='#81c784', line_width=1)
    fig_rsi.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                          height=280, font=dict(color='#90caf9'), margin=dict(l=0,r=0,t=10,b=0),
                          legend=dict(orientation='h', y=1.05, bgcolor='rgba(0,0,0,0)'))
    fig_rsi.update_xaxes(gridcolor='#283593')
    fig_rsi.update_yaxes(gridcolor='#283593')
    st.plotly_chart(fig_rsi, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Correlation
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔗 Return Correlation</div>", unsafe_allow_html=True)
    combined = pd.DataFrame({
        stock1_name: df1['Daily_Return'],
        stock2_name: df2['Daily_Return']
    }).dropna()
    correlation = combined.corr().iloc[0,1]
    fig_corr = px.scatter(combined, x=stock1_name, y=stock2_name,
                          title=f"Correlation: {correlation:.3f}",
                          trendline="ols",
                          color_discrete_sequence=['#64b5f6'])
    fig_corr.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                           height=300, font=dict(color='#90caf9'), margin=dict(l=0,r=0,t=30,b=0))
    fig_corr.update_xaxes(gridcolor='#283593')
    fig_corr.update_yaxes(gridcolor='#283593')
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 4 — PORTFOLIO TRACKER
# ══════════════════════════════════════════════════════════════
elif page == "💼 Portfolio Tracker":
    st.markdown("<h1 class='page-title'>💼 Portfolio Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Track and analyse your stock portfolio</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>➕ Add Holdings</div>", unsafe_allow_html=True)

    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []

    p1, p2, p3, p4 = st.columns([3,2,2,1])
    with p1:
        port_stock  = st.selectbox("Stock", list(NSE_STOCKS.keys()), key="port_stock")
    with p2:
        port_qty    = st.number_input("Quantity", min_value=1, value=10, key="port_qty")
    with p3:
        port_price  = st.number_input("Buy Price (₹)", min_value=1.0, value=1000.0, key="port_price")
    with p4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Add ➕"):
            st.session_state.portfolio.append({
                "name":   port_stock,
                "ticker": NSE_STOCKS[port_stock],
                "qty":    port_qty,
                "buy":    port_price
            })
            st.success(f"Added {port_stock}!")

    if st.button("🗑️ Clear Portfolio"):
        st.session_state.portfolio = []

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.portfolio:
        total_invested = 0
        total_current  = 0
        holdings_data  = []

        with st.spinner("Fetching portfolio data..."):
            for h in st.session_state.portfolio:
                try:
                    raw = fetch_stock(h['ticker'], start_date, end_date)
                    if raw.empty:
                        continue
                    cur_p     = float(raw['Close'].iloc[-1])
                    invested  = h['qty'] * h['buy']
                    current   = h['qty'] * cur_p
                    pnl       = current - invested
                    pnl_pct   = (pnl / invested) * 100
                    total_invested += invested
                    total_current  += current
                    holdings_data.append({
                        "Stock":     h['name'],
                        "Qty":       h['qty'],
                        "Buy Price": h['buy'],
                        "CMP":       cur_p,
                        "Invested":  invested,
                        "Current":   current,
                        "P&L":       pnl,
                        "P&L %":     pnl_pct,
                        "raw":       raw
                    })
                except Exception:
                    continue

        if holdings_data:
            total_pnl     = total_current - total_invested
            total_pnl_pct = (total_pnl / total_invested) * 100

            # Portfolio Summary Cards
            ps1, ps2, ps3, ps4 = st.columns(4)
            ps1.markdown(f"""<div class='metric-card metric-card-blue'>
                <div class='metric-icon icon-blue'>💰</div>
                <div class='metric-value'>₹{total_invested:,.0f}</div>
                <div class='metric-label'>Total Invested</div></div>""", unsafe_allow_html=True)
            ps2.markdown(f"""<div class='metric-card metric-card-green'>
                <div class='metric-icon icon-green'>📈</div>
                <div class='metric-value'>₹{total_current:,.0f}</div>
                <div class='metric-label'>Current Value</div></div>""", unsafe_allow_html=True)
            ps3.markdown(f"""<div class='metric-card {"metric-card-green" if total_pnl>=0 else "metric-card-red"}'>
                <div class='metric-icon {"icon-green" if total_pnl>=0 else "icon-red"}'>{"📊" if total_pnl>=0 else "📉"}</div>
                <div class='metric-value' style='color:{"#81c784" if total_pnl>=0 else "#e57373"}'>
                {"+" if total_pnl>=0 else ""}₹{total_pnl:,.0f}</div>
                <div class='metric-label'>Total P&L</div></div>""", unsafe_allow_html=True)
            ps4.markdown(f"""<div class='metric-card {"metric-card-green" if total_pnl_pct>=0 else "metric-card-red"}'>
                <div class='metric-icon {"icon-green" if total_pnl_pct>=0 else "icon-red"}'>🎯</div>
                <div class='metric-value' style='color:{"#81c784" if total_pnl_pct>=0 else "#e57373"}'>
                {"+" if total_pnl_pct>=0 else ""}{total_pnl_pct:.2f}%</div>
                <div class='metric-label'>Overall Return</div></div>""", unsafe_allow_html=True)

            # Holdings Table
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📋 Holdings</div>", unsafe_allow_html=True)
            for h in holdings_data:
                pnl_color = "#81c784" if h['P&L']>=0 else "#e57373"
                weight    = (h['Current'] / total_current) * 100
                st.markdown(f"""
                <div class='screener-row'>
                    <div style='flex:2;'>
                        <div style='color:#fff;font-weight:600;'>{h['Stock']}</div>
                        <div style='color:#90caf9;font-size:0.75rem;'>Qty: {h['Qty']} · Avg: ₹{h['Buy Price']:.2f}</div>
                    </div>
                    <div style='flex:1;text-align:center;'>
                        <div style='color:#fff;font-weight:600;'>₹{h['CMP']:.2f}</div>
                        <div style='color:#90caf9;font-size:0.75rem;'>CMP</div>
                    </div>
                    <div style='flex:1;text-align:center;'>
                        <div style='color:{pnl_color};font-weight:700;'>{"+" if h["P&L"]>=0 else ""}₹{h["P&L"]:,.0f}</div>
                        <div style='color:{pnl_color};font-size:0.75rem;'>{"+" if h["P&L %"]>=0 else ""}{h["P&L %"]:.2f}%</div>
                    </div>
                    <div style='flex:1;text-align:center;'>
                        <div style='color:#90caf9;font-size:0.8rem;'>{weight:.1f}%</div>
                        <div style='background:#283593;border-radius:4px;height:4px;margin-top:4px;'>
                            <div style='background:#64b5f6;width:{weight}%;height:4px;border-radius:4px;'></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Portfolio Allocation Pie
            pa1, pa2 = st.columns(2)
            with pa1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>🥧 Allocation</div>", unsafe_allow_html=True)
                fig_pie = px.pie(
                    values=[h['Current'] for h in holdings_data],
                    names=[h['Stock'] for h in holdings_data],
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                fig_pie.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a',
                                      height=280, margin=dict(l=0,r=0,t=0,b=0),
                                      font=dict(color='#90caf9'),
                                      legend=dict(bgcolor='rgba(0,0,0,0)'))
                st.plotly_chart(fig_pie, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with pa2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>📊 P&L by Stock</div>", unsafe_allow_html=True)
                fig_pnl = px.bar(
                    x=[h['Stock'] for h in holdings_data],
                    y=[h['P&L'] for h in holdings_data],
                    color=[h['P&L'] for h in holdings_data],
                    color_continuous_scale=['#e57373','#fff176','#81c784']
                )
                fig_pnl.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                                      height=280, margin=dict(l=0,r=0,t=0,b=0),
                                      font=dict(color='#90caf9'), showlegend=False,
                                      coloraxis_showscale=False)
                fig_pnl.update_xaxes(gridcolor='#283593')
                fig_pnl.update_yaxes(gridcolor='#283593')
                st.plotly_chart(fig_pnl, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Combined Portfolio Performance
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📈 Individual Stock Performance</div>", unsafe_allow_html=True)
            fig_perf = go.Figure()
            colors_list = ['#64b5f6','#81c784','#fff176','#ce93d8','#80cbc4','#e57373','#ffb74d']
            for i, h in enumerate(holdings_data):
                norm = (h['raw']['Close'] / float(h['raw']['Close'].iloc[0])) * 100
                fig_perf.add_trace(go.Scatter(
                    x=h['raw'].index, y=norm,
                    name=h['Stock'],
                    line=dict(color=colors_list[i % len(colors_list)], width=1.5)
                ))
            fig_perf.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a', plot_bgcolor='#1e2a9a',
                                   height=320, font=dict(color='#90caf9'),
                                   margin=dict(l=0,r=0,t=10,b=0),
                                   legend=dict(orientation='h', y=1.05, bgcolor='rgba(0,0,0,0)'))
            fig_perf.update_xaxes(gridcolor='#283593')
            fig_perf.update_yaxes(gridcolor='#283593', title="Normalised (Base 100)")
            st.plotly_chart(fig_perf, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Add stocks to your portfolio using the form above to get started!")

# ── Footer ─────────────────────────────────────────────────────
st.markdown(f"""
<div class='footer-card'>
    <div>
        <strong style='color:#90caf9;font-size:1rem;'>🔭 StockLens</strong>
        <span style='color:#5c6bc0;'> — Indian Market Analytics Platform</span>
    </div>
    <div style='color:#5c6bc0;'>
        📡 NSE · BSE · Yahoo Finance &nbsp;|&nbsp;
        20 NSE + 10 BSE stocks &nbsp;|&nbsp;
        ⚠️ Educational purposes only
    </div>
</div>
""", unsafe_allow_html=True)
