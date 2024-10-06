import streamlit as st
from bsm_opt_pricing import bsm_pricing_page
from payout_chart import display_payoff_chart
from capm_apt_future_price import display_capm_apt
from position_sizing import display_position_size
from option_price_analysis import analyze_option_price

# Define a mapping of options to their respective display functions
options = {
    "Black Scholes Pricing Model": bsm_pricing_page,
    "Options PayOff Chart": display_payoff_chart,
    "CAPM APT Future Price": display_capm_apt,
    "Kelly Criterion - Position Sizing": display_position_size,
    "Analyse Option Pricing": analyze_option_price
}


# Function to display the main menu
def main_menu():
    st.title("Choose Option Utility")

    # Create a radio button for each option
    selected_option = st.radio("",list(options.keys()))

    if st.button("Submit"):
        # Store the selected option in session state
        st.session_state.selected_option = selected_option
        st.session_state.page = "display"


# Function to display the selected option's content
def display_page():
    selected_option = st.session_state.selected_option
    # Button to go back to the main menu
    if st.button("Go to Main Menu"):
        st.session_state.page = "menu"
    # st.title(f"You selected: {selected_option}")
    # Call the display function for the selected option
    options[selected_option]()


# Main application logic
if 'page' not in st.session_state:
    st.session_state.page = "menu"

if st.session_state.page == "menu":
    main_menu()
else:
    display_page()
