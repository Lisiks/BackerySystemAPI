from pydantic import BaseModel, Field


class BranchesAddDTO(BaseModel):
    branches_name: str = Field(max_length=100)
    branches_address: str = Field(max_length=200)
    branches_phone: str = Field(pattern="^\\+\\d{1,3}\\(\\d{3}\\)\\d{3}\\-\\d{2}\\-\\d{2}$")
    is_active_for_order: bool


class BranchesDTO(BranchesAddDTO):
    id: int = Field(gt=0)
