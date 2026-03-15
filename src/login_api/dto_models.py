from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequestDTO(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)


class RegisterUserResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"

