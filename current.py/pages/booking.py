# pages/booking.py
import streamlit as st
from utils.db import get_connection

def show():
    if not st.session_state.get('logged_in'):
        st.warning('Please log in to book an appointment.')
        return

    therapist = st.session_state.get('selected_therapist')
    if not therapist:
        st.error('No therapist selected. Please go back.')
        return

    st.title(f"Book a Session with Dr. {therapist['name']}")
    st.markdown(f"**Specialty:** {therapist['specialty']}")
    st.markdown(f"**Price:** ${therapist['price_per_session']} per session")

    conn = get_connection()
    slots = conn.execute(
        'SELECT * FROM availability WHERE therapist_id = ? AND is_booked = 0 ORDER BY slot_date, start_time',
        (therapist['therapist_id'],)
    ).fetchall()
    conn.close()

    if not slots:
        st.info('No available slots for this therapist. Please check back later.')
        return

    slot_options = {f"{s['slot_date']} at {s['start_time']}": s['slot_id'] for s in slots}
    selected_label = st.selectbox('Select Available Time Slot', list(slot_options.keys()))
    selected_slot_id = slot_options[selected_label]

    if st.button('Confirm & Proceed to Payment'):
        st.session_state.booking_slot_id = selected_slot_id
        st.session_state.booking_therapist = therapist
        st.session_state.page = 'Payment'
        st.rerun()
