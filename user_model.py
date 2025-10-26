import sqlite3
import json
from database import get_db_connection
from password_utils import get_password_hash, verify_password

class User:
    def __init__(self, id=None, email=None, password=None, full_name=None, preferences=None, created_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.full_name = full_name
        self.preferences = preferences
        self.created_at = created_at
    
    
    def save(self):
        """Save user to database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if self.id:
            # Update existing user
            cursor.execute(
                "UPDATE users SET email = ?, full_name = ?, preferences = ? WHERE id = ?",
                (self.email, self.full_name, self.preferences, self.id)
            )
        else:
            # Create new user
            hashed_password = get_password_hash(self.password)
            cursor.execute(
                "INSERT INTO users (email, password, full_name, preferences) VALUES (?, ?, ?, ?)",
                (self.email, hashed_password, self.full_name, self.preferences)
            )
            self.id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return self
    
    @staticmethod
    def get_all():
        """Get all users"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        
        users = []
        for row in rows:
            user = User(
                id=row['id'], 
                email=row['email'], 
                full_name=row['full_name'], 
                preferences=row['preferences'],
                created_at=row['created_at']
            )
            users.append(user)
        return users
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row['id'], 
                email=row['email'], 
                full_name=row['full_name'], 
                preferences=row['preferences'],
                created_at=row['created_at']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row['id'], 
                email=row['email'], 
                password=row['password'],
                full_name=row['full_name'], 
                preferences=row['preferences'],
                created_at=row['created_at']
            )
        return None
    
    def verify_password(self, password):
        """Verify password"""
        return verify_password(password, self.password)
    
    @staticmethod
    def delete_by_id(user_id):
        """Delete user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def get_preferences_dict(self):
        """Get preferences as dictionary"""
        if self.preferences:
            try:
                return json.loads(self.preferences)
            except:
                return {"summary_length": "medium", "preferred_topics": []}
        return {"summary_length": "medium", "preferred_topics": []}
    
    def set_preferences_dict(self, preferences_dict):
        """Set preferences from dictionary"""
        self.preferences = json.dumps(preferences_dict)
    
    def to_dict(self):
        """Convert user to dictionary (without password)"""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "preferences": self.get_preferences_dict(),
            "created_at": self.created_at
        }
