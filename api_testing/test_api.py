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

if __name__ == "__main__":
    main()