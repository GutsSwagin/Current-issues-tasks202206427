# app.py - Mental Health Appointment Booking System
import streamlit as st
from pages import home, auth, therapists, booking, payment, questionnaire
from pages import patient_dashboard, therapist_dashboard, admin
from utils.db import init_db

st.set_page_config(
    page_title='MindBridge - Mental Health Appointments',
    page_icon='🧠',
    layout='wide',
    initial_sidebar_state='expanded'
)

def main():
    init_db()

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None

    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

    page_names = [
        'Home', 'Login', 'Register', 'Find a Therapist',
        'Booking', 'Payment', 'My Dashboard', 'Therapist Dashboard', 'Admin'
    ]
    selected_index = page_names.index(st.session_state.page) if st.session_state.page in page_names else 0
    page = st.sidebar.selectbox('Navigate', page_names, index=selected_index)
    st.session_state.page = page

    if page == 'Home':
        home.show()
    elif page == 'Login':
        auth.show_login()
    elif page == 'Register':
        auth.show_register()
    elif page == 'Find a Therapist':
        therapists.show()
    elif page == 'Booking':
        booking.show()
    elif page == 'Payment':
        payment.show()
    elif page == 'My Dashboard':
        patient_dashboard.show()
    elif page == 'Therapist Dashboard':
        therapist_dashboard.show()
    elif page == 'Admin':
        admin.show()

if __name__ == '__main__':
    main()
