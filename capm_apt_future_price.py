import numpy as np
import streamlit as st


def capm_future_price(current_price, risk_free_rate, market_return, beta, period):
    """
    Calculates the future price of an asset using the Capital Asset Pricing Model (CAPM).
    """
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    future_price = current_price * (1 + expected_return) ** period
    return future_price

def apt_future_price(current_price, factor_returns, factor_sensitivities, period):
    """
    Calculates the future price of an asset using the Arbitrage Pricing Theory (APT) model.
    """
    expected_return = np.dot(factor_returns, factor_sensitivities)
    future_price = current_price * (1 + expected_return) ** period
    return future_price

def display_capm_apt():
    # Streamlit App
    st.title("Future Price Prediction Using CAPM and APT Models")

    st.header("CAPM Model")
    current_price_capm = st.number_input("Current Price of the Asset:", value=3500)
    risk_free_rate = st.number_input("Risk-Free Rate (as a decimal):", value=0.07)
    market_return = st.number_input("Market Return (as a decimal):", value=0.15)
    beta = st.number_input("Beta of the Asset:", value=1.2)
    period_capm = st.number_input("Period (in days):", value=25)
    period_capm = period_capm/365

    if st.button("Calculate Future Price (CAPM)"):
        future_price_capm = capm_future_price(current_price_capm, risk_free_rate, market_return, beta, period_capm)
        st.success(f"Future price using CAPM: {future_price_capm:.2f}")

    st.header("APT Model")
    current_price_apt = st.number_input("Current Price of the Asset (APT):", value=3500)
    num_factors = st.number_input("Number of Factors:", value=2, min_value=1, max_value=10)

    factor_returns = []
    factor_sensitivities = []

    for i in range(num_factors):
        factor_return = st.number_input(f"Expected Return for Factor {i + 1} (as a decimal):", value=0.08)
        factor_sensitivity = st.number_input(f"Sensitivity to Factor {i + 1}:", value=1.0)
        factor_returns.append(factor_return)
        factor_sensitivities.append(factor_sensitivity)

    period_apt = st.number_input("Period (in years for APT):", value=25 / 365)

    if st.button("Calculate Future Price (APT)"):
        future_price_apt = apt_future_price(current_price_apt, factor_returns, factor_sensitivities, period_apt)
        st.success(f"Future price using APT: {future_price_apt:.2f}")

    st.sidebar.header("About")
    st.sidebar.markdown(
        "<p style='word-wrap: break-word;'>This app calculates future asset prices using CAPM and APT models.</p>",
        unsafe_allow_html=True)
