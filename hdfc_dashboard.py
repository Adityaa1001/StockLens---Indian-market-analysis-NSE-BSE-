import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="HDFC Bank Price Action Dashboard", page_icon="📈", layout="wide")
st.title("📈 HDFC Bank Price Action Dashboard")
st.markdown("Real-time technical analysis · NSE: HDFCBANK")

st.sidebar.header("⚙️ Settings")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date   = st.sidebar.date_input("End Date",   pd.to_datetime("2025-03-21"))
chart_type = st.sidebar.selectbox("Chart Type", ["Candlestick", "Line"])
show_sma   = st.sidebar.checkbox("Show SMA (20/50/200)", value=True)
show_ema   = st.sidebar.checkbox("Show EMA (20)",        value=True)
show_bb    = st.sidebar.checkbox("Show Bollinger Bands", value=True)

@st.cache_data
def load_data(start, end):
    df = pd.read_csv("hdfc_data.csv", index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    df = df[(df.index >= pd.Timestamp(start)) & (df.index <= pd.Timestamp(end))].copy()

    df['SMA_20']  = df['Close'].rolling(20).mean()
    df['SMA_50']  = df['Close'].rolling(50).mean()
    df['SMA_200'] = df['Close'].rolling(200).mean()
    df['EMA_20']  = df['Close'].ewm(span=20, adjust=False).mean()
    df['BB_Mid']   = df['Close'].rolling(20).mean()
    df['BB_Upper'] = df['BB_Mid'] + 2 * df['Close'].rolling(20).std()
    df['BB_Lower'] = df['BB_Mid'] - 2 * df['Close'].rolling(20).std()

    delta = df['Close'].diff()
    gain  = delta.where(delta > 0, 0).rolling(14).mean()
    loss  = -delta.where(delta < 0, 0).rolling(14).mean()
    df['RSI'] = 100 - (100 / (1 + gain / loss))

    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD']        = ema12 - ema26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist']   = df['MACD'] - df['MACD_Signal']

    df['Body']         = abs(df['Close'] - df['Open'])
    df['Body_Range']   = df['High'] - df['Low']
    df['Upper_Shadow'] = df['High'] - df[['Close','Open']].max(axis=1)
    df['Lower_Shadow'] = df[['Close','Open']].min(axis=1) - df['Low']
    df['Doji']              = df['Body'] <= 0.1 * df['Body_Range']
    df['Hammer']            = (df['Lower_Shadow'] >= 2*df['Body']) & (df['Upper_Shadow'] <= 0.1*df['Body_Range']) & (df['Body'] > 0)
    df['Bullish_Engulfing'] = (df['Close']>df['Open']) & (df['Close'].shift(1)<df['Open'].shift(1)) & (df['Close']>df['Open'].shift(1)) & (df['Open']<df['Close'].shift(1))
    df['Bearish_Engulfing'] = (df['Close']<df['Open']) & (df['Close'].shift(1)>df['Open'].shift(1)) & (df['Close']<df['Open'].shift(1)) & (df['Open']>df['Close'].shift(1))
    return df

df = load_data(start_date, end_date)

if df.empty:
    st.error("No data found. Please check the date range.")
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────
st.subheader("📊 Key Metrics")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Current Price", f"₹{df['Close'].iloc[-1]:.2f}")
kpi2.metric("52W High",      f"₹{df['High'].tail(252).max():.2f}")
kpi3.metric("52W Low",       f"₹{df['Low'].tail(252).min():.2f}")
kpi4.metric("Avg Volume",    f"{df['Volume'].mean()/1e6:.2f}M")
kpi5.metric("RSI (latest)",  f"{df['RSI'].iloc[-1]:.1f}")

st.divider()

# ── Main Chart ────────────────────────────────────────────────
st.subheader("💹 Price Chart")
fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    row_heights=[0.6, 0.2, 0.2], vertical_spacing=0.03)

if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                  low=df['Low'], close=df['Close'], name='HDFC Bank'), row=1, col=1)
else:
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close',
                             line=dict(color='royalblue', width=1.5)), row=1, col=1)

if show_sma:
    for col, color, name in [('SMA_20','orange','SMA 20'),('SMA_50','green','SMA 50'),('SMA_200','red','SMA 200')]:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=name, line=dict(color=color, width=1)), row=1, col=1)

if show_ema:
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], name='EMA 20',
                             line=dict(color='purple', width=1, dash='dash')), row=1, col=1)

if show_bb:
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper',
                             line=dict(color='gray', width=0.8, dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower',
                             line=dict(color='gray', width=0.8, dash='dot'),
                             fill='tonexty', fillcolor='rgba(128,128,128,0.1)'), row=1, col=1)

colors = ['green' if c >= o else 'red' for c, o in zip(df['Close'], df['Open'])]
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
                     marker_color=colors, opacity=0.6), row=2, col=1)

fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI',
                         line=dict(color='darkorange', width=1)), row=3, col=1)
fig.add_hline(y=70, line_dash='dash', line_color='red',   row=3, col=1)
fig.add_hline(y=30, line_dash='dash', line_color='green', row=3, col=1)

fig.update_layout(height=700, xaxis_rangeslider_visible=False,
                  template='plotly_dark',
                  legend=dict(orientation='h', yanchor='bottom', y=1.02))
fig.update_yaxes(title_text="Price (INR)", row=1, col=1)
fig.update_yaxes(title_text="Volume",      row=2, col=1)
fig.update_yaxes(title_text="RSI",         row=3, col=1)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── MACD ──────────────────────────────────────────────────────
st.subheader("📉 MACD")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df.index, y=df['MACD'],        name='MACD',   line=dict(color='blue',  width=1.2)))
fig2.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal', line=dict(color='red',   width=1.2)))
fig2.add_trace(go.Bar(    x=df.index, y=df['MACD_Hist'],   name='Hist',
                          marker_color=['green' if v >= 0 else 'red' for v in df['MACD_Hist']], opacity=0.6))
fig2.update_layout(height=300, template='plotly_dark', xaxis_rangeslider_visible=False)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Pattern Summary ───────────────────────────────────────────
st.subheader("🕯️ Candlestick Pattern Summary")
p1, p2, p3, p4 = st.columns(4)
p1.metric("Doji",              int(df['Doji'].sum()))
p2.metric("Hammer",            int(df['Hammer'].sum()))
p3.metric("Bullish Engulfing", int(df['Bullish_Engulfing'].sum()))
p4.metric("Bearish Engulfing", int(df['Bearish_Engulfing'].sum()))

st.divider()

# ── Raw Data ──────────────────────────────────────────────────
st.subheader("📋 Raw Data")
st.dataframe(df[['Open','High','Low','Close','Volume','RSI','MACD','SMA_20','SMA_50']].tail(50).round(2),
             use_container_width=True)
