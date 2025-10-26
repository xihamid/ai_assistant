from fastapi import HTTPException
from conversation_model import Conversation
from user_model import User

class ConversationController:
    
    @staticmethod
    def create_conversation(user_id, query, response):
        """Create a new conversation"""
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        if not response:
            raise HTTPException(status_code=400, detail="Response is required")
        
        # Check if user exists
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        conversation = Conversation(user_id=user_id, query=query, response=response)
        conversation.save()
        return conversation.to_dict()
    
    @staticmethod
    def get_all_conversations():
        """Get all conversations"""
        conversations = Conversation.get_all()
        return [conversation.to_dict() for conversation in conversations]
    
    @staticmethod
    def get_conversation_by_id(conversation_id):
        """Get conversation by ID"""
        conversation = Conversation.get_by_id(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation.to_dict()
    
    @staticmethod
    def get_conversations_by_user(user_id):
        """Get all conversations for a specific user"""
        # Check if user exists
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        conversations = Conversation.get_by_user_id(user_id)
        return [conversation.to_dict() for conversation in conversations]
    
    @staticmethod
    def update_conversation(conversation_id, query=None, response=None):
        """Update conversation"""
        conversation = Conversation.get_by_id(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        if query:
            conversation.query = query
        if response:
            conversation.response = response
        
        conversation.save()
        return conversation.to_dict()
    
    @staticmethod
    def delete_conversation(conversation_id):
        """Delete conversation"""
        success = Conversation.delete_by_id(conversation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"message": "Conversation deleted successfully"}
    
    @staticmethod
    def delete_user_conversations(user_id):
        """Delete all conversations for a specific user"""
        # Check if user exists
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        success = Conversation.delete_by_user_id(user_id)
        return {"message": f"All conversations for user {user_id} deleted successfully"}
    
    @staticmethod
    def get_conversations_by_email(email):
        """Get all conversations by user email"""
        # Get user by email
        user = User.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        conversations = Conversation.get_by_user_id(user.id)
        return {
            "user_email": email,
            "user_id": user.id,
            "total_conversations": len(conversations),
            "conversations": [conversation.to_dict() for conversation in conversations]
        }
    
    @staticmethod
    def delete_conversations_by_email(email):
        """Delete all conversations by user email"""
        # Get user by email
        user = User.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        success = Conversation.delete_by_user_id(user.id)
        return {"message": f"All conversations for user {email} deleted successfully"}
