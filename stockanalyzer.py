import streamlit as st
import yfinance as yf
import pandas as pd

# Auto-refresh every 2 minutes using meta refresh tag
refresh_interval = 120  # seconds
st.markdown(f"""
    <meta http-equiv="refresh" content="{refresh_interval}">
""", unsafe_allow_html=True)

st.set_page_config(page_title="NSE Live Stock Monitor", layout="wide")
st.title("📈 NSE Live Stock Dashboard")

# Input for up to 10 stock symbols
default_stocks = "RELIANCE.NS, TCS.NS, INFY.NS"
stock_input = st.text_input(
    "Enter up to 10 NSE stock symbols separated by commas (e.g., RELIANCE.NS, TCS.NS):",
    default_stocks
)

# Parse and validate stock symbols
symbols = [s.strip().upper() for s in stock_input.split(",") if s.strip()]
if len(symbols) > 10:
    st.warning("⚠️ Please enter no more than 10 stock symbols.")
    symbols = symbols[:10]

@st.cache_data(ttl=120)
def get_latest_data(symbols):
    rows = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1d", interval="5m")
            if not df.empty:
                latest = df.iloc[-1]
                rows.append({
                    "Symbol": symbol,
                    "Datetime": latest.name.strftime("%Y-%m-%d %H:%M"),
                    "Open": round(latest["Open"], 2),
                    "High": round(latest["High"], 2),
                    "Low": round(latest["Low"], 2),
                    "Close": round(latest["Close"], 2),
                    "Volume": int(latest["Volume"])
                })
        except Exception as e:
            rows.append({"Symbol": symbol, "Error": str(e)})
    return pd.DataFrame(rows)

# Display combined table
if symbols:
    data = get_latest_data(symbols)
    st.dataframe(data, use_container_width=True)


