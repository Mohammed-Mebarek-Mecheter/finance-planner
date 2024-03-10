import streamlit as st
import time
from pages import salary_expenses
from pages import investment_simulation

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Salary & Expenses", "Investment Simulation"])

    if page == "Home":
        home_page()
    elif page == "Salary & Expenses":
        salary_expenses.main()
    elif page == "Investment Simulation":
        investment_simulation.main()

def home_page():
    st.title("Welcome to Financial Planning App")
    st.write("This app helps you plan your financial future.")

    # Displaying text
    st.header("Overview")
    st.markdown("This app provides various tools and simulations to help you plan your finances effectively.")
    st.write("Explore the sidebar to access different functionalities.")

    # Displaying progress and status
    st.header("Progress and Status")
    with st.spinner("Loading..."):
        time.sleep(1)
        st.success("Loaded successfully!")

if __name__ == "__main__":
    main()

st.markdown(
    """
    Made with ❤️ by [Mebarek](https://www.linkedin.com/in/mohammed-mecheter/). 
    [GitHub](https://github.com/Mohammed-Mebarek-Mecheter/) | 
    [LinkedIn](https://www.linkedin.com/in/mohammed-mecheter/) | 
    [Portfolio](https://mebarek.pages.dev/)
    """
)