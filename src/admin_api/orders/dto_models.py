from datetime import datetime
from pydantic import BaseModel, Field


class OrderItemAdminDTO(BaseModel):
    product_id: int = Field(gt=0)
    product_name: str = Field(min_length=1, max_length=200)
    quantity: int = Field(gt=0)
    total_price: float = Field(ge=0)


class UserOrderAdminDTO(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    username: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=1, max_length=30)

    created_at: datetime
    order_datetime: datetime

    branch_id: int = Field(gt=0)
    branch_name: str = Field(min_length=1, max_length=100)
    branch_address: str = Field(min_length=1, max_length=200)

    status_id: int = Field(gt=0)
    status_name: str = Field(min_length=1, max_length=100)

    comment: str | None = Field(default=None, max_length=2000)
    total_amount: float = Field(ge=0)

    items: list[OrderItemAdminDTO]