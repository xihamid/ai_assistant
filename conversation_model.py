import sqlite3
from datetime import datetime
from database import get_db_connection

class Conversation:
    def __init__(self, id=None, user_id=None, query=None, response=None, timestamp=None):
        self.id = id
        self.user_id = user_id
        self.query = query
        self.response = response
        self.timestamp = timestamp
    
    def save(self):
        """Save conversation to database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if self.id:
            # Update existing conversation
            cursor.execute(
                "UPDATE conversations SET user_id = ?, query = ?, response = ? WHERE id = ?",
                (self.user_id, self.query, self.response, self.id)
            )
        else:
            # Create new conversation
            cursor.execute(
                "INSERT INTO conversations (user_id, query, response) VALUES (?, ?, ?)",
                (self.user_id, self.query, self.response)
            )
            self.id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return self
    
    @staticmethod
    def get_all():
        """Get all conversations"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversations ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversation = Conversation(
                id=row['id'], 
                user_id=row['user_id'], 
                query=row['query'], 
                response=row['response'],
                timestamp=row['timestamp']
            )
            conversations.append(conversation)
        return conversations
    
    @staticmethod
    def get_by_id(conversation_id):
        """Get conversation by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Conversation(
                id=row['id'], 
                user_id=row['user_id'], 
                query=row['query'], 
                response=row['response'],
                timestamp=row['timestamp']
            )
        return None
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get all conversations for a specific user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversations WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversation = Conversation(
                id=row['id'], 
                user_id=row['user_id'], 
                query=row['query'], 
                response=row['response'],
                timestamp=row['timestamp']
            )
            conversations.append(conversation)
        return conversations
    
    @staticmethod
    def delete_by_id(conversation_id):
        """Delete conversation by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    @staticmethod
    def delete_by_user_id(user_id):
        """Delete all conversations for a specific user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def to_dict(self):
        """Convert conversation to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "query": self.query,
            "response": self.response,
            "timestamp": self.timestamp
        }
