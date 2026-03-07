from src.database.database import engine, Base
from src.database.orm_models import *


def refresh_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)