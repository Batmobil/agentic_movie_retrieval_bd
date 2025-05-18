import os
os.environ["OPENROUTER_API_KEY"] = "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"
from agno.agent import Agent, RunResponse
from agno.models.openrouter import OpenRouter
from agno.tools.api import CustomApiTools

import json
from pprint import pprint

# Base URL of your API
BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

# Create the API toolkit
api_toolkit = CustomApiTools(
    base_url=BASE_URL,
    verify_ssl=True,
    timeout=30
)

agent = Agent(
    model=OpenRouter(id="openai/gpt-4o-2024-11-20"),
    tools=[
        api_toolkit,  # Add the API toolkit for making API calls to our FastAPI server
    ],
    description="You are a movie database and data engineer assistant that queries the Pagila DVD rental database",
    instructions=[
        "You have access to a movie database API through the make_request tool.",
        "Use this tool to query the API and provide informative responses to user queries.",
        "Format responses in a clear, structured way.",
        
        "Available endpoints:",
        "- GET /health - Health check",
        "- GET /actors - List actors (params: skip, limit)",
        "- GET /films - List films (params: skip, limit)",
        "- GET /search/actors-in-film - Find actors in a film (params: film_title)",
        "- GET /search/top-actors-by-category - Find top actors in a category (params: category_name)",
        "- GET /analysis/film-length-by-year - Film length analysis by year",
        "- GET /analysis/customer-payments - Customer payment analysis",
        "- GET /database/schema - Database schema information",
        "- GET /database/schema-diagram - Database schema diagram",
        "- POST /execute-query - Custom SQL query (params: query, params)",
        
        "Query type detection:",
        "- When asked about actors in a film, use the /search/actors-in-film endpoint with film_title parameter",
        "- When asked about films, use the /films endpoint",
        "- When asked about actors, use the /actors endpoint",
        "- When asked about top actors in a category, use the /search/top-actors-by-category endpoint with category_name parameter",
        "- When asked about film length or duration analysis, use the /analysis/film-length-by-year endpoint",
        "- When asked about customer payments or spending, use the /analysis/customer-payments endpoint",
        "- When asked about database structure or schema, use the /database/schema endpoint",
        "- When asked about database diagram or visualization, use the /database/schema-diagram endpoint",
        "- When asked to run a custom SQL query, use the /execute-query endpoint with POST method",
        
        "How to use the make_request tool:",
        "1. Determine the appropriate endpoint based on the user's query",
        "2. Call the make_request tool with the endpoint, method, and any required parameters",
        "3. Parse the JSON response and provide a clear, informative answer to the user",
        
        "Example workflow:",
        "1. User asks: 'Find actors in CHOCOLAT'",
        "2. You determine this requires the /search/actors-in-film endpoint",
        "3. You call make_request with endpoint='search/actors-in-film', method='GET', params={'film_title': 'CHOCOLAT'}",
        "   IMPORTANT: Always pass query parameters in the 'params' dictionary, not as direct arguments",
        "   CORRECT: make_request(endpoint='search/actors-in-film', method='GET', params={'film_title': 'CHOCOLAT'})",
        "   INCORRECT: make_request(endpoint='search/actors-in-film', method='GET', film_title='CHOCOLAT')",
        "4. You receive a JSON response with actor information",
        "5. You format and present this information to the user in a clear, structured way",
        
        "Always process the API response to provide a clear, informative answer. Don't just return raw JSON data.",
        "If the API request fails, explain the issue to the user and suggest alternatives if possible."
    ],
    markdown=True,
    show_tool_calls=True  # Show tool calls in the agent's response for debugging
)

# Example queries
print_section("Example Query 1: What actors were in Chocolat Harry?")
agent.print_response("What actors were in Chocolat Harry?")

print_section("Example Query 2: Top actors in Children category")
agent.print_response("Display the top 3 actors who have most appeared in films in the Children category")
