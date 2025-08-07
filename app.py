import streamlit as st
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

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
