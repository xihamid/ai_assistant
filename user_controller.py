from fastapi import HTTPException
from user_model import User
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

class UserController:
    
    @staticmethod
    def register_user(email, password, full_name, summary_length="medium", preferred_topics=None):
        """Register a new user with structured preferences"""
        try:
            if not email:
                raise HTTPException(status_code=400, detail="Email is required")
            
            if not password:
                raise HTTPException(status_code=400, detail="Password is required")
            
            if not full_name:
                raise HTTPException(status_code=400, detail="Full name is required")
            
            # Validate summary_length
            if summary_length not in ["short", "medium", "long"]:
                raise HTTPException(status_code=400, detail="Summary length must be 'short', 'medium', or 'long'")
            
            # Check if user already exists
            existing_user = User.get_by_email(email)
            if existing_user:
                raise HTTPException(status_code=400, detail="User with this email already exists")
            
            # Create preferences dictionary
            preferences_dict = {
                "summary_length": summary_length,
                "preferred_topics": preferred_topics or []
            }
            
            user = User(email=email, password=password, full_name=full_name)
            user.set_preferences_dict(preferences_dict)
            user.save()
            return user.to_dict()
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
    
    @staticmethod
    def login_user(email, password):
        """Login user"""
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        if not password:
            raise HTTPException(status_code=400, detail="Password is required")
        
        # Get user by email
        user = User.get_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not user.verify_password(password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.to_dict()
        }
    
    @staticmethod
    def update_user_preferences(user_id, summary_length=None, preferred_topics=None):
        """Update user preferences"""
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get current preferences
        current_prefs = user.get_preferences_dict()
        
        # Update preferences if provided
        if summary_length is not None:
            if summary_length not in ["short", "medium", "long"]:
                raise HTTPException(status_code=400, detail="Summary length must be 'short', 'medium', or 'long'")
            current_prefs["summary_length"] = summary_length
        
        if preferred_topics is not None:
            current_prefs["preferred_topics"] = preferred_topics
        
        # Save updated preferences
        user.set_preferences_dict(current_prefs)
        user.save()
        
        return user.to_dict()
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        users = User.get_all()
        return [user.to_dict() for user in users]
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.to_dict()
    
    @staticmethod
    def update_user(user_id, name=None, preferences=None):
        """Update user"""
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if name:
            user.name = name
        if preferences is not None:
            user.preferences = preferences
        
        user.save()
        return user.to_dict()
    
    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        success = User.delete_by_id(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    
    @staticmethod
    def search_users(name_query):
        """Search users by name"""
        users = User.get_all()
        matching_users = []
        
        for user in users:
            if name_query.lower() in user.name.lower():
                matching_users.append(user.to_dict())
        
        return {
            "users": matching_users,
            "query": name_query,
            "total_found": len(matching_users)
        }
