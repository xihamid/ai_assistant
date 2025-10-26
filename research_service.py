from research_agent import ResearchAgent
from user_model import User
from conversation_model import Conversation
from fastapi import HTTPException

class ResearchService:
    def __init__(self):
        self.agent = ResearchAgent()
    
    def process_research_query(self, user_id, query):
        """Process a research query for a specific user"""
        try:
            # Get user preferences
            user = User.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Get user preferences
            user_preferences = user.get_preferences_dict()
            
            # Process the query with the research agent
            response = self.agent.research_query(query, user_preferences)
            
            # Save the conversation to database
            conversation = Conversation(
                user_id=user_id,
                query=query,
                response=response
            )
            conversation.save()
            
            return {
                "user_id": user_id,
                "query": query,
                "response": response,
                "conversation_id": conversation.id,
                "user_preferences": user_preferences
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Research service error: {str(e)}")
    
    def get_user_research_history(self, user_id):
        """Get research history for a user"""
        try:
            # Check if user exists
            user = User.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Get conversations
            conversations = Conversation.get_by_user_id(user_id)
            
            return {
                "user_id": user_id,
                "user_name": user.name,
                "total_queries": len(conversations),
                "conversations": [conv.to_dict() for conv in conversations]
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting research history: {str(e)}")
    
    def search_without_save(self, query, max_results=3):
        """Simple search without saving to database"""
        try:
            results = self.agent.simple_search(query, max_results)
            return {
                "query": query,
                "results": results,
                "total_results": len(results) if isinstance(results, list) else 0
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
