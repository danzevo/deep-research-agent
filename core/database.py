from sqlmodel import SQLModel, create_engine, Session
from core.config import settings

# Create the engine that talks to the SQLite database
engine = create_engine(settings.database_url, echo=False)

def create_db_and_tables():
    # This creates the tables if they don't exist
    SQLModel.metadata.create_all(engine)

def get_session():
    # Provides a database session to our functions
    with Session(engine) as session:
        yield session

        