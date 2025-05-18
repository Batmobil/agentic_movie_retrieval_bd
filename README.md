# Agentic Movie Retrieval System

An intelligent system for querying a DVD rental database using natural language.

## Components

- **FastAPI Backend**: REST API for interacting with the Pagila PostgreSQL database
- **LLM Agent**: Intelligent agent for translating natural language to database queries
- **Testing Suite**: Tools for verifying API functionality

## Setup

1. Install PostgreSQL and load the Pagila sample database
2. Set up Python environments using uv
3. Run the FastAPI server
4. Query the database using natural language

## Example Queries

- "What actors were in Chocolat Harry?"
- "Display the top 3 actors who have most appeared in films in the Children category"
- "Can you analyze film lengths over time and determine if modern movies are too long?"
- "Which customer has paid the most for rentals? What about least?"
