from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class BranchesORM(Base):
    __tablename__ = "branches"
    id: Mapped[int] = mapped_column(primary_key=True)
    branches_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    branches_address: Mapped[str] = mapped_column(nullable=False, unique=True)
    branches_phone: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active_for_order: Mapped[bool] = mapped_column(nullable=False)


class CategoriesORM(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    category_description: Mapped[str] = mapped_column(nullable=True)
    showing_number: Mapped[int] = mapped_column(unique=True, nullable=False)
    display_on_site: Mapped[bool] = mapped_column(nullable=False)

class ProductsORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
    )

    sale_price: Mapped[float] = mapped_column(nullable=False)
    cost_price: Mapped[float] = mapped_column(nullable=False)

    composition: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    calories: Mapped[int] = mapped_column(nullable=False)
    protein: Mapped[float] = mapped_column(nullable=False)
    fat: Mapped[float] = mapped_column(nullable=False)
    carbs: Mapped[float] = mapped_column(nullable=False)

    weight: Mapped[int] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)

    is_visible: Mapped[bool] = mapped_column(nullable=False, default=True)