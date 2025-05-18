from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)