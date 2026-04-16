from fastapi import HTTPException, status

import bcrypt

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.admin_api.employees.dto_models import (EmployeeDTO, EmployeeAddDTO, EmployeeUpdateDTO,
                                                AuthenticateEmployeeRequestDTO, AuthenticateEmployeeResponseDTO, 
                                                )
from src.database.orm_models import EmployeesORM, BranchesORM
from src.errors import NoRecordError


def hash_employee_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пароль не должен быть длиннее 72 байт",
        )
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_employee_password(plain_password: str, password_hash: str) -> bool:
    if len(plain_password.encode("utf-8")) > 72:
        return False
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        password_hash.encode('utf-8') if isinstance(password_hash, str) else password_hash
    )


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
            detail="Неверный логин или пароль!!!!!!!!",
        )

    if not verify_employee_password(data.password, employee.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    return AuthenticateEmployeeResponseDTO(
        message="Успешная авторизация",
        employee_id=employee.id
    )


def get_all_employees(session: Session):
    orm_result = session.execute(
        select(EmployeesORM).order_by(EmployeesORM.id.asc())
    ).scalars().all()

    result = []

    for employee in orm_result:
        branch = session.get(BranchesORM, employee.branch_id)
        if branch is None:
            raise NoRecordError(f"No branch with id={employee.branch_id}")

        result.append(
            EmployeeDTO(
                id=employee.id,
                full_name=employee.full_name,
                phone=employee.phone,
                position=employee.position,
                username=employee.username,
                branch_id=employee.branch_id,
                work_address=str(branch.branches_address),
            ).model_dump(mode="json")
        )

    return result


def get_employee(employee_id: int, session: Session):
    employee = session.get(EmployeesORM, employee_id)
    if employee is None:
        raise NoRecordError(f"No employee with id={employee_id}")

    branch = session.get(BranchesORM, employee.branch_id)
    if branch is None:
        raise NoRecordError(f"No branch with id={employee.branch_id}")

    employee_id_value = getattr(employee, "id")
    branch_id_value = getattr(employee, "branch_id")

    return EmployeeDTO(
        id=employee_id_value,
        full_name=str(employee.full_name),
        phone=str(employee.phone),
        position=str(employee.position),
        username=str(employee.username),
        branch_id=branch_id_value,
        work_address=str(branch.branches_address),
    ).model_dump(mode="json")

def create_employee(new_employee: EmployeeAddDTO, session: Session):
    new_employee_orm = EmployeesORM(
        full_name=new_employee.full_name,
        phone=new_employee.phone,
        position=new_employee.position,
        username=new_employee.username,
        password_hash=hash_employee_password(new_employee.password),
        branch_id=new_employee.branch_id,
    )

    session.add(new_employee_orm)
    session.commit()


def update_employee(employee_id: int, current_employee: EmployeeUpdateDTO, session: Session):
    employee = session.get(EmployeesORM, employee_id)
    if employee is None:
        raise NoRecordError(f"No employee with id={employee_id}")

    employee.full_name = current_employee.full_name
    employee.phone = current_employee.phone
    employee.position = current_employee.position
    employee.username = current_employee.username
    #employee.password_hash=hash_employee_password(current_employee.password)
    employee.branch_id = current_employee.branch_id

    session.commit()


def delete_employee(employee_id: int, session: Session):
    employee = session.get(EmployeesORM, employee_id)
    if employee is None:
        raise NoRecordError(f"No employee with id={employee_id}")

    session.delete(employee)
    session.commit()