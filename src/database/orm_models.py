#from src.database.database import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey, String, Boolean, DateTime, Text, create_engine

class Base(DeclarativeBase):
    pass


class BranchesORM(Base):
    __tablename__ = "branches"
    id: Mapped[int] = mapped_column(primary_key=True)
    branches_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    branches_address: Mapped[str] = mapped_column(nullable=False, unique=True)
    branches_phone: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active_for_order: Mapped[bool] = mapped_column(nullable=False)

    orders: Mapped[list['OrdersORM']] = relationship(back_populates='branch')
    employees: Mapped[list['Employee']] = relationship(back_populates='branch')


class CategoriesORM(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    category_description: Mapped[str] = mapped_column(nullable=True)
    showing_number: Mapped[int] = mapped_column(unique=True, nullable=False)
    display_on_site: Mapped[bool] = mapped_column(nullable=False)

    visible_category_products: Mapped[list['ProductsORM']] = relationship(
        back_populates="category",
        primaryjoin="and_(CategoriesORM.id == ProductsORM.category_id, ProductsORM.is_visible == True)"
    )


class ProductsORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE", onupdate="CASCADE"),
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

    category: Mapped['CategoriesORM'] = relationship(back_populates="visible_category_products")
    order_products: Mapped[list['OrderItemsORM']] = relationship(back_populates='product')


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    orders: Mapped['OrdersORM'] = relationship(
        back_populates="user"
    )

class OrderStatusesORM(Base):
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    status_name: Mapped[str] = mapped_column(nullable=False, unique=True)

    orders: Mapped[list['OrdersORM']] = relationship(
        back_populates="order_status"
    )


class OrdersORM(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    username: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    order_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    status_id: Mapped[int] = mapped_column(
        ForeignKey("order_statuses.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    total_amount: Mapped[float] = mapped_column(nullable=False, default=0)

    order_status: Mapped['OrderStatusesORM'] = relationship(back_populates="orders")
    user: Mapped['UsersORM'] = relationship(back_populates="orders")
    branch: Mapped['BranchesORM'] = relationship(back_populates='orders')
    products: Mapped[list['OrderItemsORM']] = relationship(back_populates="order")



class OrderItemsORM(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True
    )

    quantity: Mapped[int] = mapped_column(nullable=False)
    total_price: Mapped[float] = mapped_column(nullable=False)

    order: Mapped['OrdersORM'] = relationship(back_populates="products")
    product: Mapped['ProductsORM'] = relationship(back_populates="order_products")


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    branches_id: Mapped[int] = mapped_column(ForeignKey("branches.id", ondelete="RESTRICT", onupdate="CASCADE"))

    branch: Mapped['BranchesORM'] = relationship(back_populates="employees")


class EmployeesORM(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )


# Добавлять отдельно

# engine = create_engine(DATABASE_URL, echo=True)

# # Вариант 1: Создать только employees
# Base.metadata.create_all(engine, tables=[EmployeesORM.__table__])