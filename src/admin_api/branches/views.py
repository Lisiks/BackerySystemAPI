from src.database.database import session_fabric
from src.database.orm_models import BranchesORM
from src.admin_api.branches.dto_models import BranchesDTO, BranchesAddDTO
from src.errors import NoRecordError

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError



def get_all_branches():
    with session_fabric() as session:
        query = select(BranchesORM).select_from(BranchesORM)
        orm_result = session.execute(query).scalars().all()
        return [BranchesDTO.model_validate(orm_record, from_attributes=True).dict()
                for orm_record in orm_result]


def create_branch(new_branch: BranchesAddDTO):
    with session_fabric() as session:
        try:
            new_branch_orm = BranchesORM(
                branches_name=new_branch.branches_name,
                branches_address=new_branch.branches_address,
                branches_phone=new_branch.branches_phone,
                is_active_for_order=new_branch.is_active_for_order
            )
            session.add(new_branch_orm)
            session.commit()
            return "ok"
        except IntegrityError as e:
            return "Integrity error"


def update_branch(current_branch: BranchesDTO):
    with session_fabric() as session:
        try:
            current_branch_orm = session.get(BranchesORM, {"id": current_branch.id})
            if current_branch_orm is None:
                raise NoRecordError
            current_branch_orm.branches_name = current_branch.branches_name
            current_branch_orm.branches_address = current_branch.branches_address
            current_branch_orm.branches_phone = current_branch.branches_phone
            current_branch_orm.is_active_for_order = current_branch.is_active_for_order
            session.commit()
            return "ok"
        except IntegrityError as e:
            return "Integrity error"
        except NoRecordError as e:
            return "No record with id"
