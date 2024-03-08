import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.title("Investment Simulation")
    st.header("Simulate Your Investment Growth Over Time")

    # Interactive widgets for input
    initial_investment = st.number_input("Enter Initial Investment Amount:", min_value=0.0, step=100.0)
    annual_interest_rate = st.slider("Annual Interest Rate (%):", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
    investment_duration = st.slider("Investment Duration (Years):", min_value=1, max_value=30, value=10, step=1)

    # Calculate investment growth
    years = np.arange(1, investment_duration + 1)
    interest_rate = 1 + (annual_interest_rate / 100)
    investment_growth = initial_investment * (interest_rate ** years)

    # Create a DataFrame to store investment data
    investment_data = pd.DataFrame({
        "Year": years,
        "Investment Value": investment_growth
    })

    # Display investment data
    st.subheader("Investment Growth Over Time")
    st.write(investment_data)

    # Plot investment growth
    st.subheader("Investment Growth Visualization")
    fig, ax = plt.subplots()
    ax.plot(years, investment_growth, marker='o', linestyle='-')
    ax.set_xlabel("Years")
    ax.set_ylabel("Investment Value ($)")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
