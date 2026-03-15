from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.database.database import session_fabric
from src.login_api.dto_models import RegisterUserRequestDTO, RegisterUserResponseDTO
from src.login_api.views import register_user

login_route = APIRouter(prefix="/login")

def get_db():
    session = session_fabric()
    try:
        yield session
    finally:
        session.close()


@login_route.post("/register", response_model=RegisterUserResponseDTO, status_code=201)
def register_user_route(
    data: RegisterUserRequestDTO,
    response: Response,
    session: Session = Depends(get_db),
):
    return register_user(data=data, response=response, session=session)
