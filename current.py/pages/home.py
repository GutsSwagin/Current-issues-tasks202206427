import streamlit as st


def show():
    st.title('MindBridge')
    st.markdown('Welcome to MindBridge — connect with psychology professionals, manage appointments, and complete pre-session questionnaires.')
    st.markdown('Use the sidebar to log in, register, or find a therapist.')
    if st.session_state.get('logged_in'):
        st.success(f"You are signed in as {st.session_state.user['name']} ({st.session_state.role}).")
    else:
        st.info('Not signed in yet? Use the Login or Register page from the sidebar.')
