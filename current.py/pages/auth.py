# pages/auth.py
import streamlit as st
import bcrypt
from utils.db import get_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def show_register():
    st.title('Create Your Account')
    st.markdown('Join MindBridge to connect with psychology experts.')
    name = st.text_input('Full Name')
    email = st.text_input('Email Address')
    password = st.text_input('Password', type='password')
    confirm = st.text_input('Confirm Password', type='password')
    role = st.selectbox('Register as', ['patient', 'therapist'])

    if st.button('Create Account'):
        if not name or not email or not password:
            st.error('Please fill in all fields.')
        elif password != confirm:
            st.error('Passwords do not match.')
        else:
            try:
                conn = get_connection()
                conn.execute(
                    'INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)',
                    (name, email, hash_password(password), role)
                )
                conn.commit()
                conn.close()
                st.success('Account created! Please log in.')
            except Exception as e:
                st.error(f'Registration failed: {e}')

def show_login():
    st.title('Welcome Back')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        conn = get_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user and verify_password(password, user['password_hash']):
            st.session_state.logged_in = True
            st.session_state.user = dict(user)
            st.session_state.role = user['role']
            st.success(f"Welcome, {user['name']}!")
            st.rerun()
        else:
            st.error('Invalid email or password.')
