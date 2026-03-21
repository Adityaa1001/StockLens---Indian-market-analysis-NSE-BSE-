import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

st.set_page_config(
    page_title="StockLens — HDFC Analytics",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background-color: #1a237e; }

section[data-testid="stSidebar"] {
    background: #0d1257 !important;
    border-right: 1px solid #283593;
}

section[data-testid="stSidebar"] * { color: #90caf9 !important; }

.sidebar-brand {
    padding: 24px 16px 32px;
    border-bottom: 1px solid #283593;
    margin-bottom: 16px;
}

.brand-logo {
    font-size: 1.6rem;
    font-weight: 700;
    color: #90caf9 !important;
    letter-spacing: -0.5px;
}

.brand-sub {
    font-size: 0.75rem;
    color: #5c6bc0 !important;
    margin-top: 2px;
}

.nav-item {
    padding: 10px 16px;
    border-radius: 10px;
    margin: 4px 0;
    cursor: pointer;
    color: #7986cb !important;
    font-size: 0.9rem;
}

.nav-item-active {
    background: #283593;
    color: #90caf9 !important;
    font-weight: 600;
}

.page-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
}

.page-subtitle {
    font-size: 0.85rem;
    color: #90caf9;
    margin-top: 4px;
    margin-bottom: 20px;
}

.card {
    background: #1e2a9a;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.3);
    margin-bottom: 16px;
}

.card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transform: translateY(-2px);
    transition: all 0.2s;
}

.metric-card {
    background: #1e2a9a;
    border-radius: 16px;
    padding: 20px 20px 16px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.3);
    margin-bottom: 16px;
    border-left: 4px solid transparent;
    transition: all 0.2s;
}

.metric-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transform: translateY(-2px);
}

