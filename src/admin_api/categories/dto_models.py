from pydantic import BaseModel, Field


class CategoriesAddDTO(BaseModel):
    category_name: str = Field(max_length=100)
    category_description: str | None = Field(max_length=500)
    showing_number: int = Field(gt=0)
    display_on_site: bool


class CategoriesDTO(CategoriesAddDTO):
    id: int = Field(gt=0)
