from pydantic import BaseModel, Field


class BranchesGetDTO(BaseModel):
    id: int = Field(gt=0)
    branches_address: str = Field(max_length=200)
    branches_phone: str = Field(pattern="^\\+\\d{1,3}\\(\\d{3}\\)\\d{3}\\-\\d{2}\\-\\d{2}$")


class CategoriesGetDTO(BaseModel):
    id: int = Field(gt=0)
    category_name: str = Field(max_length=100)
    showing_number: int = Field(gt=0)