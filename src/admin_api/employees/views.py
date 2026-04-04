from sqlalchemy import select
from sqlalchemy.orm import Session

from src.admin_api.employees.dto_models import EmployeeDTO, EmployeeAddDTO
from src.database.orm_models import EmployeesORM
from src.errors import NoRecordError


def get_all_employees(session: Session):
    orm_result = session.execute(
        select(EmployeesORM).order_by(EmployeesORM.id.asc())
    ).scalars().all()

    return [
        EmployeeDTO(
            id=int(employee.id),
            full_name=str(employee.full_name),
            phone=str(employee.phone),
            birth_date=employee.birth_date,
            position=str(employee.position),
            work_address=str(employee.work_address),
        ).model_dump(mode="json")
        for employee in orm_result
    ]


def get_employee(employee_id: int, session: Session):
    employee = session.get(EmployeesORM, employee_id)
    if employee is None:
        raise NoRecordError(f"No employee with id={employee_id}")

    return EmployeeDTO.model_validate(employee, from_attributes=True).model_dump(mode="json")


def create_employee(new_employee: EmployeeAddDTO, session: Session):
    new_employee_orm = EmployeesORM(
        full_name=new_employee.full_name,
        phone=new_employee.phone,
        birth_date=new_employee.birth_date,
        position=new_employee.position,
        work_address=new_employee.work_address,
    )

    session.add(new_employee_orm)
    session.commit()


def update_employee(current_employee: EmployeeDTO, session: Session):
    employee = session.get(EmployeesORM, current_employee.id)
    if employee is None:
        raise NoRecordError(f"No employee with id={current_employee.id}")

    employee.full_name = current_employee.full_name
    employee.phone = current_employee.phone
    employee.birth_date = current_employee.birth_date
    employee.position = current_employee.position
    employee.work_address = current_employee.work_address

    session.commit()


def delete_employee(employee_id: int, session: Session):
    employee = session.get(EmployeesORM, employee_id)
    if employee is None:
        raise NoRecordError(f"No employee with id={employee_id}")

    session.delete(employee)
    session.commit()