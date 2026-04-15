from .database import SessionLocal

def get_db():
    """
    FastAPI dependency that provides a database session.
    
    Creates a new SQLAlchemy session for each request and ensures it is properly
    closed after the request completes. This is used with FastAPI's Depends() to
    inject database sessions into route handlers.
    
    Yields:
        Session: SQLAlchemy database session object.
    
    Note:
        This is a generator function that follows FastAPI's dependency injection pattern.
        The database connection is automatically closed in the finally block,
        even if an exception occurs during request processing.
    
    Example:
        @app.get("/jobs")
        def list_jobs(db: Session = Depends(get_db)):
            return crud.get_jobs(db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()