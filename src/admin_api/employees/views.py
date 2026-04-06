from fastapi import HTTPException, status

from passlib.context import CryptContext

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.admin_api.employees.dto_models import (EmployeeDTO, EmployeeAddAndUpdateDTO,
                                                AuthenticateEmployeeRequestDTO, AuthenticateEmployeeResponseDTO)
from src.database.orm_models import EmployeesORM
from src.errors import NoRecordError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_employee_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пароль не должен быть длиннее 72 байт",
        )
    return pwd_context.hash(password)


def verify_employee_password(plain_password: str, password_hash: str) -> bool:
    if len(plain_password.encode("utf-8")) > 72:
        return False
    return pwd_context.verify(plain_password, password_hash)


def authenticate_employee(
    data: AuthenticateEmployeeRequestDTO,
    session: Session,
) -> AuthenticateEmployeeResponseDTO:
    employee = session.scalar(
        select(EmployeesORM).where(EmployeesORM.username == data.username)
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    if not verify_employee_password(data.password, employee.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    return AuthenticateEmployeeResponseDTO(
        message="Успешная авторизация",
        employee_id=employee.id,
        branch_id=employee.branch_id,
    )


def get_all_employees(session: Session):
    orm_result = session.execute(
        select(EmployeesORM).order_by(EmployeesORM.id.asc())
    ).scalars().all()

    return [
        EmployeeDTO.model_validate(employee, from_attributes=True).model_dump(mode="json")
        for employee in orm_result
    ]


def get_employee(employee_id: int, session: Session):
    employee = session.get(EmployeesORM, employee_id)
    if employee is None:
        raise NoRecordError(f"No employee with id={employee_id}")

    return EmployeeDTO.model_validate(employee, from_attributes=True).model_dump(mode="json")


def create_employee(new_employee: EmployeeAddAndUpdateDTO, session: Session):
    new_employee_orm = EmployeesORM(
        full_name=new_employee.full_name,
        phone=new_employee.phone,
        birth_date=new_employee.birth_date,
        position=new_employee.position,
        work_address=new_employee.work_address,
        username=new_employee.username,
        password_hash=hash_employee_password(new_employee.password),
        branch_id=new_employee.branch_id,
    )

    session.add(new_employee_orm)
    session.commit()


def update_employee(employee_id: int, current_employee: EmployeeAddAndUpdateDTO, session: Session):
    employee = session.get(EmployeesORM, employee_id)
    if employee is None:
        raise NoRecordError(f"No employee with id={employee_id}")

    employee.full_name = current_employee.full_name
    employee.phone = current_employee.phone
    employee.birth_date = current_employee.birth_date
    employee.position = current_employee.position
    employee.work_address = current_employee.work_address
    employee.username = current_employee.username
    employee.branch_id = current_employee.branch_id

    session.commit()


def delete_employee(employee_id: int, session: Session):
    employee = session.get(EmployeesORM, employee_id)
    if employee is None:
        raise NoRecordError(f"No employee with id={employee_id}")

    session.delete(employee)
    session.commit()