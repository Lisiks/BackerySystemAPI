from fastapi import APIRouter, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from src.errors import NoRecordError

from src.admin_api.branches.views import create_branch, update_branch, get_all_branches
from src.admin_api.branches.dto_models import BranchesDTO, BranchesAddDTO
from src.admin_api.categories.views import create_category, get_all_categories, update_category
from src.admin_api.categories.dto_models import CategoriesDTO, CategoriesAddDTO

from src.admin_api.products.views import create_product, update_product, get_all_products
from src.admin_api.products.dto_models import ProductsDTO, ProductsAddDTO, ProductsUpdateDTO, ProductsListDTO

admin_route = APIRouter(prefix="/admin")


@admin_route.get(
    path="/branches",
    tags=["Филиалы🏘️"],
    name="Получить данные обо всех филиалах",
    summary="При помощи данного запроса должно производиться загрузка данных о филиалах, включая все их поля "
            "(id, имя, адрес, телефон, возможность осуществить заказ) в админ приложение",
    response_class=JSONResponse
)
def get_branches():
    branches = get_all_branches()
    return JSONResponse(content={"branches": branches}, status_code=status.HTTP_200_OK)


@admin_route.post(
    path="/branches/add",
    tags=["Филиалы🏘️"],
    name="Добавить филиал",
    summary="При помощи данного запроса должно производиться создание филиала на основе поступившей с админ приложения"
            "информации (имя, адрес, телефонЮ возможность осуществить заказ) и его сохранение в БД.",
    response_class=JSONResponse
)
def post_branch(new_branch: BranchesAddDTO):
    try:
        create_branch(new_branch)
        return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_200_OK)
    except IntegrityError as e:
        return JSONResponse(
            content={"message": "Integrity error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@admin_route.put(
    path="/branches/update",
    tags=["Филиалы🏘️"],
    name="Изменить филиал",
    summary="При помощи данного запроса должно производиться изменение филиала на основе поступившей с админ приложения"
            "информации (имя, адрес, телефона, возможность осуществить заказ) и его сохранение в БД. При отправке"
            "данного запроса система админ приложения должна отправить JSON объект филиала со старым id и новыми"
            "данными.",
    response_class=JSONResponse
)
def put_branch(current_branch: BranchesDTO):
    try:
        update_branch(current_branch)
        return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_200_OK)
    except IntegrityError as e:
        return JSONResponse(
            content={"message": "Integrity error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except NoRecordError as e:
        return JSONResponse(
            content={"message": "No record error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@admin_route.get(
    path="/categories",
    tags=["Категории🥯🥖🥐️"],
    name="Получить данные обо всех категориях",
    summary="При помощи данного запроса должно производиться загрузка данных о категориях, включая все их поля "
            "(id, имя, описание, номер отображения, необходимость в отображении) в админ приложении",
    response_class=JSONResponse
)
def get_categories():
    categories = get_all_categories()
    return JSONResponse(content={"categories": categories}, status_code=status.HTTP_200_OK)


@admin_route.post(
    path="/categories/add",
    tags=["Категории🥯🥖🥐️"],
    name="Добавить категорию",
    summary="При помощи данного запроса должно производиться создание катогории на основе поступившей с админ "
            "приложения информации (имя, описание, номер отображения, необходимость в отображении) и ее сохранение.",
    response_class=JSONResponse
)
def post_category(new_category: CategoriesAddDTO):
    try:
        create_category(new_category)
        return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_200_OK)
    except IntegrityError as e:
        return JSONResponse(
            content={"message": "Integrity error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@admin_route.put(
    path="/categories/update",
    tags=["Категории🥯🥖🥐️"],
    name="Изменить категорию",
    summary="При помощи данного запроса должно производиться изменение категории на основе поступившей с админ "
            "приложения информации (id, имя, описание, номер отображения, необходимость в отображении) и его "
            "сохранение в БД. При отправке данного запроса система админ приложения должна отправить JSON объект "
            "филиала со старым id и новыми данными.",
    response_class=JSONResponse
)
def put_category(current_category: CategoriesDTO):
    try:
        update_category(current_category)
        return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_200_OK)
    except IntegrityError as e:
        return JSONResponse(
            content={"message": "Integrity error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except NoRecordError as e:
        return JSONResponse(
            content={"message": "No record error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

@admin_route.get(
    path="/products",
    tags=["Товары🥐"],
    name="Получить данные обо всех товарах",
    summary="При помощи данного запроса должно производиться получение данных обо всех товарах "
            "для административного приложения.",
    response_model=ProductsListDTO,
    response_class=JSONResponse
)
def get_products():
    products = get_all_products()
    return JSONResponse(content={"products": products}, status_code=status.HTTP_200_OK)

@admin_route.post(
    path="/products/add",
    tags=["Товары🥐"],
    name="Добавить товар",
    summary="При помощи данного запроса должно производиться создание товара и загрузка его изображения "
            "одним multipart-запросом.",
    response_class=JSONResponse
)
def post_product(
    name: str = Form(...),
    category_id: int = Form(...),
    sale_price: float = Form(...),
    cost_price: float = Form(...),
    composition: str = Form(...),
    description: str = Form(...),
    calories: int = Form(...),
    protein: float = Form(...),
    fat: float = Form(...),
    carbs: float = Form(...),
    weight: int = Form(...),
    is_visible: bool = Form(...),
    image_file: UploadFile = File(...)
):
    try:
        new_product = ProductsAddDTO(
            name=name,
            category_id=category_id,
            sale_price=sale_price,
            cost_price=cost_price,
            composition=composition,
            description=description,
            calories=calories,
            protein=protein,
            fat=fat,
            carbs=carbs,
            weight=weight,
            is_visible=is_visible
        )

        create_product(new_product, image_file)
        return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_200_OK)

    except IntegrityError as e:
        return JSONResponse(
            content={"message": "Integrity error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except NoRecordError as e:
        return JSONResponse(
            content={"message": "No record error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except ValueError as e:
        return JSONResponse(
            content={"message": "Validation error", "description": str(e)},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

@admin_route.put(
    path="/products/update",
    tags=["Товары🥐"],
    name="Изменить товар",
    summary="При помощи данного запроса должно производиться изменение товара. "
            "При передаче нового изображения старое изображение удаляется, а новое сохраняется под id товара.",
    response_class=JSONResponse
)
def put_product(
    id: int = Form(...),
    name: str = Form(...),
    category_id: int = Form(...),
    sale_price: float = Form(...),
    cost_price: float = Form(...),
    composition: str = Form(...),
    description: str = Form(...),
    calories: int = Form(...),
    protein: float = Form(...),
    fat: float = Form(...),
    carbs: float = Form(...),
    weight: int = Form(...),
    is_visible: bool = Form(...),
    image_file: UploadFile | None = File(None)
):
    try:
        current_product = ProductsUpdateDTO(
            id=id,
            name=name,
            category_id=category_id,
            sale_price=sale_price,
            cost_price=cost_price,
            composition=composition,
            description=description,
            calories=calories,
            protein=protein,
            fat=fat,
            carbs=carbs,
            weight=weight,
            is_visible=is_visible
        )

        update_product(current_product, image_file)
        return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_200_OK)

    except IntegrityError as e:
        return JSONResponse(
            content={"message": "Integrity error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except NoRecordError as e:
        return JSONResponse(
            content={"message": "No record error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except ValueError as e:
        return JSONResponse(
            content={"message": "Validation error", "description": str(e)},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )