import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm


# Black-Scholes pricing function
def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price

# Option Greeks function
def black_scholes_greeks(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    delta = norm.cdf(d1) if option_type == 'call' else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = (
        - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
        - r * K * np.exp(-r * T) * norm.cdf(d2)
        if option_type == 'call' else
        - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
        + r * K * np.exp(-r * T) * norm.cdf(-d2)
    )
    vega = S * norm.pdf(d1) * np.sqrt(T)
    rho = (
        K * T * np.exp(-r * T) * norm.cdf(d2)
        if option_type == 'call' else
        -K * T * np.exp(-r * T) * norm.cdf(-d2)
    )

    return {
        'Delta': delta,
        'Gamma': gamma,
        'Theta': theta,
        'Vega': vega,
        'Rho': rho
    }


# Pricing function
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price



tab1, tab2 = st.tabs(["Option Calculator", "Backtest Strategy"])

# === TAB 1: Option Calculator ===
with tab1:
    st.header("Black-Scholes Option Pricing Calculator")

    S = st.number_input("Spot Price (S)", value=100.0)
    K = st.number_input("Strike Price (K)", value=100.0)
    T = st.number_input("Time to Maturity (T in years)", value=1.0)
    r = st.number_input("Risk-Free Rate (r)", value=0.05)
    sigma = st.number_input("Volatility (σ)", value=0.2)
    option_type = st.selectbox("Option Type", ['call', 'put'])

    if st.button("Calculate"):
        price = black_scholes_price(S, K, T, r, sigma, option_type)
        greeks = black_scholes_greeks(S, K, T, r, sigma, option_type)

        st.subheader(f"Option Price: ${price:.2f}")
        st.subheader("Greeks:")
        for greek, value in greeks.items():
            st.write(f"{greek}: {value:.4f}")

# === TAB 2: Backtest Strategy ===
with tab2:
    st.header("Backtest Black-Scholes Strategy")

    # === 1. User Inputs ===
    ticker = st.text_input("Enter Ticker (e.g., SPY)", value="SPY")
    strike_price = st.number_input("Strike Price (K)", value=450.0)
    start_date = st.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2023-01-01"))
    holding_period = st.number_input("Holding Period (days)", value=30, step=1)

    if st.button("Run Backtest"):
        try:
            # === 2. Download data ===
            data = yf.download(ticker, start=start_date, end=end_date)
            data['Spot'] = data['Close']
            data['Log Return'] = np.log(data['Close'] / data['Close'].shift(1))
            data['Volatility'] = data['Log Return'].rolling(window=30).std() * np.sqrt(252)
            data.dropna(inplace=True)

            T = holding_period / 252
            r = 0.05

            df = data[['Spot', 'Volatility']].copy()
            df['Strike'] = strike_price
            df['Time'] = T
            df['Rate'] = r

            # === 3. Black-Scholes Pricing ===
            def bs_vec(S, K, T, r, sigma):
                d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
                d2 = d1 - sigma * np.sqrt(T)
                return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

            df['Predicted_Call'] = bs_vec(df['Spot'], df['Strike'], df['Time'], df['Rate'], df['Volatility'])

            # === 4. Simulate Buy-Hold Strategy ===
            returns = []
            dates = []

            for i in range(0, len(df) - holding_period, holding_period):
                buy_price = df['Predicted_Call'].iloc[i]
                sell_price = df['Predicted_Call'].iloc[i + holding_period]
                pnl = (sell_price - buy_price) * 100  # Assume 100 units
                returns.append(pnl)
                dates.append(df.index[i + holding_period])

            result = pd.DataFrame({'Date': dates, 'PnL': returns})
            result['Cumulative'] = result['PnL'].cumsum() + 10000
            result.set_index('Date', inplace=True)

            # === 5. Plot Result ===
            st.subheader("Cumulative Portfolio Value")
            fig, ax = plt.subplots()
            ax.plot(result.index, result['Cumulative'], marker='o')
            ax.set_xlabel("Date")
            ax.set_ylabel("Portfolio Value ($)")
            ax.set_title("Backtest Result")
            ax.grid(True)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error during backtest: {e}")

