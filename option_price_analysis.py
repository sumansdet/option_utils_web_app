import streamlit as st
from scipy.stats import norm
import numpy as np
from datetime import datetime

st.title("Option Pricing and Analysis Tool")


def black_scholes_merton(S, K, r, sigma, T):
    """Calculates the Black-Scholes-Merton value of a call option."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def chance_of_profit(S, K, mu, sigma, T):
    """Calculates the chance of profit for a call option."""
    d5 = (np.log(S / K) + mu * T) / (sigma * np.sqrt(T))
    return norm.cdf(d5)


def median_final_price(S, mu, T):
    """Calculates the median final underlying price."""
    return S * np.exp(mu * T)


def generalized_sharpe_ratio(SR, lambda_3, lambda_4):
    """Calculates the generalized Sharpe ratio."""
    return SR / (1 - lambda_3 * SR + (lambda_4 - 1) * SR ** 2 / 4)


def profit(theta, volatility, difference, time):
    """Calculates the profit of an option trade."""
    return theta * volatility * difference * time


def analyze_option_price():
    """Main function to analyze option prices."""
    # Input fields with default values
    params = {
        "Underlying Price (S)": 3493.0,
        "Strike Price (K)": 3500.0,
        "Risk-Free Interest Rate (r)": 0.07,
        "Volatility (sigma)": 0.24,
        "Drift (mu)": 0.1,
        # "Call Strike Price (S_c)": 105.0,
        "Sharpe Ratio (SR)": 1.0,
        "Skewness (lambda_3)": 0.0,
        "Kurtosis (lambda_4)": 3.0,
        "Theta (theta)": 0.1,
        # "Difference": 5.0,
        "Expiration Date": datetime.today().date()  # Default to today's date
    }

    S = st.number_input("Underlying Price (S)", value=params["Underlying Price (S)"])
    K = st.number_input("Strike Price (K)", value=params["Strike Price (K)"])
    r = st.number_input("Risk-Free Interest Rate (r)", value=params["Risk-Free Interest Rate (r)"])
    sigma = st.number_input("Volatility (sigma)", value=params["Volatility (sigma)"])
    mu = st.number_input("Drift (mu)", value=params["Drift (mu)"])
    # S_c = st.number_input("Call Strike Price (S_c)", value=params["Call Strike Price (S_c)"])
    SR = st.number_input("Sharpe Ratio (SR)", value=params["Sharpe Ratio (SR)"])
    lambda_3 = st.number_input("Skewness (lambda_3)", value=params["Skewness (lambda_3)"])
    lambda_4 = st.number_input("Kurtosis (lambda_4)", value=params["Kurtosis (lambda_4)"])
    theta = st.number_input("Theta (theta)", value=params["Theta (theta)"])
  #  difference = st.number_input("Difference", value=params["Difference"])
    difference = S - K
    # Date picker for expiration date
    expiration_date = st.date_input("Expiration Date", value=params["Expiration Date"])

    # Calculate time to expiration in years
    today = datetime.today().date()  # Get today's date as a date object
    T = (expiration_date - today).days / 365.0

    # Calculate and display results
    if st.button("Calculate"):
        call_value = black_scholes_merton(S, K, r, sigma, T)
        st.write(f"**BSM Call Option Value:** {call_value:.2f}")

        profit_chance = chance_of_profit(S, K, mu, sigma, T)
        st.write(f"**Chance of Profit:** {profit_chance * 100:.2f}%")

        median_price = median_final_price(S, mu, T)
        st.write(f"**Median Final Underlying Price:** {median_price:.2f}")

        gen_sharpe = generalized_sharpe_ratio(SR, lambda_3, lambda_4)
        st.write(f"**Generalized Sharpe Ratio:** {gen_sharpe:.2f}")

        trade_profit = profit(theta, sigma, difference, (expiration_date - today).days)
        st.write(f"**Profit:** {trade_profit:.2f}")


# if __name__ == "__main__":
  #  analyze_option_price()
