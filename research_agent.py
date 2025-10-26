import os
from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate

class ResearchAgent:
    def __init__(self):
        # API Keys - Load from environment variables
        openai_key = os.getenv("OPENAI_API_KEY")
        tavily_key = os.getenv("TAVILY_API_KEY")
        
        # Initialize LLM
        try:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.1,
                api_key=openai_key
            )
            print("OpenAI LLM initialized successfully!")
        except Exception as e:
            print(f"Error initializing OpenAI: {e}")
            self.llm = None
        
        # Initialize search tool
        try:
            self.search_tool = TavilySearchResults(
                tavily_api_key=tavily_key,
                max_results=5
            )
            print("Tavily search tool initialized successfully!")
        except Exception as e:
            print(f"Error initializing Tavily: {e}")
            self.search_tool = None
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful research assistant. Your job is to:
1. Analyze the search results provided
2. Provide personalized responses based on user preferences
3. Always cite your sources

IMPORTANT RESPONSE LENGTH RULES:
- If user prefers "short": Provide ONLY 2-3 bullet points maximum, keep each point very brief
- If user prefers "medium": Provide 3-5 bullet points with some details
- If user prefers "long": Provide comprehensive information with sources

Always be accurate and helpful."""),
            ("human", "Query: {query}\nSearch Results: {search_results}\nUser Preferences: {preferences}")
        ])
    
    def research_query(self, query, user_preferences=None):
        """Process a research query with user preferences"""
        try:
            if not self.search_tool:
                return "Search functionality not available. Please configure Tavily API key."
            
            if not self.llm:
                return "AI processing not available. Please configure OpenAI API key."
            
            # Get user preferences for response formatting
            preferred_topics = []
            if user_preferences and isinstance(user_preferences, dict):
                preferred_topics = user_preferences.get("preferred_topics", [])
            
            # Search for information
            search_results = self.search_tool.invoke({"query": query})
            
            # Format search results
            formatted_results = ""
            if isinstance(search_results, list):
                for i, result in enumerate(search_results[:3], 1):
                    formatted_results += f"{i}. {result.get('title', 'No title')}\n"
                    formatted_results += f"   {result.get('content', 'No content')}\n"
                    formatted_results += f"   URL: {result.get('url', 'No URL')}\n\n"
            else:
                formatted_results = str(search_results)
            
            # Process user preferences
            preferences_text = "standard response"
            if user_preferences:
                if isinstance(user_preferences, dict):
                    summary_length = user_preferences.get("summary_length", "medium")
                    preferred_topics = user_preferences.get("preferred_topics", [])
                    
                    if summary_length == "short":
                        preferences_text = "CRITICAL: Provide ONLY 2-3 bullet points maximum. Keep each point very brief and concise. No long explanations."
                    elif summary_length == "long":
                        preferences_text = "Provide a detailed response with comprehensive information and sources"
                    else:  # medium
                        preferences_text = "Provide 3-5 bullet points with some details"
                    
                    if preferred_topics:
                        preferences_text += f". Focus on topics: {', '.join(preferred_topics)}"
                else:
                    preferences_text = str(user_preferences)
            
            # Create the prompt
            chain = self.prompt | self.llm
            
            # Generate response
            response = chain.invoke({
                "query": query,
                "search_results": formatted_results,
                "preferences": preferences_text
            })
            
            return response.content
        
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def simple_search(self, query, max_results=3):
        """Simple search without agent for basic queries"""
        try:
            if not self.search_tool:
                return "Search functionality not available. Please configure Tavily API key."
            
            results = self.search_tool.invoke({"query": query})
            return results
        except Exception as e:
            return f"Search error: {str(e)}"