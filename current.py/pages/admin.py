import streamlit as st


def show():
    if not st.session_state.get('logged_in'):
        st.warning('Please log in to view admin tools.')
        return

    if st.session_state.role != 'admin':
        st.warning('Admin access only.')
        return

    st.title('Admin Dashboard')
    st.markdown('Admin tools are coming soon. Here you can manage users, appointments, and therapists.')
