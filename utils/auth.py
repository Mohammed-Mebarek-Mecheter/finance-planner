# utils/auth.py
import streamlit as st
import streamlit_authenticator as stauth
from utils.data_storage import get_user, save_user, create_table, hash_password

def authenticate():
    create_table()
    users = get_user()
    usernames = [user['username'] for user in users]
    names = [user['name'] for user in users]
    hashed_passwords = [user['password'] for user in users]

    authenticator = stauth.Authenticate(
        credentials={"usernames": dict(zip(usernames, [{"name": name, "password": password} for name, password in zip(names, hashed_passwords)]))},
        cookie_name="financial_planner",
        key="abcdef",
        cookie_expiry_days=30
    )

    name, authentication_status, username = authenticator.login("Login", "sidebar")

    if authentication_status:
        st.success(f"Welcome {name}")
        st.session_state.user_id = username
        return True
    elif authentication_status == False:
        st.error("Username/password is incorrect")
        return False
    elif authentication_status == None:
        st.warning("Please enter your username and password")
        return False

def register():
    st.sidebar.header("Register")
    new_username = st.sidebar.text_input("Username")
    new_password = st.sidebar.text_input("Password", type='password')
    name = st.sidebar.text_input("Name")
    if st.sidebar.button("Register"):
        if new_username and new_password and name:
            save_user(name, new_username, hash_password(new_password))
            st.sidebar.success("User registered successfully!")
        else:
            st.sidebar.error("Please fill in all fields.")


def reset_password():
    st.header("Reset Password")
    username = st.text_input("Username")
    new_password = st.text_input("New Password", type='password')
    if st.button("Reset Password"):
        if username and new_password:
            users = get_user()
            user_exists = any(user['username'] == username for user in users)
            if user_exists:
                save_user(username, hash_password(new_password))
                st.success("Password reset successfully!")
            else:
                st.error("Username does not exist.")
        else:
            st.error("Please fill in all fields.")

# Ensure tables are created
create_table()
