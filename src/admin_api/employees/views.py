from sqlalchemy import select
from sqlalchemy.orm import Session

from src.admin_api.employees.dto_models import EmployeeDTO
from src.database.orm_models import EmployeesORM


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