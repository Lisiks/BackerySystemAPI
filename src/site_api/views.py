from src.database.database import session_fabric
from src.database.orm_models import *
from src.site_api.dto_models import *

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.errors import NoRecordError



def get_branches_info():
    with session_fabric() as session:
        query = select(
            BranchesORM.id,
            BranchesORM.branches_address,
            BranchesORM.branches_phone
        ).select_from(BranchesORM)

        orm_result = session.execute(query).all()
        return [BranchesGetDTO.model_validate(orm_record, from_attributes=True)
                .model_dump() for orm_record in orm_result]


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
                .model_dump() for orm_record in orm_result]


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
        result = dict()
        for orm_record in orm_result:
            result[orm_record.id] = dict()
            for product_record in orm_record.visible_category_products:
                dto_record = ProductsGetDTO.model_validate(product_record, from_attributes=True)
                result[orm_record.id][dto_record.id] = {
                    "name": dto_record.name,
                    "sale_price": dto_record.sale_price,
                    "weight": dto_record.weight,
                    "image_irl": dto_record.image_url
                }
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
        return ProductsFullInfoDTO.model_validate(orm_result, from_attributes=True).model_dump()

def add_product_to_favorites(user_id: int, product_id: int):
    with session_fabric() as session:
        product = session.get(ProductsORM, {"id": product_id})
        if product is None:
            raise NoRecordError(f"Товар с id={product_id} не найден")

        favorite_query = select(FavoriteProductsORM).where(
            FavoriteProductsORM.user_id == user_id,
            FavoriteProductsORM.product_id == product_id
        )
        favorite = session.execute(favorite_query).scalar_one_or_none()

        if favorite is not None:
            raise ValueError("Товар уже добавлен в избранное")

        new_favorite = FavoriteProductsORM(
            user_id=user_id,
            product_id=product_id
        )

        session.add(new_favorite)
        session.commit()



def delete_product_from_favorites(user_id: int, product_id: int):
    with session_fabric() as session:
        favorite_query = select(FavoriteProductsORM).where(
            FavoriteProductsORM.user_id == user_id,
            FavoriteProductsORM.product_id == product_id
        )
        favorite = session.execute(favorite_query).scalar_one_or_none()

        if favorite is None:
            raise NoRecordError(
                f"Товар с id={product_id} отсутствует в избранном у пользователя"
            )

        session.delete(favorite)
        session.commit()


