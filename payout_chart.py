import streamlit as st
import plotly.graph_objects as go
import numpy as np


def option_payoff(sT, strike_price, option_type, premium, lot_size, position):
    """Calculates the payoff for a single option."""
    if option_type == 'call':
        payoff = np.where(sT > strike_price, (sT - strike_price) * lot_size - (premium * lot_size), -premium * lot_size)
    elif option_type == 'put':
        payoff = np.where(sT < strike_price, (strike_price - sT) * lot_size - (premium * lot_size), -premium * lot_size)
    else:
        raise ValueError("Invalid option type. Must be 'call' or 'put'.")

    return payoff if position == 'long' else -payoff


def stock_payoff(sT, buy_price, qty):
    """Calculates the payoff for a stock position."""
    return (sT - buy_price) * qty


def plot_payoff(spot_price, options, stock_position, lot_size, selected_options):
    """Plots the payoff diagram using Plotly."""
    sT = np.arange(0.7 * spot_price, 1.3 * spot_price, 1)  # Stock price range
    total_payoff = np.zeros_like(sT)

    fig = go.Figure()

    # Add stock payoff if available
    if stock_position and stock_position['qty'] >= 0:
        stock_payoff_values = stock_payoff(sT, stock_position['buy_price'], stock_position['qty'])
        total_payoff += stock_payoff_values
        fig.add_trace(go.Scatter(x=sT, y=stock_payoff_values, mode='lines',
                                 name=f"Stock: {stock_position['qty']} shares"))

    if options and selected_options:
        for index in selected_options:
            option = options[index]
            strike_price = option['strike_price']
            option_type = option['option_type']
            premium = option['premium']
            position = option['position']
            payoff = option_payoff(sT, strike_price, option_type, premium, lot_size, position)
            total_payoff += payoff

            fig.add_trace(go.Scatter(x=sT, y=payoff, mode='lines',
                                     name=f"{position.upper()} {option_type.upper()} Strike: {strike_price}"))

    fig.add_trace(go.Scatter(x=sT, y=total_payoff, mode='lines',
                             name='Total Payoff', line=dict(color='green', width=4)))

    # Current price line
    fig.add_shape(go.layout.Shape(type="line", x0=spot_price, x1=spot_price, y0=min(total_payoff),
                                  y1=max(total_payoff), line=dict(color="gray", dash="dash"),
                                  name='Current Price'))

    # Zero line
    fig.add_shape(go.layout.Shape(type="line", x0=min(sT), x1=max(sT), y0=0, y1=0,
                                  line=dict(color="gray", dash="dash")))

    fig.update_layout(
        title='Option Payoff Diagram',
        xaxis_title='Stock Price at Expiration',
        yaxis_title='Profit and Loss',
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        width=800,  # Set the desired width in pixels
        height=600,
        # legend=dict(x=0.01, y=0.99, bordercolor="White", borderwidth=1)
        legend=dict(
            x=1,  # position horizontally
            y=1,  # position vertically
            traceorder="normal",  # Order of traces in legend
            font=dict(size=10),  # Font size
            # bgcolor="LightSteelBlue",  # Background color of the legend
            bordercolor="Black",  # Border color of the legend
            borderwidth=1,  # Border width of the legend
            title_font=dict(size=12)  # Title font size (if needed)
        )
    )

    return fig


def display_payoff_chart():
    """Streamlit web app."""
    st.title("Option Payoff Calculator")

    # Input fields in sidebar
    with st.sidebar:
        st.header("User Inputs")

        spot_price = st.number_input("Enter the current stock price: ", value=100)
        lot_size = st.number_input("Enter the lot size: ", value=100)

        # Initialize session state for stock and options
        if 'options' not in st.session_state:
            st.session_state.options = []
        if 'stock_position' not in st.session_state:
            st.session_state.stock_position = None  # Initialize stock position as None

        # Add Option Form
        with st.form("option_form"):
            option_type = st.selectbox("Option type:", ("call", "put"))
            strike_price = st.number_input("Strike price:", key="strike_price_input")
            premium = st.number_input("Premium:", key="premium_input")
            position = st.selectbox("Position:", ("long", "short"))
            option_submitted = st.form_submit_button("Submit Option")

        if option_submitted:
            if strike_price >= 0 and premium >= 0:
                # Add option to session state outside form block
                st.session_state.options.append({
                    'strike_price': strike_price,
                    'option_type': option_type,
                    'premium': premium,
                    'position': position
                })
                st.success("Option added successfully!")
            else:
                st.error("Invalid option input!")

        # Add Stock Form
        with st.form("stock_form"):
            stock_qty = st.number_input("Number of shares:", key="stock_qty_input")
            stock_buy_price = st.number_input("Average buy price:", key="stock_buy_price_input")
            stock_submitted = st.form_submit_button("Submit Stock")

        if stock_submitted:
            if stock_qty >= 0 and stock_buy_price >= 0:
                # Update session state with stock info outside the form
                st.session_state.stock_position = {
                    'buy_price': stock_buy_price,
                    'qty': stock_qty
                }
                st.success("Stock added successfully!")
            else:
                st.error("Invalid stock input!")

        # Clear Options Button
        if st.button("Clear Options"):
            st.session_state.options = []  # Clear all options
            st.success("All options cleared!")

    # Display Checkboxes for Options
    st.header("Select Options to Include in Payoff Chart")
    selected_options = []
    for i, option in enumerate(st.session_state.options):
        if st.checkbox(f"{option['position'].capitalize()} {option['option_type'].capitalize()} Strike: {option['strike_price']}", value=True, key=f"option_{i}"):
            selected_options.append(i)

    # Debugging
    st.write("Current Options:", st.session_state.options)
    st.write("Current Stock Position:", st.session_state.stock_position)

    # Plot the payoff diagram in the main window
    fig = plot_payoff(spot_price, st.session_state.options, st.session_state.stock_position, lot_size, selected_options)
    st.plotly_chart(fig)


# if __name__ == "__main__":
#     main()
