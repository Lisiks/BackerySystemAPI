from pydantic import BaseModel, Field


class ProductsAddDTO(BaseModel):
    name: str = Field(max_length=200)
    category_id: int | None = None
    sale_price: float
    cost_price: float
    composition: str | None = None
    description: str | None = None
    calories: int | None = None
    protein: float | None = None
    fat: float | None = None
    carbs: float | None = None
    weight: int | None = None
    is_visible: bool


class ProductsUpdateDTO(ProductsAddDTO):
    id: int = Field(gt=0)


class ProductsDTO(ProductsAddDTO):
    id: int = Field(gt=0)
    image_url: str | None = None


class MessageDTO(BaseModel):
    message: str


class ProductImageUploadDTO(BaseModel):
    image_url: str