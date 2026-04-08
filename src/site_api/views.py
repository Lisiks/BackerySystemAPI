from src.database.database import session_fabric
from src.database.orm_models import *
from src.site_api.dto_models import *




from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, joinedload

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session
from src.errors import *


OPEN_ORDER_STATUS_ID = 1


def get_branches_info():
    with session_fabric() as session:
        query = select(
            BranchesORM.id,
            BranchesORM.branches_address,
            BranchesORM.branches_phone
        ).select_from(BranchesORM).where(BranchesORM.is_active_for_order == True)

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
        query = query = select(
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
            CategoriesORM.category_name  #
        ).select_from(ProductsORM).join(ProductsORM.category).where(
            and_(
                ProductsORM.id == product_id,
                ProductsORM.is_visible == True,
                CategoriesORM.display_on_site == True
            )
        )


        orm_result = session.execute(query).all()
        return ProductsFullInfoDTO.model_validate(orm_result[0], from_attributes=True).dict() if len(orm_result) == 1 else None



def create_order(user_id: int, order_data: OrderAddDTO, session: Session):
        branch = session.get(BranchesORM, {"id": order_data.branch_id})
        if branch is None:
            raise NoBranchError()

        if not branch.is_active_for_order:
            raise UnavaliableBranch()

        product_ids = [item.product_id for item in order_data.items]

        products = session.execute(
            select(ProductsORM).where(ProductsORM.id.in_(product_ids))
        ).scalars().all()

        products_map = {product.id: product for product in products}

        unvaliable_products = [product_id for product_id in product_ids if product_id not in products_map]
        unvaliable_products.extend([product.id for product in products if not product.is_visible or not product.category.display_on_site])

        if unvaliable_products:
            raise UnavaliableProducts(unvaliable_products)

        new_order = OrdersORM(
            user_id=user_id,
            username=order_data.username,
            phone=order_data.phone,
            created_at=datetime.now(),
            order_datetime=order_data.order_datetime,
            branch_id=order_data.branch_id,
            comment=order_data.comment,
            status_id=OPEN_ORDER_STATUS_ID,
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


