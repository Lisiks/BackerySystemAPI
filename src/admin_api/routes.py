from fastapi import APIRouter, status, UploadFile, File, Form, Depends, HTTPException, Path
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.admin_api.orders.views import *
from src.admin_api.employees.dto_models import ( EmployeeAddDTO, EmployeeUpdateDTO, AuthenticateEmployeeRequestDTO,
                                           AuthenticateEmployeeResponseDTO)
from src.admin_api.orders.dto_models import OrderStatusChangeModel
from src.admin_api.employees.views import (get_all_employees, get_employee, create_employee, update_employee,
                                           get_all_positions, delete_employee, authenticate_employee)
from src.admin_api.branches.views import create_branch, update_branch, get_all_branches
from src.admin_api.branches.dto_models import BranchesDTO, BranchesAddDTO
from src.admin_api.categories.views import create_category, get_all_categories, update_category
from src.admin_api.categories.dto_models import CategoriesDTO, CategoriesAddDTO
from src.admin_api.products.views import create_product, update_product, get_all_products
from src.admin_api.products.dto_models import ProductsAddDTO, ProductsUpdateDTO

admin_route = APIRouter(prefix="/admin")


def get_db():
    session = session_fabric()
    try:
        yield session
    finally:
        session.close()


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
    product_id: int = Form(...),
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
            id=product_id,
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


@admin_route.get(
    path="/orders/{employee_id}",
    tags=["Заказы"],
    name="Получить все заказы, доступные сотруднику",
    summary="Получить все заказы, доступные сотруднику",
    response_class=JSONResponse
)
def get_orders(employee_id: int = Path(gt=0)):
    try:
        result = get_all_orders_to_employee(employee_id)
        return JSONResponse(content={"orders": result}, status_code=status.HTTP_200_OK)
    except NoRecordError as e:
        return JSONResponse(content={"message": f"{e.args[0]}"}, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)

@admin_route.put(
    path="/orders/update",
    tags=["Заказы"],
    name="Изменить статус заказа",
    summary="Изменить статус заказа",
    response_class=JSONResponse
)
def change_order_status_route(change_order_data: OrderStatusChangeModel):
    try:
        change_order_status(change_order_data)
        return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_200_OK)
    except NoRecordError as e:
        return JSONResponse(content={"message": f"{e.args[0]}"}, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)


@admin_route.get(
    path="/employees",
    tags=["Сотрудники👥"],
    name="Получить данные обо всех сотрудниках",
    summary="При помощи данного запроса должно производиться получение данных обо всех сотрудниках "
            "для административного приложения.",
    response_class=JSONResponse
)
def get_employees(
    session: Session = Depends(get_db),
):
    employees = get_all_employees(session)
    return JSONResponse(
        content={"employees": employees},
        status_code=status.HTTP_200_OK
    )


@admin_route.get(
    path="/employees/{employee_id}",
    tags=["Сотрудники👥"],
    name="Получить данные о сотруднике",
    summary="При помощи данного запроса должно производиться получение данных "
            "о конкретном сотруднике для административного приложения.",
    response_class=JSONResponse
)
def get_employee_route(
    employee_id: int,
    session: Session = Depends(get_db),
):
    try:
        employee = get_employee(employee_id, session)
        return JSONResponse(
            content={"employee": employee},
            status_code=status.HTTP_200_OK
        )
    except NoRecordError as e:
        return JSONResponse(
            content={"message": "No record error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@admin_route.get(
    path="/positions",
    tags=["Сотрудники👥"],
    name="Получить данные обо всех должностях",
    summary="При помощи данного запроса должно производиться получение данных обо всех должностях для формы сотрудников административного приложения.",
    response_class=JSONResponse
)
def get_positions(
    session: Session = Depends(get_db),
):
    positions = get_all_positions(session)
    return JSONResponse(
        content={"positions": positions},
        status_code=status.HTTP_200_OK
    )


@admin_route.post(
    path="/employees/authenticate",
    tags=["Сотрудники👥"],
    name="Аутентификация сотрудника",
    summary="При помощи данного запроса должна производиться аутентификация сотрудника по логину и паролю "
            "в административном приложении.",
    response_model=AuthenticateEmployeeResponseDTO,
    response_class=JSONResponse
)
def authenticate_employee_route(
    data: AuthenticateEmployeeRequestDTO,
    session: Session = Depends(get_db),
):
    try:
        result = authenticate_employee(data, session)
        return JSONResponse(
            content=result.model_dump(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        return JSONResponse(
            content={"message": e.detail},
            status_code=e.status_code
        )


@admin_route.post(
    path="/employees/add",
    tags=["Сотрудники👥"],
    name="Добавить сотрудника",
    summary="При помощи данного запроса должно производиться создание записи о сотруднике на основании данных"
            " из административного приложения.",
    response_class=JSONResponse
)
def post_employee(
    new_employee: EmployeeAddDTO,
    session: Session = Depends(get_db),
):
    try:
        create_employee(new_employee, session)
        return JSONResponse(
            content={"message": "ok"},
            status_code=status.HTTP_200_OK
        )
    except IntegrityError as e:
        return JSONResponse(
            content={"message": "Integrity error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@admin_route.put(
    path="/employees/update/{employee_id}",
    tags=["Сотрудники👥"],
    name="Изменить сотрудника",
    summary="При помощи данного запроса должно производиться изменение сотрудника на основании поступивших данных"
            " из административного приложения.",
    response_class=JSONResponse
)
def put_employee(
    employee_id: int,
    current_employee: EmployeeUpdateDTO,
    session: Session = Depends(get_db),
):
    try:
        update_employee(employee_id, current_employee, session)
        return JSONResponse(
            content={"message": "ok"},
            status_code=status.HTTP_200_OK
        )
    except NoRecordError as e:
        return JSONResponse(
            content={"message": "No record error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except IntegrityError as e:
        return JSONResponse(
            content={"message": "Integrity error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@admin_route.delete(
    path="/employees/delete/{employee_id}",
    tags=["Сотрудники👥"],
    name="Удалить сотрудника",
    summary="При помощи данного запроса должно производиться удаление сотрудника "
            "по его id для административного приложения.",
    response_class=JSONResponse
)
def delete_employee_route(
    employee_id: int,
    session: Session = Depends(get_db),
):
    try:
        delete_employee(employee_id, session)
        return JSONResponse(
            content={"message": "ok"},
            status_code=status.HTTP_200_OK
        )
    except NoRecordError as e:
        return JSONResponse(
            content={"message": "No record error", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
