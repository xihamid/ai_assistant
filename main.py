from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from database import init_database
from user_controller import UserController
from conversation_controller import ConversationController
from research_controller import ResearchController
from auth import get_current_user
from user_model import User

# Pydantic models for request validation
class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    summary_length: str = "medium"
    preferred_topics: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class PreferencesRequest(BaseModel):
    summary_length: Optional[str] = None
    preferred_topics: Optional[str] = None

# Initialize database
init_database()

app = FastAPI(
    title="Personalized Research Assistant API", 
    version="1.0.0",
    description="AI-powered research assistant with personalized responses"
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Personalized Research Assistant API",
        "available_apis": [
            "POST /register/ - Register new user with preferences (NO AUTH REQUIRED)",
            "POST /login/ - Login user (returns JWT token) (NO AUTH REQUIRED)",
            "PUT /preferences/ - Update current user preferences (AUTH REQUIRED)",
            "GET /conversations/ - Get all conversations for current user (AUTH REQUIRED)",
            "DELETE /conversations/ - Delete all conversations for current user (AUTH REQUIRED)",
            "GET /research/query?query=your_question - Process research query with AI (AUTH REQUIRED, URL parameter)"
        ]
    }
    


# Essential APIs only
@app.post("/register/")
async def register_user(request: RegisterRequest):
    """Register a new user with structured preferences"""
    # Convert preferred_topics string to list if provided
    topics_list = None
    if request.preferred_topics:
        topics_list = [topic.strip() for topic in request.preferred_topics.split(",")]
    
    return UserController.register_user(request.email, request.password, request.full_name, request.summary_length, topics_list)

@app.post("/login/")
async def login_user(request: LoginRequest):
    """Login user"""
    return UserController.login_user(request.email, request.password)

@app.get("/conversations/")
async def get_my_conversations(current_user: User = Depends(get_current_user)):
    """Get all conversations for current logged-in user"""
    return ConversationController.get_conversations_by_user(current_user.id)

@app.delete("/conversations/")
async def delete_my_conversations(current_user: User = Depends(get_current_user)):
    """Delete all conversations for current logged-in user"""
    return ConversationController.delete_user_conversations(current_user.id)


@app.get("/research/query")
async def research_query_get(query: str, current_user: User = Depends(get_current_user)):
    """Process a research query with AI assistance (URL parameter)"""
    research_controller = ResearchController()
    return research_controller.process_query(current_user.id, query)


@app.put("/preferences/")
async def update_preferences(request: PreferencesRequest, current_user: User = Depends(get_current_user)):
    """Update current user preferences"""
    # Convert preferred_topics string to list if provided
    topics_list = None
    if request.preferred_topics:
        topics_list = [topic.strip() for topic in request.preferred_topics.split(",")]
    
    return UserController.update_user_preferences(current_user.id, request.summary_length, topics_list)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    print("Server is running on http://127.0.0.1:8000")