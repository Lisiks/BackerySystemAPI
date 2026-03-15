from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Response, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import settings
from src.database.orm_models import UsersORM
from src.login_api.dto_models import (RegisterUserRequestDTO, RegisterUserResponseDTO, AuthenticateUserRequestDTO,
                                      AuthenticateUserResponseDTO)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пароль не должен быть длиннее 72 байт",
        )
    return pwd_context.hash(password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    if len(plain_password.encode("utf-8")) > 72:
        return False
    return pwd_context.verify(plain_password, password_hash)

def create_access_token(user_id: int, email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),
        "email": email,
        "type": "access",
        "exp": expire,
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(user_id: int, email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {
        "sub": str(user_id),
        "email": email,
        "type": "refresh",
        "exp": expire,
    }
    return jwt.encode(
        payload,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def register_user(
    data: RegisterUserRequestDTO,
    response: Response,
    session: Session,
) -> RegisterUserResponseDTO:
    existing_user_by_email = session.scalar(
        select(UsersORM).where(UsersORM.email == data.email)
    )
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже существует",
        )

    existing_user_by_username = session.scalar(
        select(UsersORM).where(UsersORM.username == data.username)
    )
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким логином уже существует",
        )

    user = UsersORM(
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password),
        is_active=True,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    access_token = create_access_token(user.id, user.email)
    refresh_token = create_refresh_token(user.id, user.email)

    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )

    return RegisterUserResponseDTO(
        access_token=access_token,
        token_type="bearer",
    )

def authenticate_user(
    data: AuthenticateUserRequestDTO,
    response: Response,
    session: Session,
) -> AuthenticateUserResponseDTO:
    user = session.scalar(
        select(UsersORM).where(UsersORM.username == data.username)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь деактивирован",
        )

    access_token = create_access_token(user.id, user.email)
    refresh_token = create_refresh_token(user.id, user.email)

    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )

    return AuthenticateUserResponseDTO(
        access_token=access_token,
        token_type="bearer",
    )