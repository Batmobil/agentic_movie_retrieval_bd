#!/usr/bin/env python3
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
    """Test a GET API endpoint and return the response"""
    url = f"{BASE_URL}/{endpoint}"
    print(f"Making GET request to: {url}")
    
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

def test_post_endpoint(endpoint, data):
    """Test a POST API endpoint and return the response"""
    url = f"{BASE_URL}/{endpoint}"
    print(f"Making POST request to: {url}")
    
    try:
        response = requests.post(url, json=data)
        
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

def main():
    # Test 1: Health check
    print_section("Health Check")
    health = test_endpoint("health")
    if health:
        pprint(health)

    # Test 2: List actors
    print_section("List Actors (First 5)")
    actors = test_endpoint("actors", {"limit": 5})
    if actors:
        for actor in actors:
            print(f"Actor {actor['actor_id']}: {actor['first_name']} {actor['last_name']}")

    # Test 3: List films
    print_section("List Films (First 5)")
    films = test_endpoint("films", {"limit": 5})
    if films:
        for film in films:
            print(f"Film {film['film_id']}: {film['title']} ({film['release_year']}) - {film['length']} minutes")

    # Test 4: Search actors in a film
    print_section("Find Actors in 'CHOCOLAT'")
    actors_in_film = test_endpoint("search/actors-in-film", {"film_title": "CHOCOLAT"})
    if actors_in_film:
        if len(actors_in_film) == 0:
            print("No actors found for this film.")
        else:
            print(f"Found {len(actors_in_film)} actors in this film:")
            for actor in actors_in_film:
                print(f"  • {actor['first_name']} {actor['last_name']}")
    
    # Test 5: Top actors in Children category
    print_section("Top 3 Actors in Children Category")
    top_actors = test_endpoint("search/top-actors-by-category", {"category_name": "Children"})
    if top_actors:
        print("Top actors in Children films:")
        for i, actor in enumerate(top_actors, 1):
            print(f"{i}. {actor['first_name']} {actor['last_name']} - {actor['film_count']} films")
    
    # Test 6: Film length analysis
    print_section("Film Length Analysis")
    length_data = test_endpoint("analysis/film-length-by-year")
    if length_data:
        print("Film length trends over time:")
        for year_data in length_data:
            print(f"{year_data['year']}: Avg {year_data['avg_length']:.1f} min, {year_data['film_count']} films")
        
        # Simple analysis
        if len(length_data) > 1:
            earliest = length_data[0]
            latest = length_data[-1]
            change = latest['avg_length'] - earliest['avg_length']
            print(f"\nAnalysis: From {earliest['year']} to {latest['year']}, average film length")
            if change > 0:
                print(f"increased by {change:.1f} minutes (from {earliest['avg_length']:.1f} to {latest['avg_length']:.1f})")
            elif change < 0:
                print(f"decreased by {abs(change):.1f} minutes (from {earliest['avg_length']:.1f} to {latest['avg_length']:.1f})")
            else:
                print(f"remained the same at {earliest['avg_length']:.1f} minutes")
    
    # Test 7: Customer payment analysis
    print_section("Customer Payment Analysis")
    payment_data = test_endpoint("analysis/customer-payments")
    if payment_data:
        print("Top paying customers:")
        for i, cust in enumerate(payment_data['top_customers'], 1):
            print(f"{i}. {cust['first_name']} {cust['last_name']} - ${cust['total_paid']:.2f} ({cust['payment_count']} payments)")
        
        print("\nLowest paying customers:")
        for i, cust in enumerate(payment_data['bottom_customers'], 1):
            print(f"{i}. {cust['first_name']} {cust['last_name']} - ${cust['total_paid']:.2f} ({cust['payment_count']} payments)")
    
    # Test 8: Database schema
    print_section("Database Schema")
    schema = test_endpoint("database/schema")
    if schema:
        print(f"Found {len(schema)} tables in the database:")
        # Print a few key tables as examples
        important_tables = ['actor', 'film', 'category', 'customer', 'payment']
        for table_name in important_tables:
            if table_name in schema:
                table_info = schema[table_name]
                print(f"\n- {table_name}:")
                print(f"  Columns: {len(table_info['columns'])}")
                print(f"  Primary keys: {', '.join(table_info['primary_keys'])}")
                if table_info['foreign_keys']:
                    print("  Foreign keys:")
                    for fk in table_info['foreign_keys']:
                        print(f"    {fk['column']} → {fk['references']['table']}.{fk['references']['column']}")
        print("\n(Showing only a subset of tables. Full schema available via API)")
    
    # Test 9: Schema diagram
    print_section("Database Schema Diagram")
    diagram = test_endpoint("database/schema-diagram")
    if diagram:
        print("Mermaid.js ER Diagram generated successfully.")
        print("First few lines of the diagram:")
        diagram_lines = diagram['diagram'].split('\n')
        for line in diagram_lines[:5]:
            print(line)
        print("...")
    
    # Test 10: Custom SQL query
    print_section("Custom SQL Query")
    query = {
        "query": "SELECT c.name as category, COUNT(f.film_id) as film_count FROM category c JOIN film_category fc ON c.category_id = fc.category_id JOIN film f ON fc.film_id = f.film_id GROUP BY c.name ORDER BY film_count DESC LIMIT 5",
        "params": {}
    }
    result = test_post_endpoint("execute-query", query)
    if result:
        print("Top 5 film categories by count:")
        for row in result["results"]:
            print(f"  {row['category']}: {row['film_count']} films")

if __name__ == "__main__":
    main()
