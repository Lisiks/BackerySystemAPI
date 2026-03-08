from src.database.database import session_fabric
from src.database.orm_models import *
from src.site_api.dto_models import *
from sqlalchemy import select


def get_branches_info():
    with session_fabric() as session:
        query = select(
            BranchesORM.id,
            BranchesORM.branches_address,
            BranchesORM.branches_phone
        ).select_from(BranchesORM)

        orm_result = session.execute(query).all()
        return [BranchesGetDTO.model_validate(orm_record, from_attributes=True)
                .dict() for orm_record in orm_result]


def get_categories_info():
    with session_fabric() as session:
        query = select(
            CategoriesORM.id,
            CategoriesORM.category_name,
            CategoriesORM.showing_number
        ).select_from(
            CategoriesORM
        ).where(
             CategoriesORM.display_on_site == True
        ).order_by(CategoriesORM.showing_number)

        orm_result = session.execute(query).all()
        return [CategoriesGetDTO.model_validate(orm_record, from_attributes=True)
                .dict() for orm_record in orm_result]