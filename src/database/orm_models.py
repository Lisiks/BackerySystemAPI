from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column


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

