from src.database.database import session_fabric
from src.database.orm_models import *
from src.site_api.dto_models import *

from sqlalchemy import select
from sqlalchemy.orm import selectinload


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


def get_all_available_products_by_category():
    with session_fabric() as session:
        query = select(
            CategoriesORM
        ).options(
            selectinload(CategoriesORM.visible_category_products)
        ).where(
            CategoriesORM.display_on_site == True
        ).order_by(CategoriesORM.showing_number)

        orm_result = session.execute(query).scalars().all()
        result = {"categories": []}
        for orm_record in orm_result:
            result["categories"].append(
                {
                    "category_id": orm_record.id,
                    "products": [ProductsGetDTO.model_validate(product_record, from_attributes=True).dict()
                                 for product_record in orm_record.visible_category_products]
                })
        return result


def get_product_info_by_id(product_id):
    with session_fabric() as session:
        query = select(
            ProductsORM.id,
            ProductsORM.name,
            ProductsORM.weight,
            ProductsORM.sale_price,
            ProductsORM.image_url,
            ProductsORM.composition,
            ProductsORM.description,
            ProductsORM.calories,
            ProductsORM.protein,
            ProductsORM.fat,
            ProductsORM.carbs,
            CategoriesORM.category_name
        ).select_from(ProductsORM).join(
            CategoriesORM,
            CategoriesORM.id == ProductsORM.category_id
        ).where(ProductsORM.id == product_id)

        orm_result = session.execute(query).one()
        return ProductsFullInfoDTO.model_validate(orm_result, from_attributes=True).dict()




