from pydantic import BaseModel, Field


class EmployeeAddDTO(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=30)
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=1, max_length=72)
    branch_id: int = Field(gt=0)
    position_id: int = Field(gt=0)

class EmployeeUpdateDTO(BaseModel):
    #id: int = Field(gt=0)
    full_name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=30)
    position: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=100)
    branch_id: int = Field(gt=0)

class EmployeeDTO(BaseModel):
    id: int = Field(gt=0)
    full_name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=30)
    username: str = Field(min_length=3, max_length=100)
    branch_id: int = Field(gt=0)
    position_id: int = Field(gt=0)
    position_name: str = Field(min_length=1, max_length=100)
    work_address: str = Field(min_length=1, max_length=200)


class PositionDTO(BaseModel):
    id: int = Field(gt=0)
    position_name: str = Field(min_length=1, max_length=100)


class AuthenticateEmployeeRequestDTO(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=1, max_length=72)


class AuthenticateEmployeeResponseDTO(BaseModel):
    message: str
    employee_id: int = Field(gt=0)