#!/usr/bin/env python3
"""
Agent Evaluation Script

This script evaluates the Agno agent's ability to handle various types of queries
related to the Pagila DVD rental database. It tests the agent with a variety of
query types and compares the agent's responses to expected endpoints and parameters.
"""

import sys
import json
from test_agno import agent
from agent import agent

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def evaluate_query(query, expected_endpoint, expected_params=None, description=None):
    """
    Evaluate a single query against the agent
    
    Args:
        query (str): The query to test
        expected_endpoint (str): The expected endpoint the agent should use
        expected_params (dict, optional): The expected parameters the agent should use
        description (str, optional): A description of what the query is testing
        
    Returns:
        bool: True if the agent's response matches the expected endpoint and parameters
    """
    print(f"\nQuery: \"{query}\"")
    if description:
        print(f"Testing: {description}")
    
    # Run the query through the agent
    response = agent.run(query)
    
    # Parse the agent's response
    try:
        # The agent should return a string that can be evaluated as Python code
        agent_code = response.content.strip()
        print(f"Agent response: {agent_code}")
        
        # Extract endpoint and params from the agent's response
        # Expected format: test_endpoint('endpoint', {'param1': 'value1'})
        if "test_endpoint(" in agent_code:
            # Parse the endpoint and params from the agent's code
            code_parts = agent_code.split("test_endpoint(")[1].split(")", 1)[0]
            
            # Extract endpoint
            if "'" in code_parts:
                agent_endpoint = code_parts.split("'")[1]
            elif '"' in code_parts:
                agent_endpoint = code_parts.split('"')[1]
            else:
                print("❌ Failed to parse endpoint from agent response")
                return False
            
            # Extract params if they exist
            agent_params = None
            if "{" in code_parts:
                params_str = code_parts.split("{")[1].split("}", 1)[0]
                # Convert the params string to a dict
                try:
                    # Add curly braces back and replace single quotes with double quotes for JSON parsing
                    params_json = "{" + params_str + "}"
                    params_json = params_json.replace("'", '"')
                    agent_params = json.loads(params_json)
                except json.JSONDecodeError:
                    print("❌ Failed to parse parameters from agent response")
                    return False
            
            # Compare with expected values
            endpoint_match = agent_endpoint == expected_endpoint
            params_match = True
            
            if expected_params is not None:
                if agent_params is None:
                    params_match = False
                else:
                    # Check if all expected params are in agent_params with correct values
                    for key, value in expected_params.items():
                        if key not in agent_params or agent_params[key] != value:
                            params_match = False
                            break
            
            # Print results
            if endpoint_match:
                print(f"✅ Endpoint: {agent_endpoint}")
            else:
                print(f"❌ Endpoint: {agent_endpoint} (expected: {expected_endpoint})")
            
            if params_match:
                print(f"✅ Parameters: {agent_params}")
            else:
                print(f"❌ Parameters: {agent_params} (expected: {expected_params})")
            
            return endpoint_match and params_match
        else:
            print("❌ Agent response does not contain test_endpoint call")
            return False
    except Exception as e:
        print(f"❌ Error evaluating agent response: {e}")
        return False

