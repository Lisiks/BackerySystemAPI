from pydantic import BaseModel, Field


class OrderStatusChangeModel(BaseModel):
    order_id: int = Field(gt=0)
    status_id: int = Field(gt=0, lt=6)