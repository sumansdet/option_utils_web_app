import streamlit as st
import numpy as np
from scipy.stats import norm
from datetime import date


def bsm_option_price(S, K, r, T, sigma):
    """
    Calculates the fair value of European call and put options using the Black-Scholes-Merton model.

    Args:
      S (float): Current price of the underlying asset.
      K (float): Option strike price.
      r (float): Risk-free interest rate (annualized).
      T (float): Time to expiration (in years).
      sigma (float): Volatility of the underlying asset (annualized).

    Returns:
      tuple: The fair value of the call option and the put option.
    """

    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate option prices
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return call_price, put_price


def bsm_pricing_page():
    # Streamlit app
    st.title("Black-Scholes-Merton Option Pricing Calculator")

    # Input parameters with Streamlit widgets
    S = st.number_input("Current Underlying Asset Price (S)", value=3493.0)
    K = st.number_input("Strike Price (K)", value=3500.0)
    r = st.number_input("Risk-Free Interest Rate (r)", value=0.07)

    # Date picker for expiration date
    today = date.today()
    expiry_date = st.date_input("Expiration Date", min_value=today, value=today)

    # Calculate time to expiration in years
    T = (expiry_date - today).days / 365

    sigma = st.number_input("Volatility (sigma)", value=0.24)

    # Calculate option prices
    if st.button("Calculate"):
        call_price, put_price = bsm_option_price(S, K, r, T, sigma)
        st.success(f"Call option fair value: {call_price:.2f}")
        st.success(f"Put option fair value: {put_price:.2f}")
