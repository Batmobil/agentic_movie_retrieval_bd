from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union

# Database connection - Update with your password
DATABASE_URL = "postgresql://postgres:postgres@localhost/pagila"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(title="Pagila DVD Rental API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/")
def read_root():
    return {"message": "Pagila DVD Rental API"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/actors")
def get_actors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = text("SELECT actor_id, first_name, last_name FROM actor ORDER BY actor_id LIMIT :limit OFFSET :skip")
    result = db.execute(query, {"skip": skip, "limit": limit})
    actors = [{"actor_id": row[0], "first_name": row[1], "last_name": row[2]} for row in result]
    return actors

@app.get("/films")
def get_films(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = text("""
        SELECT film_id, title, description, release_year, length, rating 
        FROM film ORDER BY film_id LIMIT :limit OFFSET :skip
    """)
    result = db.execute(query, {"skip": skip, "limit": limit})
    films = [
        {
            "film_id": row[0], 
            "title": row[1], 
            "description": row[2],
            "release_year": row[3],
            "length": row[4],
            "rating": row[5]
        } 
        for row in result
    ]
    return films

@app.get("/search/actors-in-film")
def actors_in_film(film_title: str, db: Session = Depends(get_db)):
    """Example endpoint to answer 'What actors were in Chocolat Harry?'"""
    query = text("""
        SELECT a.actor_id, a.first_name, a.last_name
        FROM actor a
        JOIN film_actor fa ON a.actor_id = fa.actor_id
        JOIN film f ON fa.film_id = f.film_id
        WHERE LOWER(f.title) LIKE LOWER(:title)
    """)
    result = db.execute(query, {"title": f"%{film_title}%"})
    actors = [{"actor_id": row[0], "first_name": row[1], "last_name": row[2]} for row in result]
    return actors

@app.get("/search/top-actors-by-category")
def top_actors_by_category(category_name: str, limit: int = 3, db: Session = Depends(get_db)):
    """
    Get top actors who have appeared in the most films of a specific category.
    Example: 'Display the top 3 actors who have most appeared in films in the Children category'
    """
    query = text("""
        SELECT a.actor_id, a.first_name, a.last_name, COUNT(fa.film_id) as film_count
        FROM actor a
        JOIN film_actor fa ON a.actor_id = fa.actor_id
        JOIN film f ON fa.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE LOWER(c.name) = LOWER(:category_name)
        GROUP BY a.actor_id, a.first_name, a.last_name
        ORDER BY film_count DESC
        LIMIT :limit
    """)
    result = db.execute(query, {"category_name": category_name, "limit": limit})
    actors = [
        {
            "actor_id": row[0], 
            "first_name": row[1], 
            "last_name": row[2],
            "film_count": row[3]
        } 
        for row in result
    ]
    return actors

@app.get("/analysis/film-length-by-year")
def film_length_by_year(db: Session = Depends(get_db)):
    """
    Analyze film lengths over time.
    Example: 'Can you analyze film lengths over time and determine if that criticism is fair'
    """
    query = text("""
        SELECT release_year, 
               AVG(length) as avg_length,
               MIN(length) as min_length,
               MAX(length) as max_length,
               COUNT(*) as film_count
        FROM film
        GROUP BY release_year
        ORDER BY release_year
    """)
    result = db.execute(query)
    data = [
        {
            "year": row[0],
            "avg_length": float(row[1]),
            "min_length": row[2],
            "max_length": row[3],
            "film_count": row[4]
        }
        for row in result
    ]
    return data

@app.get("/analysis/customer-payments")
def customer_payments(top_count: int = 5, db: Session = Depends(get_db)):
    """
    Analyze customer payment data to find highest and lowest paying customers.
    Example: 'Which customer has paid the most for rentals? What about least?'
    """
    query = text("""
        SELECT c.customer_id, c.first_name, c.last_name, 
               SUM(p.amount) as total_paid,
               COUNT(p.payment_id) as payment_count
        FROM customer c
        JOIN payment p ON c.customer_id = p.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_paid DESC
    """)
    result = db.execute(query)
    all_customers = [
        {
            "customer_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "total_paid": float(row[3]),
            "payment_count": row[4]
        }
        for row in result
    ]
    
    # Return top and bottom customers
    return {
        "top_customers": all_customers[:top_count],
        "bottom_customers": all_customers[-top_count:][::-1]  # Reverse to get lowest first
    }

class SQLQuery(BaseModel):
    query: str
    params: Optional[Dict[str, Any]] = {}

@app.post("/execute-query")
def execute_query(query_data: SQLQuery, db: Session = Depends(get_db)):
    """
    Execute a custom SQL query.
    WARNING: In a production environment, you would need to implement
    security measures to prevent SQL injection and restrict queries.
    """
    try:
        result = db.execute(text(query_data.query), query_data.params)
        
        # Convert result to list of dictionaries
        columns = result.keys()
        rows = []
        for row in result:
            rows.append({col: val for col, val in zip(columns, row)})
        
        return {"results": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")

@app.get("/database/schema")
def get_database_schema(db: Session = Depends(get_db)):
    """
    Get database schema information including tables, columns, and relationships.
    """
    
    # Get tables
    tables_query = text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables_result = db.execute(tables_query)
    tables = [row[0] for row in tables_result]
    
    schema = {}
    
    # Get columns for each table
    for table in tables:
        columns_query = text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = :table_name
            ORDER BY ordinal_position
        """)
        columns_result = db.execute(columns_query, {"table_name": table})
        columns = [
            {
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == 'YES'
            }
            for row in columns_result
        ]
        
        # Get primary keys
        pk_query = text("""
            SELECT c.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name)
            JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
                AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
            WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_name = :table_name
        """)
        pk_result = db.execute(pk_query, {"table_name": table})
        primary_keys = [row[0] for row in pk_result]
        
        # Get foreign keys
        fk_query = text("""
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = :table_name
        """)
        fk_result = db.execute(fk_query, {"table_name": table})
        foreign_keys = [
            {
                "column": row[0],
                "references": {
                    "table": row[1],
                    "column": row[2]
                }
            }
            for row in fk_result
        ]
        
        schema[table] = {
            "columns": columns,
            "primary_keys": primary_keys,
            "foreign_keys": foreign_keys
        }
    
    return schema

@app.get("/database/schema-diagram")
def get_schema_diagram(db: Session = Depends(get_db)):
    """
    Get a Mermaid.js diagram of the database schema.
    """
    
    # Get tables and their foreign keys
    fk_query = text("""
        SELECT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
          AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
          AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
    """)
    fk_result = db.execute(fk_query)
    relationships = [
        {
            "table": row[0],
            "column": row[1],
            "foreign_table": row[2],
            "foreign_column": row[3]
        }
        for row in fk_result
    ]
    
    # Generate Mermaid diagram
    mermaid = ["erDiagram"]
    
    # Add relationships
    for rel in relationships:
        mermaid.append(f'    {rel["table"]} ||--o{{ {rel["foreign_table"]} : "{rel["column"]}"')
    
    return {"diagram": "\n".join(mermaid)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
