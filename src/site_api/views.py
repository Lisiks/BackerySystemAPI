from src.database.database import session_fabric
from src.database.orm_models import *
from src.site_api.dto_models import *
from datetime import datetime
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


def create_order(user_id: int, order_data: OrderAddDTO):
    with session_fabric() as session:
        branch = session.get(BranchesORM, {"id": order_data.branch_id})
        if branch is None:
            raise NoRecordError(f"Филиал с id={order_data.branch_id} не найден")

        if not branch.is_active_for_order:
            raise ValueError("Указанный филиал недоступен для оформления заказа")

        if len(order_data.items) == 0:
            raise ValueError("Список товаров заказа не должен быть пустым")

        product_ids = [item.product_id for item in order_data.items]

        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Список товаров заказа содержит повторяющиеся позиции")

        products = session.execute(
            select(ProductsORM).where(ProductsORM.id.in_(product_ids))
        ).scalars().all()

        products_map = {product.id: product for product in products}

        missing_ids = [product_id for product_id in product_ids if product_id not in products_map]
        if missing_ids:
            raise NoRecordError(
                f"Не найдены товары с id={', '.join(map(str, missing_ids))}"
            )

        unavailable_ids = [
            str(product.id) for product in products if not product.is_visible
        ]
        if unavailable_ids:
            raise ValueError(
                f"Недоступны для заказа товары с id={', '.join(unavailable_ids)}"
            )

        open_status = session.execute(
            select(OrderStatusesORM).where(OrderStatusesORM.status_name == "Открыт")
        ).scalar_one_or_none()

        if open_status is None:
            open_status = OrderStatusesORM(status_name="Открыт")
            session.add(open_status)
            session.flush()

        new_order = OrdersORM(
            user_id=user_id,
            phone=order_data.phone,
            created_at=datetime.now(),
            order_datetime=order_data.order_datetime,
            branch_id=order_data.branch_id,
            comment=order_data.comment,
            status_id=open_status.id,
            total_amount=0
        )

        session.add(new_order)
        session.flush()

        total_amount = 0

        for item in order_data.items:
            product = products_map[item.product_id]
            item_total_price = product.sale_price * item.quantity
            total_amount += item_total_price

            new_order_item = OrderItemsORM(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item.quantity,
                total_price=item_total_price
            )
            session.add(new_order_item)

        new_order.total_amount = total_amount

        session.commit()

        return {
            "message": "Заказ успешно создан",
            "order_id": new_order.id
        }
