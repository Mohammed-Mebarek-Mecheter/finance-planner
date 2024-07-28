# main.py
import streamlit as st
from pages import investment_simulation, salary_expenses, stock_analysis, budgeting
from pages import retirement_planning, debt_management, goal_tracking, dashboard, admin, user
from utils.auth import register, authenticate

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.sidebar.title("Navigation")
    selected_theme = st.sidebar.selectbox("Select Theme", ["Default", "Dark Mode", "Light Mode", "Classic", "Modern"])

    if selected_theme == "Dark Mode":
        load_css("assets/dark_mode.css")
    elif selected_theme == "Light Mode":
        load_css("assets/light_mode.css")
    elif selected_theme == "Classic":
        load_css("assets/classic_theme.css")
    elif selected_theme == "Modern":
        load_css("assets/modern_theme.css")
    else:
        load_css("assets/default_theme.css")

    pages = ["Login", "Register", "Dashboard", "Investment Simulation", "Salary & Expenses", "Stock Analysis", "Budgeting", "Retirement Planning", "Debt Management", "Goal Tracking", "Admin"]
    if "username" not in st.session_state:
        st.session_state.username = None

    if st.session_state.username:
        selection = st.sidebar.radio("Go to", pages[2:])
        if selection == "Dashboard":
            dashboard.app()
        elif selection == "Investment Simulation":
            investment_simulation.app()
        elif selection == "Salary & Expenses":
            salary_expenses.app()
        elif selection == "Stock Analysis":
            stock_analysis.app()
        elif selection == "Budgeting":
            budgeting.app()
        elif selection == "Retirement Planning":
            retirement_planning.app()
        elif selection == "Debt Management":
            debt_management.app()
        elif selection == "Goal Tracking":
            goal_tracking.app()
        elif selection == "Admin":
            admin.app()
    else:
        selection = st.sidebar.radio("Go to", ["Login", "Register"])
        if selection == "Login":
            if authenticate():
                st.session_state.username = st.session_state.user_id
        elif selection == "Register":
            register()

if __name__ == "__main__":
    main()
