# Black-Scholes Option Pricing Tool

This is a deployed Streamlit web app that uses the Black-Scholes model to calculate European call and put option prices, display the Greeks, and now also **backtest a theoretical trading strategy** using historical stock data.


## Features

### Option Pricing Calculator
- Input Spot Price, Strike Price, Interest Rate, Volatility, Time to Maturity
- Calculates Option Prices for both **Call** and **Put** options
- Displays the full set of Greeks:
  - Delta, Gamma, Theta, Vega, Rho

### Backtest Strategy Simulator
- Enter a stock ticker (e.g., SPY)
- Choose strike price, date range, and holding period
- Pulls historical data from Yahoo Finance
- Calculates rolling volatility and predicts call option values using Black-Scholes
- Simulates a **buy/sell strategy** on model-predicted prices
- Displays **cumulative portfolio value** over time

---

## Technologies Used

- **Python**
- **NumPy**, **SciPy** – for numerical math and the Black-Scholes model
- **Pandas** – for data manipulation
- **Matplotlib** – for visualization
- **Streamlit** – for frontend UI
- **yfinance** – for historical stock data
- **GitHub** – for version control and CI/CD via Streamlit Cloud

## Live App
[Click here to view the live app](https://black-scholes-ui-q894ymwpsimvvoyhzewl3l.streamlit.app)

## How to Run Locally
1. Clone this repo
2. Run `pip install -r requirements.txt`
3. Run `streamlit run app.py`
