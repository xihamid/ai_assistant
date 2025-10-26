import sqlite3
import os

# Database file path
DATABASE_FILE = "ai_assistant.db"

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_database():
    """Initialize database and create tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop existing tables to start fresh
    cursor.execute('DROP TABLE IF EXISTS conversations')
    cursor.execute('DROP TABLE IF EXISTS users')
    
    # Create users table with email, password, full_name
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            preferences TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create conversations table
    cursor.execute('''
        CREATE TABLE conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with fresh tables!")

def close_db_connection(conn):
    """Close database connection"""
    if conn:
        conn.close()