.metric-card-blue   { border-left-color: #64b5f6; }
.metric-card-green  { border-left-color: #81c784; }
.metric-card-red    { border-left-color: #e57373; }
.metric-card-purple { border-left-color: #ce93d8; }
.metric-card-yellow { border-left-color: #fff176; }
.metric-card-teal   { border-left-color: #80cbc4; }

.metric-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    margin-bottom: 12px;
}

.icon-blue   { background: #1565c0; }
.icon-green  { background: #1b5e20; }
.icon-red    { background: #b71c1c; }
.icon-purple { background: #4a148c; }
.icon-yellow { background: #f57f17; }
.icon-teal   { background: #004d40; }

.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}

.metric-label {
    font-size: 0.78rem;
    color: #90caf9;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 4px;
}

.signal-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.pill-buy  { background: #1b5e20; color: #81c784; }
.pill-sell { background: #b71c1c; color: #ef9a9a; }
.pill-hold { background: #f57f17; color: #fff176; }

.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #283593;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #283593;
    font-size: 0.875rem;
}

.stat-row:last-child { border-bottom: none; }
.stat-key   { color: #90caf9; }
.stat-value { font-weight: 600; color: #ffffff; }

.pattern-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 12px;
    background: #283593;
    border-radius: 10px;
    margin-bottom: 8px;
    transition: background 0.2s;
}

.pattern-row:hover { background: #303f9f; }

.footer-card {
    background: #0d1257;
    border-radius: 16px;
    padding: 20px 24px;
    color: #90caf9;
    font-size: 0.82rem;
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <div class='brand-logo'>🔭 StockLens</div>
        <div class='brand-sub'>HDFC Bank Analytics Platform</div>
    </div>
    <div class='nav-item nav-item-active'>📊 &nbsp; Dashboard</div>
    <div class='nav-item'>💹 &nbsp; Price Action</div>
    <div class='nav-item'>📈 &nbsp; Indicators</div>
    <div class='nav-item'>🕯️ &nbsp; Patterns</div>
    <div class='nav-item'>📦 &nbsp; Volume</div>
    <div class='nav-item'>⚙️ &nbsp; Settings</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📅 Date Range**")
    start_date = st.date_input("From", pd.to_datetime("2020-01-01"), label_visibility="collapsed")
    end_date   = st.date_input("To",   pd.to_datetime("2025-03-21"), label_visibility="collapsed")

    st.markdown("**📊 Chart**")
    chart_type = st.selectbox("Type", ["Candlestick", "Line", "OHLC"], label_visibility="collapsed")

    st.markdown("**📈 Overlays**")
    show_sma  = st.checkbox("Moving Averages", value=True)
    show_ema  = st.checkbox("EMA 20",          value=True)
    show_bb   = st.checkbox("Bollinger Bands", value=True)
    show_vwap = st.checkbox("VWAP",            value=False)

    st.markdown("**🕯️ Patterns**")
    show_patterns = st.checkbox("Show on Chart", value=True)

    st.markdown("**🔢 Periods**")
    rsi_period = st.slider("RSI", 7, 28, 14)
    bb_period  = st.slider("BB",  10, 50, 20)

    st.markdown("""
    <div style='background:#283593;border-radius:10px;padding:12px;margin-top:16px;
    font-size:0.75rem;color:#7986cb;'>
    📡 NSE · Yahoo Finance<br>
    🗓️ 2020 – 2025<br>
    🔄 CSV-cached data
    </div>
    """, unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────────
@st.cache_data
def load_data(start, end, rsi_p, bb_p):
    df = pd.read_csv("hdfc_data.csv", index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    df = df[(df.index >= pd.Timestamp(start)) & (df.index <= pd.Timestamp(end))].copy()

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

df = load_data(start_date, end_date, rsi_period, bb_period)

if df.empty:
    st.error("No data found. Please adjust the date range.")
    st.stop()

# ── Computed Values ────────────────────────────────────────────
cur       = df['Close'].iloc[-1]
prev      = df['Close'].iloc[-2]
chg       = cur - prev
chgp      = chg / prev * 100
rsi       = df['RSI'].iloc[-1]
macd      = df['MACD'].iloc[-1]
hi52      = df['High'].tail(252).max()
lo52      = df['Low'].tail(252).min()
total_ret = ((cur / df['Close'].iloc[0]) - 1) * 100
sharpe    = df['Daily_Return'].mean() / df['Daily_Return'].std() * np.sqrt(252)
max_dd    = ((df['Close'] / df['Close'].cummax()) - 1).min() * 100
vol_colors= ['#81c784' if c >= o else '#e57373' for c, o in zip(df['Close'], df['Open'])]

# ── Page Header ────────────────────────────────────────────────
st.markdown(f"""
<div>
    <h1 class='page-title'>Dashboard
        <span style='font-size:0.9rem;font-weight:400;color:#90caf9;margin-left:12px;'>
        NSE: HDFCBANK &nbsp;·&nbsp;
        {df.index[0].strftime('%d %b %Y')} — {df.index[-1].strftime('%d %b %Y')}
        </span>
    </h1>
    <p class='page-subtitle'>
        {'🟢' if chg>=0 else '🔴'} ₹{cur:.2f} &nbsp;
        <strong style='color:{"#81c784" if chg>=0 else "#e57373"}'>
        {'▲' if chg>=0 else '▼'} ₹{abs(chg):.2f} ({chgp:+.2f}%)
        </strong>
        &nbsp;·&nbsp; Last updated: {df.index[-1].strftime('%d %b %Y')}
    </p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────
c1,c2,c3,c4,c5,c6 = st.columns(6)

cards = [
    (c1, "💰", "icon-blue",   "metric-card-blue",   f"₹{cur:.2f}",       "Current Price",  f"{'▲' if chg>=0 else '▼'} {chgp:+.2f}% today",       chg>=0),
    (c2, "📈", "icon-green",  "metric-card-green",  f"₹{hi52:.2f}",      "52W High",       f"{((cur/hi52)-1)*100:.1f}% below high",                False),
    (c3, "📉", "icon-red",    "metric-card-red",    f"₹{lo52:.2f}",      "52W Low",        f"{((cur/lo52)-1)*100:.1f}% above low",                 True),
    (c4, "⚡", "icon-purple", "metric-card-purple", f"{rsi:.1f}",        "RSI (14)",       "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral", rsi<=70),
    (c5, "📊", "icon-yellow", "metric-card-yellow", f"{total_ret:.1f}%", "Total Return",   f"Since {df.index[0].strftime('%b %Y')}",               total_ret>0),
    (c6, "🎯", "icon-teal",   "metric-card-teal",   f"{sharpe:.2f}",     "Sharpe Ratio",   "Risk-adjusted return",                                 sharpe>1),
]

for col, icon, icon_cls, card_cls, val, label, sub, pos in cards:
    color = "#81c784" if pos else "#e57373"
    col.markdown(f"""
    <div class='metric-card {card_cls}'>
        <div class='metric-icon {icon_cls}'>{icon}</div>
        <div class='metric-value'>{val}</div>
        <div class='metric-label'>{label}</div>
        <div style='color:{color};font-size:0.78rem;font-weight:500;margin-top:6px;'>{sub}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Chart + Signals ────────────────────────────────────────────
chart_col, signal_col = st.columns([3, 1])

with chart_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💹 Price Action</div>", unsafe_allow_html=True)

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        row_heights=[0.6, 0.2, 0.2], vertical_spacing=0.02)

    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='HDFC',
            increasing_line_color='#81c784', decreasing_line_color='#e57373'
        ), row=1, col=1)
    elif chart_type == "OHLC":
        fig.add_trace(go.Ohlc(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='HDFC'
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'], name='Close',
            line=dict(color='#64b5f6', width=2),
            fill='tozeroy', fillcolor='rgba(100,181,246,0.1)'
        ), row=1, col=1)

    if show_sma:
        for col_name, color, name in [
            ('SMA_20', '#fff176', 'SMA 20'),
            ('SMA_50', '#81c784', 'SMA 50'),
            ('SMA_200','#e57373', 'SMA 200')
        ]:
            fig.add_trace(go.Scatter(x=df.index, y=df[col_name], name=name,
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
        doji_df   = df[df['Doji']]
        hammer_df = df[df['Hammer']]
        bull_df   = df[df['Bullish_Engulfing']]
        bear_df   = df[df['Bearish_Engulfing']]
        fig.add_trace(go.Scatter(x=doji_df.index, y=doji_df['High']*1.01, mode='markers',
                                 name='Doji', marker=dict(symbol='circle-open', color='#fff176',
                                 size=8, line=dict(width=2))), row=1, col=1)
        fig.add_trace(go.Scatter(x=hammer_df.index, y=hammer_df['Low']*0.99, mode='markers',
                                 name='Hammer', marker=dict(symbol='triangle-up',
                                 color='#81c784', size=10)), row=1, col=1)
        fig.add_trace(go.Scatter(x=bull_df.index, y=bull_df['Low']*0.99, mode='markers',
                                 name='Bull Engulf', marker=dict(symbol='star',
                                 color='#81c784', size=11)), row=1, col=1)
        fig.add_trace(go.Scatter(x=bear_df.index, y=bear_df['High']*1.01, mode='markers',
                                 name='Bear Engulf', marker=dict(symbol='star',
                                 color='#e57373', size=11)), row=1, col=1)

    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
                         marker_color=vol_colors, opacity=0.6), row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI',
                             line=dict(color='#fff176', width=1.5)), row=3, col=1)
    fig.add_hrect(y0=70, y1=100, fillcolor='rgba(229,115,115,0.1)', line_width=0, row=3, col=1)
    fig.add_hrect(y0=0,  y1=30,  fillcolor='rgba(129,199,132,0.1)', line_width=0, row=3, col=1)
    fig.add_hline(y=70, line_dash='dash', line_color='#e57373', line_width=1, row=3, col=1)
    fig.add_hline(y=30, line_dash='dash', line_color='#81c784', line_width=1, row=3, col=1)

    fig.update_layout(
        height=560,
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
        paper_bgcolor='#1e2a9a',
        plot_bgcolor='#1e2a9a',
        legend=dict(orientation='h', yanchor='bottom', y=1.01,
                    bgcolor='rgba(0,0,0,0)', font=dict(size=11, color='#90caf9')),
        font=dict(family='Inter', color='#90caf9'),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    for i in range(1, 4):
        fig.update_xaxes(gridcolor='#283593', showline=False, row=i, col=1)
        fig.update_yaxes(gridcolor='#283593', showline=False, row=i, col=1)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with signal_col:
    rsi_sig  = ("BUY",  "pill-buy")  if rsi < 30 else ("SELL", "pill-sell") if rsi > 70 else ("HOLD", "pill-hold")
    macd_sig = ("BUY",  "pill-buy")  if macd > 0 else ("SELL", "pill-sell")
    sma_sig  = ("BUY",  "pill-buy")  if cur > df['SMA_200'].iloc[-1] else ("SELL", "pill-sell")
    bb_pos   = (cur - df['BB_Lower'].iloc[-1]) / (df['BB_Upper'].iloc[-1] - df['BB_Lower'].iloc[-1])
    bb_sig   = ("BUY",  "pill-buy")  if bb_pos < 0.2 else ("SELL", "pill-sell") if bb_pos > 0.8 else ("HOLD", "pill-hold")
    vol_sig  = ("HIGH", "pill-sell") if df['Volatility'].iloc[-1] > df['Volatility'].mean()*1.5 else ("LOW", "pill-buy")

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
        <div class='pattern-row'><span style='color:#90caf9;font-size:0.85rem;'>Volatility</span>
            <span class='signal-pill {vol_sig[1]}'>{vol_sig[0]}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card'>
        <div class='section-title'>📐 Statistics</div>
        <div class='stat-row'><span class='stat-key'>Mean Price</span>
            <span class='stat-value'>₹{df['Close'].mean():.2f}</span></div>
        <div class='stat-row'><span class='stat-key'>Std Dev</span>
            <span class='stat-value'>₹{df['Close'].std():.2f}</span></div>
        <div class='stat-row'><span class='stat-key'>Best Day</span>
            <span class='stat-value' style='color:#81c784;'>+{df['Daily_Return'].max():.2f}%</span></div>
        <div class='stat-row'><span class='stat-key'>Worst Day</span>
            <span class='stat-value' style='color:#e57373;'>{df['Daily_Return'].min():.2f}%</span></div>
        <div class='stat-row'><span class='stat-key'>Max Drawdown</span>
            <span class='stat-value' style='color:#e57373;'>{max_dd:.2f}%</span></div>
        <div class='stat-row'><span class='stat-key'>Avg Volume</span>
            <span class='stat-value'>{df['Volume'].mean()/1e6:.1f}M</span></div>
        <div class='stat-row'><span class='stat-key'>+ve Days</span>
            <span class='stat-value'>{(df['Daily_Return']>0).mean()*100:.1f}%</span></div>
    </div>
    """, unsafe_allow_html=True)

    total_patterns = int(df['Doji'].sum() + df['Hammer'].sum() +
                         df['Bullish_Engulfing'].sum() + df['Bearish_Engulfing'].sum())
    st.markdown(f"""
    <div class='card'>
        <div class='section-title'>🕯️ Patterns Found</div>
        <div class='pattern-row'><span style='font-size:0.85rem;color:#ffffff;'>🟡 Doji</span>
            <span style='font-weight:700;color:#fff176;'>{int(df['Doji'].sum())}</span></div>
        <div class='pattern-row'><span style='font-size:0.85rem;color:#ffffff;'>🟢 Hammer</span>
            <span style='font-weight:700;color:#81c784;'>{int(df['Hammer'].sum())}</span></div>
        <div class='pattern-row'><span style='font-size:0.85rem;color:#ffffff;'>🔴 Shoot. Star</span>
            <span style='font-weight:700;color:#e57373;'>{int(df['Shooting_Star'].sum())}</span></div>
        <div class='pattern-row'><span style='font-size:0.85rem;color:#ffffff;'>🟢 Bull Engulf</span>
            <span style='font-weight:700;color:#81c784;'>{int(df['Bullish_Engulfing'].sum())}</span></div>
        <div class='pattern-row'><span style='font-size:0.85rem;color:#ffffff;'>🔴 Bear Engulf</span>
            <span style='font-weight:700;color:#e57373;'>{int(df['Bearish_Engulfing'].sum())}</span></div>
        <div style='margin-top:12px;padding-top:12px;border-top:2px solid #283593;
        text-align:center;font-size:0.8rem;color:#90caf9;'>
            {total_patterns} patterns · {len(df)} trading days
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Distribution + Heatmap ─────────────────────────────────────
dist_col, heat_col = st.columns([1, 2])

with dist_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Returns Distribution</div>", unsafe_allow_html=True)
    fig_ret = px.histogram(df['Daily_Return'].dropna(), nbins=50,
                           color_discrete_sequence=['#64b5f6'])
    fig_ret.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a',
                          plot_bgcolor='#1e2a9a', height=260,
                          showlegend=False, margin=dict(l=0,r=0,t=0,b=0),
                          xaxis_title="Daily Return (%)", yaxis_title="Frequency",
                          font=dict(color='#90caf9'))
    fig_ret.update_xaxes(gridcolor='#283593')
    fig_ret.update_yaxes(gridcolor='#283593')
    st.plotly_chart(fig_ret, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with heat_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🗓️ Monthly Returns Heatmap</div>", unsafe_allow_html=True)
    month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                   7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    monthly = df.groupby(['Year','Month'])['Daily_Return'].sum().unstack()
    monthly.columns = [month_names[m] for m in monthly.columns]
    fig_heat = px.imshow(monthly, color_continuous_scale='RdYlGn',
                         aspect='auto', text_auto='.1f')
    fig_heat.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a',
                           plot_bgcolor='#1e2a9a', height=260,
                           margin=dict(l=0,r=0,t=0,b=0),
                           font=dict(color='#90caf9'),
                           coloraxis_showscale=False)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Volume + Volatility ────────────────────────────────────────
vol_col, vola_col = st.columns(2)

with vol_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📦 Volume Analysis</div>", unsafe_allow_html=True)
    df['Vol_MA20'] = df['Volume'].rolling(20).mean()
    fig_v = go.Figure()
    fig_v.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
                           marker_color=vol_colors, opacity=0.5))
    fig_v.add_trace(go.Scatter(x=df.index, y=df['Vol_MA20'], name='MA 20',
                               line=dict(color='#64b5f6', width=2)))
    fig_v.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a',
                        plot_bgcolor='#1e2a9a', height=240,
                        showlegend=True, margin=dict(l=0,r=0,t=0,b=0),
                        font=dict(color='#90caf9'),
                        legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'))
    fig_v.update_xaxes(gridcolor='#283593')
    fig_v.update_yaxes(gridcolor='#283593')
    st.plotly_chart(fig_v, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with vola_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🌊 Rolling Volatility</div>", unsafe_allow_html=True)
    fig_vola = go.Figure()
    fig_vola.add_trace(go.Scatter(x=df.index, y=df['Volatility'], name='Volatility',
                                   fill='tozeroy', fillcolor='rgba(206,147,216,0.15)',
                                   line=dict(color='#ce93d8', width=2)))
    fig_vola.add_hline(y=df['Volatility'].mean(), line_dash='dash',
                       line_color='#fff176', line_width=1.5,
                       annotation_text="Mean", annotation_position="right",
                       annotation_font_color='#fff176')
    fig_vola.update_layout(template='plotly_dark', paper_bgcolor='#1e2a9a',
                           plot_bgcolor='#1e2a9a', height=240,
                           showlegend=False, margin=dict(l=0,r=0,t=0,b=0),
                           font=dict(color='#90caf9'))
    fig_vola.update_xaxes(gridcolor='#283593')
    fig_vola.update_yaxes(gridcolor='#283593')
    st.plotly_chart(fig_vola, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Data Explorer ──────────────────────────────────────────────
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📋 Data Explorer</div>", unsafe_allow_html=True)

exp_c1, exp_c2 = st.columns([3, 1])
with exp_c1:
    show_cols = st.multiselect("Columns",
        options=['Open','High','Low','Close','Volume','RSI','MACD',
                 'BB_Upper','BB_Lower','SMA_20','SMA_50','SMA_200',
                 'EMA_20','ATR','Volatility','Daily_Return','VWAP'],
        default=['Open','High','Low','Close','Volume','RSI','MACD'])
with exp_c2:
    n_rows = st.slider("Rows", 10, 100, 25)

st.dataframe(df[show_cols].tail(n_rows).round(2).sort_index(ascending=False),
             use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown(f"""
<div class='footer-card'>
    <div>
        <strong style='color:#90caf9;font-size:1rem;'>🔭 StockLens</strong>
        <span style='color:#5c6bc0;'> — HDFC Bank Analytics Platform</span>
    </div>
    <div style='color:#5c6bc0;'>
        📡 NSE · Yahoo Finance &nbsp;|&nbsp;
        {len(df)} trading days &nbsp;|&nbsp;
        ⚠️ Educational purposes only
    </div>
</div>
""", unsafe_allow_html=True)
