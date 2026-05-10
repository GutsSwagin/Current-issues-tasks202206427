# pages/payment.py
import streamlit as st
from utils.db import get_connection
import datetime

def show():
    if not st.session_state.get('logged_in'):
        st.warning('Please log in.')
        return

    therapist = st.session_state.get('booking_therapist')
    slot_id = st.session_state.get('booking_slot_id')

    st.title('Secure Payment')
    st.markdown(f"**Session Cost: ${therapist['price_per_session']}**")

    method = st.radio('Payment Method', ['Credit Card', 'Debit Card', 'Digital Wallet'])

    if method in ['Credit Card', 'Debit Card']:
        card_num = st.text_input('Card Number (16 digits)', max_chars=16)
        col1, col2 = st.columns(2)
        with col1:
            expiry = st.text_input('Expiry (MM/YY)')
        with col2:
            cvv = st.text_input('CVV', type='password', max_chars=3)
    else:
        wallet_id = st.text_input('Wallet ID / Phone Number')

    if st.button('Pay & Confirm Booking'):
        patient_id = st.session_state.user['user_id']
        therapist_id = therapist['therapist_id']
        amount = therapist['price_per_session']

        conn = get_connection()
        conn.execute('UPDATE availability SET is_booked = 1 WHERE slot_id = ?', (slot_id,))
        conn.execute(
            'INSERT INTO appointments (patient_id, therapist_id, slot_id, status) VALUES (?, ?, ?, ?)',
            (patient_id, therapist_id, slot_id, 'confirmed')
        )
        appt_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.execute(
            'INSERT INTO payments (appt_id, amount, method, status) VALUES (?, ?, ?, ?)',
            (appt_id, amount, method, 'completed')
        )
        conn.commit()
        conn.close()

        st.success('Payment successful! Your appointment is confirmed.')
        st.info('Your therapist will send you a pre-session questionnaire. Check your dashboard!')
        st.balloons()
