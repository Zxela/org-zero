# core/memory/postgres_client.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import get_settings

settings = get_settings()

DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
