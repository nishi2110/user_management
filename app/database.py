import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base declarative class for models
Base = declarative_base()

class Database:
    """
    Handles database connections and sessions.
    Provides methods to initialize and retrieve session factories.
    """
    _engine = None
    _session_factory = None

    @classmethod
    def initialize(cls, database_url: str, echo: bool = False):
        """
        Initialize the async engine and sessionmaker.

        Args:
            database_url (str): The database connection URL.
            echo (bool): Whether to enable SQLAlchemy echo for debugging.
        """
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set or invalid.")

        if cls._engine is None:  # Ensure the engine is created only once
            cls._engine = create_async_engine(database_url, echo=echo, future=True)
            cls._session_factory = sessionmaker(
                bind=cls._engine, class_=AsyncSession, expire_on_commit=False, future=True
            )

    @classmethod
    def get_session_factory(cls):
        """
        Returns the session factory, ensuring it's initialized.

        Returns:
            sessionmaker: The configured session factory.

        Raises:
            ValueError: If the database has not been initialized.
        """
        if cls._session_factory is None:
            raise ValueError("Database not initialized. Call `initialize()` first.")
        return cls._session_factory

    @classmethod
    async def dispose_engine(cls):
        """
        Dispose the database engine, closing all connections.

        This is useful for shutting down the application gracefully.
        """
        if cls._engine:
            await cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None

# Dependency for FastAPI routes to get the database session
async def get_db():
    """
    Dependency to provide a database session for FastAPI routes.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session.
    """
    session_factory = Database.get_session_factory()
    async with session_factory() as session:
        yield session

# Initialize the database with environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set or invalid.")

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

Database.initialize(DATABASE_URL, echo=DEBUG_MODE)
