from pydantic import BaseModel, Field


class ProductsAddDTO(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    category_id: int = Field(gt=0)
    sale_price: float = Field(gt=0)
    cost_price: float = Field(ge=0)
    composition: str = Field(min_length=1, max_length=1000)
    description: str = Field(min_length=1, max_length=2000)
    calories: int = Field(ge=0)
    protein: float = Field(ge=0)
    fat: float = Field(ge=0)
    carbs: float = Field(ge=0)
    weight: int = Field(gt=0)
    is_visible: bool


class ProductsUpdateDTO(ProductsAddDTO):
    id: int = Field(gt=0)


class ProductsDTO(ProductsAddDTO):
    id: int = Field(gt=0)
    image_url: str = Field(min_length=1, max_length=500)


class ProductsListDTO(BaseModel):
    products: list[ProductsDTO]


class MessageDTO(BaseModel):
    message: str