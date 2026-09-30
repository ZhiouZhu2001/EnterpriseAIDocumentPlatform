from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, URL
from app.core.config import get_settings

settings = get_settings()
url = URL.create(
    "postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password.get_secret_value(),
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(url, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass