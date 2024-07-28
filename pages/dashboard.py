# pages/dashboard.py
import streamlit as st
import requests
import streamlit.components.v1 as components

def display_lottie_animation(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def app():
    st.title("Dashboard")

    lottie_url = "https://assets4.lottiefiles.com/packages/lf20_q5pk6p1k.json"
    animation = display_lottie_animation(lottie_url)
    if animation:
        components.html(animation)
    else:
        st.error("Failed to load animation")

if __name__ == "__main__":
    app()
