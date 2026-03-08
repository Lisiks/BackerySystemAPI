from src.database.database import session_fabric
from src.database.orm_models import CategoriesORM
from src.admin_api.categories.dto_models import CategoriesAddDTO, CategoriesDTO
from src.errors import NoRecordError

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


def get_all_categories():
    with session_fabric() as session:
        query = select(CategoriesORM).select_from(CategoriesORM)
        orm_result = session.execute(query).scalars().all()
        return [CategoriesDTO.model_validate(orm_record, from_attributes=True).dict()
                for orm_record in orm_result]


def create_category(new_category: CategoriesAddDTO):
    with session_fabric() as session:
        new_category_orm = CategoriesORM(
            category_name=new_category.category_name,
            category_description=new_category.category_description,
            showing_number=new_category.showing_number,
            display_on_site=new_category.display_on_site
        )
        session.add(new_category_orm)
        session.commit()


def update_category(current_category: CategoriesDTO):
    with session_fabric() as session:

        current_category_orm = session.get(CategoriesORM, {"id": current_category.id})
        if current_category_orm is None:
            raise NoRecordError(f"No record with id={current_category.id}")
        current_category_orm.category_name = current_category.category_name
        current_category_orm.category_description = current_category.category_description
        current_category_orm.showing_number = current_category.showing_number
        current_category_orm.display_on_site = current_category.display_on_site
        session.commit()
