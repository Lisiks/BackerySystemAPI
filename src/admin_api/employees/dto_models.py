from datetime import date

from pydantic import BaseModel, Field


class EmployeeAddDTO(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=30)
    birth_date: date
    position: str = Field(min_length=1, max_length=100)
    work_address: str = Field(min_length=1, max_length=255)


class EmployeeDTO(EmployeeAddDTO):
    id: int = Field(gt=0)