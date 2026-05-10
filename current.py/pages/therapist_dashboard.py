# pages/therapist_dashboard.py
import streamlit as st
from utils.db import get_connection

def show():
    if not st.session_state.get('logged_in') or st.session_state.role != 'therapist':
        st.warning('Access restricted to therapists.')
        return

    user = st.session_state.user
    st.title(f"Therapist Panel - Dr. {user['name']}")

    conn = get_connection()
    therapist = conn.execute('SELECT * FROM therapists WHERE user_id = ?',
                             (user['user_id'],)).fetchone()

    tab1, tab2, tab3 = st.tabs(['My Schedule', 'Patient Responses', 'Create Questionnaire'])

    with tab1:
        appts = conn.execute('''
            SELECT a.appt_id, av.slot_date, av.start_time, u.name AS patient_name
            FROM appointments a
            JOIN availability av ON a.slot_id = av.slot_id
            JOIN users u ON a.patient_id = u.user_id
            WHERE a.therapist_id = ? AND a.status = 'confirmed'
            ORDER BY av.slot_date ASC
        ''', (therapist['therapist_id'],)).fetchall()
        if not appts:
            st.info('No confirmed appointments yet.')
        for a in appts:
            st.markdown(f"**Patient:** {a['patient_name']} | {a['slot_date']} at {a['start_time']}")

    with tab2:
        st.markdown('**Submitted Patient Questionnaire Responses:**')
        responses = conn.execute('''
            SELECT pr.answer_text, q.question_text, u.name AS patient_name
            FROM patient_responses pr
            JOIN questions q ON pr.question_id = q.question_id
            JOIN appointments a ON pr.appt_id = a.appt_id
            JOIN users u ON a.patient_id = u.user_id
            WHERE a.therapist_id = ?
        ''', (therapist['therapist_id'],)).fetchall()
        if not responses:
            st.info('No questionnaire responses received yet.')
        for r in responses:
            st.markdown(f"**{r['patient_name']}** answered: *{r['question_text']}*")
            st.markdown(f"> {r['answer_text']}")

    with tab3:
        from pages import questionnaire
        questionnaire.show_therapist_create()

    conn.close()
