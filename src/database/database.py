from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import settings

engine = create_engine(
    url=settings.database_link,
    echo=False,
    max_overflow=10,
    pool_size=30,
    pool_pre_ping=True,
    pool_recycle=3600
)

session_fabric = sessionmaker(
    bind=engine,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


