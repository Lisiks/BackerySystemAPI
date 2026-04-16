from src.database.database import session_fabric
from src.database.orm_models import *
from src.admin_api.orders.dto_models import UserOrderAdminDTO, OrderItemAdminDTO, OrderStatusChangeModel
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session
from src.errors import NoRecordError


def get_all_orders_to_employee(employee_id: int):
    with (session_fabric() as session):
        current_employee = session.get(EmployeesORM, employee_id)
        if not current_employee: raise NoRecordError(f"No employee with id={employee_id}")

        query = select(
            OrdersORM
        ).options(
            selectinload(OrdersORM.products).selectinload(OrderItemsORM.product),
            selectinload(OrdersORM.branch),
            selectinload(OrdersORM.order_status)
        ).where(
            OrdersORM.branch_id == current_employee.branch_id
        ).order_by(OrdersORM.created_at.desc())
        raw_result = session.execute(query).scalars().all()

        result = list()
        for order in raw_result:
            new_order_json = dict()
            new_order_json['id'] = order.id
            new_order_json['user_id'] = order.user_id
            new_order_json['phone'] = order.phone
            new_order_json['created_at'] = order.created_at.strftime("%Y-%m-%d %H:%M:%S")
            new_order_json['order_datetime'] = order.order_datetime.strftime("%Y-%m-%d %H:%M:%S")
            new_order_json['order_comment'] = order.comment
            new_order_json['branch_name'] = order.branch.branches_name
            new_order_json['branch_address'] = order.branch.branches_address
            new_order_json['status_id'] = order.status_id
            new_order_json['status_name'] = order.order_status.status_name
            new_order_json['total_ammount'] = order.total_amount

            order_product_json = list()
            for order_product in order.products:
                new_product_record = dict()
                new_product_record['id'] = order_product.product.id
                new_product_record['name'] = order_product.product.name
                new_product_record['quantity'] = order_product.quantity
                new_product_record['total_price'] = order_product.total_price
                order_product_json.append(new_product_record)
            new_order_json['product_list'] = order_product_json
            result.append(new_order_json)
        return result


def change_order_status(change_order_data: OrderStatusChangeModel):
    with session_fabric() as session:
        order = session.get(OrdersORM, change_order_data.order_id)
        if not order:
            raise NoRecordError(f"No order with id={change_order_data.order_id}")
        order.status_id = change_order_data.status_id
        session.commit()


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
