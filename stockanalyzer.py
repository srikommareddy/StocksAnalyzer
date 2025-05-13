#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 Stock Price Analyzer")

# User inputs
ticker = st.text_input("Enter stock symbol (e.g., TCS.NS):")
start_date = st.date_input("From date")
end_date = st.date_input("To date")

# Fetch and display data
if ticker and start_date and end_date:
    data = yf.download(ticker, start=start_date, end=end_date)
    #data.index = pd.to_datetime(data.index)

    if not data.empty:
        st.subheader("Historical Prices")
        st.dataframe(data)

        st.subheader("Price Line Chart")

        # Drop NaNs and ensure index is datetime
        data = data.dropna(subset=["Close"])
        data.index = pd.to_datetime(data.index)

        # Plot if data exists
        if not data.empty and "Close" in data.columns:
            st.line_chart(data[["Close"]])
        else:
            st.warning("No valid closing price data available to plot.")


        if st.button("Analyze"):
            # Compute percentage changes
            data['Pct Change'] = data['Close'].pct_change() * 100
            
            max_gain = data['Pct Change'].max()
            max_drop = data['Pct Change'].min()

            st.markdown("### 📊 Analysis")
            st.write(f"✅ Maximum Percentage Gain: **{max_gain:.2f}%**")
            st.write(f"🔻 Maximum Percentage Drop: **{max_drop:.2f}%**")
    else:
        st.warning("No data found. Please check the symbol or date range.")

