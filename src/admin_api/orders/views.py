from src.database.database import session_fabric
from src.database.orm_models import *
from src.admin_api.orders.dto_models import OrderStatusChangeModel
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.errors import NoRecordError


def get_all_orders_to_employee(employee_id: int):
    with (session_fabric() as session):
        current_employee = session.get(Employee, employee_id)
        if not current_employee: raise NoRecordError(f"No employee with id={employee_id}")

        query = select(
            OrdersORM
        ).options(
            selectinload(OrdersORM.products).selectinload(OrderItemsORM.product),
            selectinload(OrdersORM.branch),
            selectinload(OrdersORM.order_status)
        ).where(
            OrdersORM.branch_id == current_employee.branches_id
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