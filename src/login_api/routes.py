from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.database.database import session_fabric
from src.login_api.dto_models import (RegisterUserRequestDTO, RegisterUserResponseDTO, AuthenticateUserRequestDTO,
                                      AuthenticateUserResponseDTO)
from src.login_api.views import register_user, authenticate_user


login_route = APIRouter(prefix="/login", tags=["Логин"])

def get_db():
    session = session_fabric()
    try:
        yield session
    finally:
        session.close()


@login_route.post("/register",
                  response_model=RegisterUserResponseDTO,
                  status_code=201,
                  summary="Регистрация пользователя")
def register_user_route(
    data: RegisterUserRequestDTO,
    response: Response,
    session: Session = Depends(get_db),
):
    return register_user(data=data, response=response, session=session)

@login_route.post(
    "/authenticate",
    response_model=AuthenticateUserResponseDTO,
    status_code=200,
    summary="Аутентификация пользователя"
)
def authenticate_user_route(
    data: AuthenticateUserRequestDTO,
    response: Response,
    session: Session = Depends(get_db),
):
    return authenticate_user(data=data, response=response, session=session)
