from sqlmodel import Session, create_engine
from app.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create all tables in the database"""
    from sqlmodel import SQLModel
    from app.models.user import User  # Import models to register them
    
    SQLModel.metadata.create_all(engine)