def run_evaluations():
    """Run all evaluation queries and return the results"""
    results = {
        "film_queries": 0,
        "actor_queries": 0,
        "category_queries": 0,
        "customer_queries": 0,
        "complex_queries": 0,
        "total": 0
    }
    
    total_queries = 0
    successful_queries = 0
    
    # Film-specific queries
    print_section("Film-specific Queries")
    
    # Query 1
    total_queries += 1
    if evaluate_query(
        "What are the 5 longest films in the database?",
        "films",
        {"limit": 5, "sort_by": "length", "sort_order": "desc"},
        "Testing film sorting by length"
    ):
        successful_queries += 1
        results["film_queries"] += 1
    
    # Query 2
    total_queries += 1
    if evaluate_query(
        "List all films with a rating of 'PG-13'",
        "films",
        {"rating": "PG-13"},
        "Testing film filtering by rating"
    ):
        successful_queries += 1
        results["film_queries"] += 1
    
    # Query 3
    total_queries += 1
    if evaluate_query(
        "Find films released in 2006 with a rental duration longer than 5 days",
        "films",
        {"release_year": 2006, "min_rental_duration": 5},
        "Testing film filtering by multiple criteria"
    ):
        successful_queries += 1
        results["film_queries"] += 1
    
    # Actor-specific queries
    print_section("Actor-specific Queries")
    
    # Query 4
    total_queries += 1
    if evaluate_query(
        "Which actor has appeared in the most Comedy films?",
        "search/top-actors-by-category",
        {"category_name": "Comedy", "limit": 1},
        "Testing finding top actor in a specific category"
    ):
        successful_queries += 1
        results["actor_queries"] += 1
    
    # Query 5
    total_queries += 1
    if evaluate_query(
        "Find all actors who have appeared in more than 30 films",
        "actors",
        {"min_film_count": 30},
        "Testing actor filtering by film count"
    ):
        successful_queries += 1
        results["actor_queries"] += 1
    
    # Query 6
    total_queries += 1
    if evaluate_query(
        "List actors who have appeared in both Action and Drama films",
        "search/actors-in-multiple-categories",
        {"categories": ["Action", "Drama"]},
        "Testing finding actors in multiple categories"
    ):
        successful_queries += 1
        results["actor_queries"] += 1
    
    # Category-based queries
    print_section("Category-based Queries")
    
    # Query 7
    total_queries += 1
    if evaluate_query(
        "What is the most popular film category based on rental count?",
        "analysis/category-popularity",
        {"sort_by": "rental_count", "limit": 1},
        "Testing category popularity analysis"
    ):
        successful_queries += 1
        results["category_queries"] += 1
    
    # Query 8
    total_queries += 1
    if evaluate_query(
        "Compare the average film length between Horror and Comedy categories",
        "analysis/category-comparison",
        {"categories": ["Horror", "Comedy"], "metric": "avg_length"},
        "Testing category comparison"
    ):
        successful_queries += 1
        results["category_queries"] += 1
    
    # Query 9
    total_queries += 1
    if evaluate_query(
        "Which category has the highest average rental rate?",
        "analysis/category-comparison",
        {"sort_by": "avg_rental_rate", "sort_order": "desc", "limit": 1},
        "Testing category sorting by rental rate"
    ):
        successful_queries += 1
        results["category_queries"] += 1
    
    # Customer analysis queries
    print_section("Customer Analysis Queries")
    
    # Query 10
    total_queries += 1
    if evaluate_query(
        "Who are the top 5 customers by rental frequency?",
        "analysis/customer-payments",
        {"sort_by": "rental_count", "limit": 5},
        "Testing customer sorting by rental frequency"
    ):
        successful_queries += 1
        results["customer_queries"] += 1
    
    # Query 11
    total_queries += 1
    if evaluate_query(
        "Find customers who have never returned a film",
        "customers",
        {"unreturned_rentals": True},
        "Testing customer filtering by rental status"
    ):
        successful_queries += 1
        results["customer_queries"] += 1
    
    # Query 12
    total_queries += 1
    if evaluate_query(
        "What's the average payment amount for customers in district 'Alberta'?",
        "analysis/customer-payments",
        {"district": "Alberta", "metric": "avg_payment"},
        "Testing customer payment analysis by district"
    ):
        successful_queries += 1
        results["customer_queries"] += 1
    
    # Complex analysis queries
    print_section("Complex Analysis Queries")
    
    # Query 13
    total_queries += 1
    if evaluate_query(
        "Which month had the highest rental activity in the database?",
        "analysis/rental-activity",
        {"group_by": "month", "sort_by": "count", "sort_order": "desc", "limit": 1},
        "Testing time-based rental analysis"
    ):
        successful_queries += 1
        results["complex_queries"] += 1
    
    # Query 14
    total_queries += 1
    if evaluate_query(
        "What's the correlation between film length and rental rate?",
        "analysis/film-correlation",
        {"metric1": "length", "metric2": "rental_rate"},
        "Testing correlation analysis"
    ):
        successful_queries += 1
        results["complex_queries"] += 1
    
    # Query 15
    total_queries += 1
    if evaluate_query(
        "Find films that have never been rented",
        "films",
        {"never_rented": True},
        "Testing film filtering by rental status"
    ):
        successful_queries += 1
        results["complex_queries"] += 1
    
    # Calculate success rate
    success_rate = (successful_queries / total_queries) * 100 if total_queries > 0 else 0
    results["total"] = successful_queries
    
    # Print summary
    print_section("Evaluation Summary")
    print(f"Total queries: {total_queries}")
    print(f"Successful queries: {successful_queries}")
    print(f"Success rate: {success_rate:.2f}%")
    print("\nResults by category:")
    print(f"- Film queries: {results['film_queries']}/3")
    print(f"- Actor queries: {results['actor_queries']}/3")
    print(f"- Category queries: {results['category_queries']}/3")
    print(f"- Customer queries: {results['customer_queries']}/3")
    print(f"- Complex queries: {results['complex_queries']}/3")
    
    return results

if __name__ == "__main__":
    print_section("Agent Evaluation")
    print("Evaluating agent's ability to handle various query types...")
    results = run_evaluations()
    
    # Exit with status code based on success rate
    if results["total"] == 15:
        print("\n🎉 All tests passed! The agent is working perfectly.")
        sys.exit(0)
    elif results["total"] >= 10:
        print("\n✅ Most tests passed. The agent is working well but could be improved.")
        sys.exit(0)
    else:
        print("\n❌ Too many tests failed. The agent needs significant improvement.")
        sys.exit(1)
