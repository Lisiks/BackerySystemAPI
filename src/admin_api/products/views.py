import os
import uuid

from sqlalchemy import select
from src.database.database import session_fabric
from src.database.orm_models import ProductsORM, CategoriesORM
from src.admin_api.products.dto_models import ProductsAddDTO, ProductsUpdateDTO, ProductsDTO
from src.errors import NoRecordError


UPLOAD_DIR = "src/static/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_all_products():
    with session_fabric() as session:
        query = select(ProductsORM).select_from(ProductsORM)
        orm_result = session.execute(query).scalars().all()

        return [
            ProductsDTO.model_validate(orm_record, from_attributes=True).dict()
            for orm_record in orm_result
        ]


def create_product(new_product: ProductsAddDTO):
    with session_fabric() as session:
        if new_product.category_id is not None:
            category = session.get(CategoriesORM, {"id": new_product.category_id})
            if category is None:
                raise NoRecordError(f"No category with id={new_product.category_id}")

        new_product_orm = ProductsORM(
            name=new_product.name,
            category_id=new_product.category_id,
            sale_price=new_product.sale_price,
            cost_price=new_product.cost_price,
            composition=new_product.composition,
            description=new_product.description,
            calories=new_product.calories,
            protein=new_product.protein,
            fat=new_product.fat,
            carbs=new_product.carbs,
            weight=new_product.weight,
            image_url=new_product.image_url,
            is_visible=new_product.is_visible
        )

        session.add(new_product_orm)
        session.commit()


def update_product(current_product: ProductsUpdateDTO):
    with session_fabric() as session:
        current_product_orm = session.get(ProductsORM, {"id": current_product.id})
        if current_product_orm is None:
            raise NoRecordError(f"No record with id={current_product.id}")

        if current_product.category_id is not None:
            category = session.get(CategoriesORM, {"id": current_product.category_id})
            if category is None:
                raise NoRecordError(f"No category with id={current_product.category_id}")

        current_product_orm.name = current_product.name
        current_product_orm.category_id = current_product.category_id
        current_product_orm.sale_price = current_product.sale_price
        current_product_orm.cost_price = current_product.cost_price
        current_product_orm.composition = current_product.composition
        current_product_orm.description = current_product.description
        current_product_orm.calories = current_product.calories
        current_product_orm.protein = current_product.protein
        current_product_orm.fat = current_product.fat
        current_product_orm.carbs = current_product.carbs
        current_product_orm.weight = current_product.weight
        current_product_orm.image_url = current_product.image_url
        current_product_orm.is_visible = current_product.is_visible

        session.commit()


def save_product_image(image_file) -> str:
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    file_extension = os.path.splitext(image_file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise ValueError("Недопустимый формат изображения")

    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as file_object:
        file_object.write(image_file.file.read())

    return f"/static/products/{unique_filename}"