from src import app
import uvicorn

from src.database.database import Base, engine
from src.database.orm_models import *

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    uvicorn.run("main:app", reload=True)


