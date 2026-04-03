from sqlalchemy import select
from sqlalchemy.orm import Session

from src.admin_api.orders.dto_models import UserOrderAdminDTO, OrderItemAdminDTO
from src.database.orm_models import (
    UsersORM,
    OrdersORM,
    OrderItemsORM,
    ProductsORM,
    BranchesORM,
    OrderStatusesORM,
)
from src.errors import NoRecordError


def get_user_orders(user_id: int, session: Session):
    user = session.get(UsersORM, user_id)
    if user is None:
        raise NoRecordError(f"No user with id={user_id}")

    orders = session.execute(
        select(OrdersORM)
        .where(OrdersORM.user_id == user_id)
        .order_by(OrdersORM.created_at.desc(), OrdersORM.id.desc())
    ).scalars().all()

    result = []

    for order in orders:
        branch = session.get(BranchesORM, order.branch_id)
        status = session.get(OrderStatusesORM, order.status_id)

        order_items_rows = session.execute(
            select(OrderItemsORM, ProductsORM)
            .join(ProductsORM, ProductsORM.id == OrderItemsORM.product_id)
            .where(OrderItemsORM.order_id == order.id)
        ).all()

        items = [
            OrderItemAdminDTO(
                product_id=int(product.id),
                product_name=str(product.name),
                quantity=int(order_item.quantity),
                total_price=float(order_item.total_price),
            )
            for order_item, product in order_items_rows
        ]

        order_dto = UserOrderAdminDTO(
            id=int(order.id),
            user_id=int(order.user_id),
            username=str(user.username),
            phone=str(order.phone),
            created_at=order.created_at,
            order_datetime=order.order_datetime,
            branch_id=int(order.branch_id),
            branch_name=str(branch.branches_name) if branch else "",
            branch_address=str(branch.branches_address) if branch else "",
            status_id=int(order.status_id),
            status_name=str(status.status_name) if status else "",
            comment=str(order.comment) if order.comment is not None else None,
            total_amount=float(order.total_amount),
            items=items,
        )

        result.append(order_dto.model_dump(mode="json"))

    return result