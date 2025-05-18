import os
os.environ["OPENROUTER_API_KEY"] = "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"
from agno.agent import Agent, RunResponse
from agno.models.openrouter import OpenRouter
from agno.tools.api import CustomApiTools
from agno.team.team import Team
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

researcher = Agent(
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

writer = Agent(
    model=OpenRouter(id="openai/gpt-4o-2024-11-20"),
    name="Writer",
    role="Writes a high-quality answer",
    description=(
        "You are a senior writer for the Movies Magazine. Given a topic you provide some concise but enlightning analysis."
        "your goal is to write a high-quality NYT-worthy article answering the question."
    ),
    instructions=[
        "Read all infos from the dvd movies resarch DB."
        "Then write a high-quality NYT-worthy article answering the query"
        "The article should be well-structured, informative, engaging and catchy.",
        "Remember: you are writing for the New York Times, so the quality of the article is important.",
    ],
    add_datetime_to_instructions=True,
)


planner = Team(
    name="Reasoning Movies analysis leader",
    mode="coordinate",
    model=OpenRouter(id="anthropic/claude-3.7-sonnet"),
    members=[researcher, writer],
    description="You are a senior Movie editor and database angineer. Given a query, your goal is to write a useful and onpoint answer .",
    instructions=[
        "First ask the movie researcher to search for the most relevant data for that query.",
        "Then ask the writer to get an engaging draft of the article.",
        "Edit, proofread, and refine the answer to ensure it meets the high standards of the New York Times.",
        "The answer should be extremely articulate and well written. "
        "Focus on clarity, coherence, and overall quality.",
        "Remember: you are the final gatekeeper before the answer is published, so make sure the answer is perfect.",
    ],
    add_datetime_to_instructions=True,
    # send_team_context_to_members=True,
    markdown=True,
    debug_mode=True,
    show_members_responses=True,
)





query = "“A common criticism of modern movies is that they are too long. Can you analyze film lengths over time and determine if that criticism is fair” "
planner.print_response(query)