# pages/patient_dashboard.py
import streamlit as st
from utils.db import get_connection

def show():
    if not st.session_state.get('logged_in') or st.session_state.role != 'patient':
        st.warning('Please log in as a patient to view your dashboard.')
        return

    user = st.session_state.user
    st.title(f"Welcome, {user['name']}")
    st.markdown('---')

    tab1, tab2, tab3 = st.tabs(['Upcoming Appointments', 'Questionnaires', 'History'])

    conn = get_connection()
    appts = conn.execute('''
        SELECT a.appt_id, a.status, av.slot_date, av.start_time,
               u.name AS therapist_name, t.specialty
        FROM appointments a
        JOIN therapists t ON a.therapist_id = t.therapist_id
        JOIN users u ON t.user_id = u.user_id
        JOIN availability av ON a.slot_id = av.slot_id
        WHERE a.patient_id = ?
        ORDER BY av.slot_date DESC
    ''', (user['user_id'],)).fetchall()
    conn.close()

    with tab1:
        upcoming = [a for a in appts if a['status'] == 'confirmed']
        if not upcoming:
            st.info('No upcoming appointments. Book one from Find a Therapist!')
        for a in upcoming:
            st.markdown(f"**Dr. {a['therapist_name']}** | {a['specialty']} | {a['slot_date']} at {a['start_time']}")
            st.markdown(f"Status: `{a['status']}`")
            st.markdown('---')

    with tab2:
        st.markdown('**Questionnaires Awaiting Your Response:**')
        st.info('No pending questionnaires at the moment.')
        # In production: query questionnaire assignments for patient

    with tab3:
        st.markdown('**All Past Appointments:**')
        for a in appts:
            st.markdown(f"Dr. {a['therapist_name']} | {a['slot_date']} | Status: `{a['status']}`")
