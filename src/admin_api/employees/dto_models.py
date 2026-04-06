from datetime import date

from pydantic import BaseModel, Field


class EmployeeAddAndUpdateDTO(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=30)
    birth_date: date
    position: str = Field(min_length=1, max_length=100)
    work_address: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=1, max_length=72)
    branch_id: int = Field(gt=0)


class EmployeeDTO(BaseModel):
    id: int = Field(gt=0)
    full_name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=30)
    birth_date: date
    position: str = Field(min_length=1, max_length=100)
    work_address: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=3, max_length=100)
    branch_id: int = Field(gt=0)


class AuthenticateEmployeeRequestDTO(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=1, max_length=72)


class AuthenticateEmployeeResponseDTO(BaseModel):
    message: str
    employee_id: int = Field(gt=0)
    branch_id: int = Field(gt=0)