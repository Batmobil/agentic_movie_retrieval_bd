# Agentic Movies Retrieval System

## Overview

Navigating databases dynamically has historically been challenging. However, with AI agents and tools, being able to dynamically retrieve data to answer user queries is now more accessible than ever. This project demonstrates how to build an intelligent data retrieval and analysis system that can answer analytical questions about movie data stored in a PostgreSQL database.

## Problem Statement

Traditional database querying requires technical knowledge of SQL and database schemas. This creates a barrier for non-technical users who want to extract insights from data. This project aims to bridge that gap by allowing users to ask questions in natural language and receive accurate, well-formatted answers.

## Solution Architecture

The system consists of three main components:

1. **FastAPI Backend** (`pagila-api/`): A REST API that provides endpoints to query the Pagila PostgreSQL database, including:
   - Basic data retrieval (actors, films)
   - Specialized searches (actors in films, top actors by category)
   - Complex analysis (film length trends, customer payment analysis)
   - Database schema information
   - Custom SQL query execution

2. **AI Agent System** (`base_agent/`): Intelligent agents built with the Agno framework that:
   - Translate natural language queries into API calls
   - Process and format API responses
   - Generate human-readable answers

3. **Team-Based Architecture**: For complex analytical questions, the system employs a team of specialized agents:
   - **Researcher**: Queries the database and retrieves relevant data
   - **Writer**: Crafts engaging, informative responses based on the data
   - **Planner**: Coordinates between agents to produce comprehensive answers

## Example Queries

The system can handle a variety of analytical questions, such as:

1. **Simple Lookups**: "What actors were in Chocolat Harry?"
2. **Ranking Queries**: "Display the top 3 actors who have most appeared in films in the Children category"
3. **Trend Analysis**: "A common criticism of modern movies is that they are too long. Can you analyze film lengths over time and determine if that criticism is fair"
4. **Comparative Analysis**: "Which customer has paid the most for rentals? What about least?"

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database with the Pagila sample dataset installed
- OpenRouter API key (for accessing LLM models)

### Installation

1. **Set up the PostgreSQL database**:
   - Install PostgreSQL
   - Load the Pagila sample dataset
   - Update the database connection string in `pagila-api/main.py`

2. **Install dependencies**:
   ```bash
   # For the API
   cd pagila-api
   pip install -r requirements.txt
   
   # For the agent system
   cd base_agent
   pip install -r requirements.txt
   ```

3. **Configure API key**:
   - Set your OpenRouter API key in `base_agent/agent.py` and `base_agent/agents_team.py`

### Running the System

1. **Start the FastAPI server**:
   ```bash
   cd pagila-api
   uvicorn main:app --reload
   ```

2. **Run the agent**:
   ```bash
   cd base_agent
   python agent.py
   ```

3. **For complex analytical queries, use the team-based approach**:
   ```bash
   cd base_agent
   python agents_team.py
   ```

## Technical Details

### API Endpoints

- `/health`: Health check
- `/actors`: List actors
- `/films`: List films
- `/search/actors-in-film`: Find actors in a film
- `/search/top-actors-by-category`: Find top actors in a category
- `/analysis/film-length-by-year`: Film length analysis by year
- `/analysis/customer-payments`: Customer payment analysis
- `/database/schema`: Database schema information
- `/database/schema-diagram`: Database schema diagram
- `/execute-query`: Custom SQL query execution

### Agent Architecture

The system uses a combination of:
- **Natural Language Understanding**: To interpret user queries
- **Query Planning**: To determine the appropriate API endpoints to call
- **Response Generation**: To format data into human-readable answers

For complex queries, the team-based approach divides responsibilities between specialized agents, allowing for more sophisticated analysis and better-quality responses.

## Future Enhancements

- Web interface for easier interaction
- better agents evaluation 
- Support for more complex analytical questions
- Integration with additional data sources
- Improved visualization capabilities
- Fine-tuning of language models for better domain understanding

## License

This project is open source and available under the MIT License.
