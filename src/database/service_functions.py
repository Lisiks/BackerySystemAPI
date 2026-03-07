from src.database.database import engine, Base


def refresh_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)