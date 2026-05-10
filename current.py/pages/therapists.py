# pages/therapists.py
import streamlit as st
from utils.db import get_connection

def show():
    st.title('Find a Therapist')
    st.markdown('Browse and filter licensed psychology professionals.')

    col1, col2, col3 = st.columns(3)
    with col1:
        specialty = st.selectbox('Specialty', ['All', 'Anxiety', 'Depression',
                                               'Trauma', 'Relationships', 'Stress'])
    with col2:
        max_price = st.slider('Max Price per Session ($)', 20, 300, 150)
    with col3:
        sort_by = st.selectbox('Sort By', ['Rating', 'Price (Low to High)'])

    conn = get_connection()
    query = '''SELECT t.*, u.name FROM therapists t JOIN users u ON t.user_id = u.user_id
               WHERE t.price_per_session <= ?'''
    params = [max_price]
    if specialty != 'All':
        query += ' AND t.specialty = ?'
        params.append(specialty)
    if sort_by == 'Rating':
        query += ' ORDER BY t.rating DESC'
    else:
        query += ' ORDER BY t.price_per_session ASC'

    therapists = conn.execute(query, params).fetchall()
    conn.close()

    if not therapists:
        st.info('No therapists found matching your filters. Try adjusting the criteria.')
        return

    for t in therapists:
        with st.expander(f"Dr. {t['name']} | {t['specialty']} | ${t['price_per_session']}/session"):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**Bio:** {t['bio']}")
                st.markdown(f"**Rating:** {'⭐' * int(t['rating'])} ({t['rating']}/5)")
            with col_b:
                if st.button('Book Now', key=f"book_{t['therapist_id']}"):
                    st.session_state.selected_therapist = dict(t)
                    st.session_state.page = 'Booking'
                    st.rerun()
