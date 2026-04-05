from pydantic import BaseModel, Field
from datetime import datetime


class BranchesGetDTO(BaseModel):
    id: int = Field(gt=0)
    branches_address: str = Field(max_length=200)
    branches_phone: str = Field(pattern="^\\+\\d{1,3}\\(\\d{3}\\)\\d{3}\\-\\d{2}\\-\\d{2}$")


class CategoriesGetDTO(BaseModel):
    id: int = Field(gt=0)
    category_name: str = Field(max_length=100)
    showing_number: int = Field(gt=0)


class ProductsGetDTO(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=200)
    sale_price: float = Field(gt=0)
    weight: int = Field(gt=0)
    image_url: str = Field(min_length=1, max_length=500)


class ProductsFullInfoDTO(ProductsGetDTO):
    composition: str = Field(min_length=1, max_length=1000)
    description: str = Field(min_length=1, max_length=2000)
    calories: int = Field(ge=0)
    protein: float = Field(ge=0)
    fat: float = Field(ge=0)
    carbs: float = Field(ge=0)
    category_name: str = Field(max_length=100)

class FavoriteProductAddDTO(BaseModel):
    product_id: int = Field(gt=0)

class MessageDTO(BaseModel):
    message: str


class OrderItemAddDTO(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderAddDTO(BaseModel):
    username: str = Field(max_length=50)
    phone: str = Field(min_length=5, max_length=30)
    items: list[OrderItemAddDTO] = Field(min_length=1)
    order_datetime: datetime
    branch_id: int = Field(gt=0)
    comment: str | None = Field(default=None, max_length=1000)


class OrderCreateResponseDTO(BaseModel):
    message: str
    order_id: int = Field(gt=0)