from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.database import session_fabric
from src.database.orm_models import UsersORM
from src.login_api.dto_models import (RegisterUserRequestDTO, RegisterUserResponseDTO, AuthenticateUserRequestDTO,
                                      AuthenticateUserResponseDTO, RefreshAccessTokenResponseDTO)
from src.login_api.views import register_user, authenticate_user, refresh_access_token, validate_access_token


login_route = APIRouter(prefix="/login", tags=["Логин"])
security = HTTPBearer()

def get_db():
    session = session_fabric()
    try:
        yield session
    finally:
        session.close()

def verify_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_db),
) -> UsersORM:
    return validate_access_token(credentials.credentials, session)


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

@login_route.post(
    "/refresh",
    response_model=RefreshAccessTokenResponseDTO,
    status_code=200,
    summary="Обновление access токена",
)
def refresh_access_token_route(
    request: Request,
    session: Session = Depends(get_db),
):
    return refresh_access_token(request=request, session=session)