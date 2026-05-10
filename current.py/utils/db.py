# utils/db.py
import sqlite3
import os

DB_PATH = 'mindbridge.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'patient',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS therapists (
        therapist_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id),
        specialty TEXT,
        price_per_session REAL,
        bio TEXT,
        rating REAL DEFAULT 4.0
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS availability (
        slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        therapist_id INTEGER REFERENCES therapists(therapist_id),
        slot_date TEXT,
        start_time TEXT,
        is_booked INTEGER DEFAULT 0
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        appt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER REFERENCES users(user_id),
        therapist_id INTEGER REFERENCES therapists(therapist_id),
        slot_id INTEGER REFERENCES availability(slot_id),
        status TEXT DEFAULT 'pending',
        payment_id INTEGER
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        appt_id INTEGER,
        amount REAL,
        method TEXT,
        status TEXT DEFAULT 'pending',
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS questionnaires (
        q_id INTEGER PRIMARY KEY AUTOINCREMENT,
        therapist_id INTEGER REFERENCES therapists(therapist_id),
        title TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        q_id INTEGER REFERENCES questionnaires(q_id),
        question_text TEXT,
        question_type TEXT DEFAULT 'text'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS patient_responses (
        response_id INTEGER PRIMARY KEY AUTOINCREMENT,
        appt_id INTEGER REFERENCES appointments(appt_id),
        question_id INTEGER REFERENCES questions(question_id),
        answer_text TEXT,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()
