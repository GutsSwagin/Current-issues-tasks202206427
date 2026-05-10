# pages/questionnaire.py
import streamlit as st
from utils.db import get_connection

def show_therapist_create():
    st.title('Create Pre-Session Questionnaire')
    therapist_id = st.session_state.user.get('therapist_id')
    title = st.text_input('Questionnaire Title', value='Initial Patient Assessment')

    st.markdown('**Add Questions** (minimum 3 recommended)')
    questions = []
    num_q = st.number_input('Number of Questions', min_value=1, max_value=15, value=5)
    for i in range(int(num_q)):
        q_text = st.text_input(f'Question {i+1}', key=f'q_{i}')
        q_type = st.selectbox('Type', ['text', 'scale (1-10)', 'yes/no'], key=f'qt_{i}')
        questions.append({'text': q_text, 'type': q_type})

    if st.button('Save Questionnaire'):
        conn = get_connection()
        conn.execute('INSERT INTO questionnaires (therapist_id, title) VALUES (?, ?)',
                     (therapist_id, title))
        q_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        for q in questions:
            if q['text']:
                conn.execute('INSERT INTO questions (q_id, question_text, question_type) VALUES (?, ?, ?)',
                             (q_id, q['text'], q['type']))
        conn.commit()
        conn.close()
        st.success('Questionnaire saved and assigned to upcoming patients!')

def show_patient_fill(appt_id, q_id):
    st.title('Pre-Session Questionnaire')
    st.info('Your therapist has sent you these questions. Your answers will help make your session more effective.')

    conn = get_connection()
    questions = conn.execute('SELECT * FROM questions WHERE q_id = ?', (q_id,)).fetchall()
    conn.close()

    answers = {}
    for q in questions:
        if q['question_type'] == 'scale (1-10)':
            answers[q['question_id']] = st.slider(q['question_text'], 1, 10, 5)
        elif q['question_type'] == 'yes/no':
            answers[q['question_id']] = st.radio(q['question_text'], ['Yes', 'No'])
        else:
            answers[q['question_id']] = st.text_area(q['question_text'])

    if st.button('Submit Answers'):
        conn = get_connection()
        for q_id_key, answer in answers.items():
            conn.execute(
                'INSERT INTO patient_responses (appt_id, question_id, answer_text) VALUES (?, ?, ?)',
                (appt_id, q_id_key, str(answer))
            )
        conn.commit()
        conn.close()
        st.success('Answers submitted! Your therapist will review them before your session.')
        st.balloons()
