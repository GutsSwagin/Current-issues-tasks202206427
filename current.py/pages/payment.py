import streamlit as st
from utils.db import get_connection


def show():
    if not st.session_state.get('logged_in'):
        st.warning('Please log in to complete payment.')
        return

    therapist = st.session_state.get('booking_therapist')
    slot_id = st.session_state.get('booking_slot_id')
    if not therapist or not slot_id:
        st.warning('No booking information found. Please choose a therapist and a slot first.')
        return

    st.title('Confirm Payment')
    st.markdown(f"**Therapist:** Dr. {therapist['name']}")
    st.markdown(f"**Specialty:** {therapist['specialty']}")
    st.markdown(f"**Price:** ${therapist['price_per_session']}")

    conn = get_connection()
    slot = conn.execute('SELECT * FROM availability WHERE slot_id = ?', (slot_id,)).fetchone()
    conn.close()

    if not slot:
        st.error('Selected slot no longer exists.')
        return

    st.markdown(f"**Appointment Time:** {slot['slot_date']} at {slot['start_time']}")

    if st.button('Confirm Payment and Book'):
        user = st.session_state.user
        conn = get_connection()
        conn.execute('UPDATE availability SET is_booked = 1 WHERE slot_id = ?', (slot_id,))
        conn.execute(
            'INSERT INTO appointments (patient_id, therapist_id, slot_id, status) VALUES (?, ?, ?, ?)',
            (user['user_id'], therapist['therapist_id'], slot_id, 'confirmed')
        )
        conn.commit()
        conn.close()
        st.success('Your appointment is confirmed! Return to My Dashboard for details.')
        st.session_state.page = 'My Dashboard'
        st.rerun()
