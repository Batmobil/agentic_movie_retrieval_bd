import os
os.environ["OPENROUTER_API_KEY"] = "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"
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.agent import Agent, RunResponse


import requests
import json
from pprint import pprint

# Base URL of your API
BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

def test_endpoint(endpoint, params=None):
    """Test an API endpoint and return the response"""
    url = f"{BASE_URL}/{endpoint}"
    print(f"Making request to: {url}")
    
    try:
        if params:
            response = requests.get(url, params=params)
        else:
            response = requests.get(url)
        
        if response.status_code == 200:
            print(f"Status: ✅ {response.status_code} OK")
            return response.json()
        else:
            print(f"Status: ❌ {response.status_code} ERROR")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

agent = Agent(
    model=OpenRouter(id="openai/gpt-4o-2024-11-20"),
    # tools=[
    #     ReasoningTools(add_instructions=True),  # Add reasoning capabilities
    #     # CustomApiTools(base_url=API_BASE_URL),  # For making API calls to our FastAPI server
    # ],
    description="You are a movie database and data engineer assistant that queries the Pagila DVD rental database",
    instructions=[
        "From the examples and information below, provide the arguments string for the test_endpoint function to be able to answer the user query",
        "Format responses in a clear, structured way",
        "Available endpoints:",
        "- GET /actors - List actors (params: skip, limit)",
        "- GET /films - List films (params: skip, limit)",
        "- GET /search/actors-in-film - Find actors in a film (params: film_title)",
        "When asked about actors in a film, use the /search/actors-in-film endpoint",
        "When asked about films, use the /films endpoint",
        "When asked about actors, use the /actors endpoint",
        "examples:",
        "user_query = 'Find Actors in 'CHOCOLAT'",
        "test_endpoint('search/actors-in-film', {'film_title': 'CHOCOLAT'})",
        "Only ouput the python code string with no additional character, do not enclose your answer in ```python prefix ```suffix"

    ],
    markdown=False
)

# Print the response in the terminal
agent.print_response("What actors were in Chocolat Harry?")
query = "What actors were in Chocolat Harry?"
resp =agent.run(query)

print(eval(resp.content))