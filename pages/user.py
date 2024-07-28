# pages/user.py
import streamlit as st
from utils.auth import authenticate

def app():
    st.title("User Page")

    authenticated = authenticate()
    if authenticated:
        st.write("Welcome to your dashboard!")
        st.write("Here you can manage your personal financial data and view insights.")
        # Add more personalized features here
    else:
        st.write("Please login to access this page.")

if __name__ == "__main__":
    app()
