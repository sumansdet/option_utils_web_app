import streamlit as st

def kelly_criterion(win_probability, return_percentage):
    """
    Calculates the Kelly Criterion.

    Args:
      win_probability: The probability of winning the bet (0 to 1).
      return_percentage: The percentage return on the bet (as a decimal).

    Returns:
      The Kelly Criterion percentage as a decimal, or None if invalid.
    """
    if return_percentage == 0:
        st.error("Return percentage cannot be zero.")
        return None
    kelly_pct = (win_probability * (1 + return_percentage) - 1) / return_percentage
    return kelly_pct


def calculate_expected_return(capital, bet_size, win_probability):
    """
    Calculates the expected return based on the capital, bet size, and win probability.

    Args:
      capital: The total capital available.
      bet_size: The size of the bet.
      win_probability: The probability of winning the bet (as a decimal).

    Returns:
      The expected return in actual figures.
    """
    # Calculate the Kelly percentage
    kelly_pct = bet_size / capital

    # Calculate the return percentage based on Kelly Criterion
    if kelly_pct == win_probability:
        raise ValueError("Kelly percentage cannot equal win probability.")

    expected_return = (win_probability - 1) / (kelly_pct - win_probability)

    return expected_return



def display_position_size():
    st.title("Kelly Criterion and Expected Return Calculator")

    # Input fields for total capital, bet size, win probability, and return percentage
    total_capital = st.number_input("Total Capital", min_value=0.0, value=9300000.0)
    actual_bet_size = st.number_input("Bet Size (Actual)", min_value=0.0, value=100000.0)
    win_probability = st.number_input("Win Probability (%)", min_value=0.0, max_value=100.0, value=81.0) / 100.0
    return_percentage = st.number_input("Return Percentage (%)", min_value=0.0, max_value=200.0, value=25.0) / 100.0

    # Calculate and display the Kelly Criterion percentage
    if st.button("Calculate Kelly Criterion"):
        kelly_pct = kelly_criterion(win_probability, return_percentage)
        if kelly_pct is not None:
            kelly_pct_percentage = kelly_pct * 100
            st.metric("Kelly Criterion (%)", f"{kelly_pct_percentage:.2f}")
            if kelly_pct > 0:
                st.success(f"The optimal bet size according to Kelly Criterion is : {kelly_pct_percentage:.2f}%.")
                st.success(f"The optimal bet value as per Kelly Criterion is: ${kelly_pct_percentage * total_capital/100:,.0f}")

            elif kelly_pct < 0:
                st.warning("The Kelly Criterion suggests not to place a bet.")
            else:
                st.info("The Kelly Criterion suggests a break-even bet size of 0%.")

    # Calculate and display the expected return
    if st.button("Calculate Expected Return"):
        expected_return = calculate_expected_return(total_capital, actual_bet_size, win_probability)
        st.metric("Expected Return (%)", f"{expected_return * 100:.2f}%")
        st.metric("Expected Return (Actual)", f"{expected_return * actual_bet_size:,.0f}")

