# 🤖 Personalized Research Assistant

A simple AI-powered research assistant that helps users get personalized answers to their questions using web search and AI.

## 📋 Table of Contents
- [What is this project?](#what-is-this-project)
- [How it works?](#how-it-works)
- [File Structure](#file-structure)
- [Database Design](#database-design)
- [API Endpoints](#api-endpoints)
- [How to run?](#how-to-run)
- [How to use?](#how-to-use)

## 🎯 What is this project?

This is a **Personalized Research Assistant** that:
- Creates users with their preferences
- Takes questions from users
- Searches the web for answers
- Uses AI to give personalized responses
- Saves all conversations in a database

**Example:**
- User asks: "What is AI?"
- System searches the web
- AI gives a personalized answer based on user preferences
- Everything is saved for later

## 🔄 How it works?

```
User → FastAPI → LangChain → Web Search → AI Processing → Database
```

1. **User** asks a question
2. **FastAPI** receives the request
3. **LangChain** searches the web using Tavily
4. **OpenAI** processes the results
5. **Database** saves the conversation

## 📁 File Structure

### Main Files

#### `main.py` - The Main Application
**Purpose:** This is the main file that starts the web server and defines all the API routes.

**What it does:**
- Starts the FastAPI server
- Defines 5 API endpoints
- Connects everything together

**Key imports:**
```python
from fastapi import FastAPI  # Web framework
from database import init_database  # Database setup
from user_controller import UserController  # User management
from conversation_controller import ConversationController  # Chat history
from research_controller import ResearchController  # AI research
```

#### `database.py` - Database Connection
**Purpose:** Manages the SQLite database connection and creates tables.

**What it does:**
- Connects to SQLite database
- Creates users and conversations tables
- Provides database connection functions

**Key functions:**
```python
def get_db_connection()  # Get database connection
def init_database()  # Create tables
def close_db_connection()  # Close connection
```

#### `user_model.py` - User Data Model
**Purpose:** Defines how user data is stored and retrieved from database.

**What it does:**
- Creates User objects
- Saves users to database
- Gets users from database
- Updates user information

**Key functions:**
```python
def save()  # Save user to database
def get_all()  # Get all users
def get_by_id()  # Get user by ID
def get_by_name()  # Get user by name
```

#### `user_controller.py` - User Business Logic
**Purpose:** Contains the business logic for user operations.

**What it does:**
- Validates user data
- Handles user creation
- Manages user operations
- Returns proper responses

**Key functions:**
```python
def create_user()  # Create new user
def get_all_users()  # Get all users
def get_user_by_id()  # Get specific user
```

#### `conversation_model.py` - Chat History Model
**Purpose:** Manages conversation data (questions and answers).

**What it does:**
- Stores chat conversations
- Links conversations to users
- Tracks timestamps
- Manages conversation history

**Key functions:**
```python
def save()  # Save conversation
def get_all()  # Get all conversations
def get_by_user_id()  # Get user's conversations
def delete_by_id()  # Delete conversation
```

#### `conversation_controller.py` - Chat History Logic
**Purpose:** Handles conversation business logic.

**What it does:**
- Validates conversation data
- Manages conversation operations
- Handles errors
- Returns conversation data

**Key functions:**
```python
def create_conversation()  # Create new conversation
def get_conversation_by_id()  # Get specific conversation
def delete_conversation()  # Delete conversation
```

#### `research_agent.py` - AI Research Engine
**Purpose:** The brain of the system - handles AI and web search.

**What it does:**
- Connects to OpenAI API
- Connects to Tavily search API
- Searches the web
- Processes results with AI
- Returns personalized answers

**Key functions:**
```python
def research_query()  # Main research function
def simple_search()  # Basic search
```

**API Keys needed:**
```python
openai_key = "sk-your-openai-key"  # OpenAI API key
tavily_key = "tvly-your-tavily-key"  # Tavily search key
```

#### `research_service.py` - Research Business Logic
**Purpose:** Connects research agent with database and user management.

**What it does:**
- Gets user preferences
- Calls research agent
- Saves results to database
- Returns formatted responses

**Key functions:**
```python
def process_research_query()  # Main research processing
def get_user_research_history()  # Get user's research history
```

#### `research_controller.py` - Research API Logic
**Purpose:** Handles research API requests and responses.

**What it does:**
- Validates research requests
- Calls research service
- Handles errors
- Returns API responses

**Key functions:**
```python
def process_query()  # Process research query
def get_research_history()  # Get research history
```

## 🗄️ Database Design

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    preferences TEXT
)
```

**Fields:**
- `id` - Unique user ID (auto-generated)
- `name` - User's name
- `preferences` - User's preferences (like "short summaries")

### Conversations Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

**Fields:**
- `id` - Unique conversation ID
- `user_id` - Which user asked the question
- `query` - The question asked
- `response` - The AI's answer
- `timestamp` - When it happened

## 🌐 API Endpoints

### 1. Create User
```
POST /users/
```
**Purpose:** Create a new user with preferences

**Example:**
```json
{
  "name": "Ahmed",
  "preferences": "short summaries"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Ahmed",
  "preferences": "short summaries"
}
```

### 2. Get Conversation by ID
```
GET /conversations/{conversation_id}
```
**Purpose:** Get a specific conversation

**Example:**
```
GET /conversations/1
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "query": "What is AI?",
  "response": "AI is artificial intelligence...",
  "timestamp": "2025-10-25 12:00:00"
}
```

### 3. Delete Conversation
```
DELETE /conversations/{conversation_id}
```
**Purpose:** Delete a specific conversation

**Example:**
```
DELETE /conversations/1
```

**Response:**
```json
{
  "message": "Conversation deleted successfully"
}
```

### 4. Process Research Query
```
POST /research/query
```
**Purpose:** Ask a question and get AI-powered answer

**Example:**
```json
{
  "user_id": 1,
  "query": "What is machine learning?"
}
```

**Response:**
```json
{
  "user_id": 1,
  "query": "What is machine learning?",
  "response": "Machine learning is a subset of AI...",
  "conversation_id": 2,
  "user_preferences": "short summaries"
}
```

### 5. Get Research History
```
GET /research/history/{user_id}
```
**Purpose:** Get all conversations for a user

**Example:**
```
GET /research/history/1
```

**Response:**
```json
{
  "user_id": 1,
  "user_name": "Ahmed",
  "total_queries": 5,
  "conversations": [
    {
      "id": 1,
      "query": "What is AI?",
      "response": "AI is...",
      "timestamp": "2025-10-25 12:00:00"
    }
  ]
}
```

## 🚀 How to run?

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Add API Keys
Edit `research_agent.py` and add your API keys:
```python
openai_key = "sk-your-actual-openai-key"
tavily_key = "tvly-your-actual-tavily-key"
```

### Step 3: Start Server
```bash
python main.py
```

### Step 4: Test API
Visit: http://127.0.0.1:8000/docs

## 📱 How to use?

### 1. Create a User
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ahmed", "preferences": "short summaries"}'
```

### 2. Ask a Question
```bash
curl -X POST "http://127.0.0.1:8000/research/query" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "query": "What is artificial intelligence?"}'
```

### 3. Check History
```bash
curl -X GET "http://127.0.0.1:8000/research/history/1"
```

## 🔧 User Preferences Examples

- `"short summaries"` - Get 3-5 bullet points
- `"detailed responses with references"` - Get comprehensive info with sources
- `"technical details"` - Get technical explanations
- `"simple explanations"` - Get easy-to-understand responses

## 📊 Data Flow

1. **User** creates account with preferences
2. **User** asks a question via API
3. **System** searches web using Tavily
4. **AI** processes results based on user preferences
5. **Database** saves the conversation
6. **User** can view history anytime

## 🛠️ Technologies Used

- **FastAPI** - Web framework
- **SQLite** - Database
- **LangChain** - AI orchestration
- **OpenAI** - Language model
- **Tavily** - Web search
- **Python** - Programming language

## 📝 Notes for Developers

- All files use simple Python classes
- No complex frameworks or patterns
- Easy to understand and modify
- Database is automatically created
- API keys are in the code (not environment variables)
- Everything is in one folder

## 🎯 Summary

This is a simple research assistant that:
- Takes user questions
- Searches the web
- Uses AI to give personalized answers
- Saves everything in a database
- Provides 5 simple API endpoints

Perfect for learning how to build AI-powered applications! 🚀
