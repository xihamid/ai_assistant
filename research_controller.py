from fastapi import HTTPException
from research_service import ResearchService
from user_model import User

class ResearchController:
    
    def __init__(self):
        self.research_service = ResearchService()
    
    def process_query(self, user_id, query):
        """Process a research query for a user"""
        if not query or not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        return self.research_service.process_research_query(user_id, query)
    
    def get_research_history(self, user_id):
        """Get research history for a user"""
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        return self.research_service.get_user_research_history(user_id)
    
    def quick_search(self, query, max_results=3):
        """Quick search without user context"""
        if not query or not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        return self.research_service.search_without_save(query, max_results)
    
    def quick_search_with_user(self, user_id, query, max_results=3):
        """Quick search with user context and history tracking"""
        if not query or not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        return self.research_service.process_research_query(user_id, query)
    
    def update_user_preferences(self, user_id, preferences):
        """Update user research preferences"""
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.preferences = preferences
        user.save()
        
        return {
            "message": "User preferences updated successfully",
            "user_id": user_id,
            "preferences": preferences
        }
