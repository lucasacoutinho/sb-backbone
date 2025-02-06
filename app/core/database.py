from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
)

# Create a new async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL logs in the console (useful in development)
    future=True,  # Enables SQLAlchemy 2.0-style usage
)

# Create a session factory bound to our engine
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)


async def get_db():
    """
    Dependency that provides a new database session per request
    and ensures it's closed on completion.
    """
    async with AsyncSessionLocal() as session:
        yield session
