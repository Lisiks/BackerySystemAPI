from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.site_api.views import *
from src.site_api.dto_models import *
from src.login_api.views import validate_access_token
from src.database.database import session_fabric

site_data_route = APIRouter(prefix="/sitedata")
security = HTTPBearer()




@site_data_route.get(
    path="/product",
    tags=["Запросы для фронтенда сайта ⚙️"],
    name="Получить доступные изделия по категориям",
    summary="При помощи данного запроса на сайт загружается информация по доступным товарам по категориям",
    response_class=JSONResponse
)
def get_available_products():
    products_by_categories = get_all_available_products_by_category()
    return JSONResponse(content={"categories": products_by_categories}, status_code=status.HTTP_200_OK)


@site_data_route.post(
    path="/favorites/add",
    tags=["Избранное❤️"],
    name="Добавить товар в избранное",
    summary="При помощи данного запроса должно производиться добавление товара в избранное для текущего пользователя"
            " по access JWT токену.",
    response_model=MessageDTO,
    response_class=JSONResponse
)
def post_favorite_product(
    favorite_product: FavoriteProductAddDTO,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        access_token = credentials.credentials

        with session_fabric() as session:
            user = validate_access_token(access_token, session)
            add_product_to_favorites(user.id, favorite_product.product_id, session)


        return JSONResponse(
            content={"message": "ОК"},
            status_code=status.HTTP_200_OK
        )

    except HTTPException as e:
        return JSONResponse(
            content={"message": "Ошибка авторизации", "description": e.detail},
            status_code=e.status_code
        )

    except ValueError as e:
        payload = e.args[0] if e.args else "Ошибка валидации"

        if isinstance(payload, dict):
            return JSONResponse(
                content=payload,
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
            )

        return JSONResponse(
            content={"message": "Ошибка валидации", "description": str(payload)},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    except NoRecordError as e:
        payload = e.args[0] if e.args else "Ошибка отсутствующей записи"

        if isinstance(payload, dict):
            return JSONResponse(
                content=payload,
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
            )
        return JSONResponse(
            content={"message": "Ошибка отсутствующей записи", "description": payload},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

@site_data_route.delete(
    path="/favorites/delete/{product_id}",
    tags=["Избранное❤️"],
    name="Удалить товар из избранного",
    summary="При помощи данного запроса должно производиться удаление товара из избранного для текущего пользователя"
            " по access JWT токену.",
    response_model=MessageDTO,
    response_class=JSONResponse
)
def delete_favorite_product(
    product_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        access_token = credentials.credentials

        with session_fabric() as session:
            user = validate_access_token(access_token, session)
            delete_product_from_favorites(user.id, product_id, session)

        return JSONResponse(
            content={"message": "ОК"},
            status_code=status.HTTP_200_OK
        )

    except HTTPException as e:
        return JSONResponse(
            content={"message": "Ошибка авторизации", "description": e.detail},
            status_code=e.status_code
        )

    except ValueError as e:
        payload = e.args[0] if e.args else "Ошибка валидации"

        if isinstance(payload, dict):
            return JSONResponse(
                content=payload,
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
            )

        return JSONResponse(
            content={"message": "Ошибка валидации", "description": str(payload)},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    except NoRecordError as e:
        payload = e.args[0] if e.args else "Ошибка отсутствующей записи"

        if isinstance(payload, dict):
            return JSONResponse(
                content=payload,
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
            )
        return JSONResponse(
            content={"message": "Ошибка отсутствующей записи", "description": payload},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@site_data_route.get(
    path="/orders",
    tags=["Заказы🧾"],
    name="Получить все заказы текущего пользователя",
    summary="При помощи данного запроса должно производиться получение всех заказов текущего пользователя "
            "по access JWT токену.",
    response_class=JSONResponse
)
def get_orders(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        access_token = credentials.credentials

        with session_fabric() as session:
            user = validate_access_token(access_token, session)
            orders = get_user_orders(user.id, session)

        return JSONResponse(
            content={"orders": orders},
            status_code=status.HTTP_200_OK
        )

    except HTTPException as e:
        return JSONResponse(
            content={"message": "Ошибка авторизации", "description": e.detail},
            status_code=e.status_code
        )


@site_data_route.post(
    path="/orders/add",
    tags=["Заказы🧾"],
    name="Создать заказ",
    summary="При помощи данного запроса должно производиться создание нового заказа для текущего пользователя"
            " по access JWT токену.",
    response_model=OrderCreateResponseDTO,
    response_class=JSONResponse
)
def post_order(
    order_data: OrderAddDTO,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        access_token = credentials.credentials

        with session_fabric() as session:
            user = validate_access_token(access_token, session)
            result = create_order(user.id, order_data, session)

        return JSONResponse(
            content=result,
            status_code=status.HTTP_201_CREATED
        )

    except HTTPException as e:
        return JSONResponse(
            content={"message": "Ошибка авторизации", "description": e.detail},
            status_code=e.status_code
        )

    except ValueError as e:
        payload = e.args[0] if e.args else "Ошибка валидации"

        if isinstance(payload, dict):
            return JSONResponse(
                content=payload,
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
            )

        return JSONResponse(
            content={"message": "Ошибка валидации", "description": str(payload)},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    except NoRecordError as e:
        payload = e.args[0] if e.args else "Ошибка отсутствующей записи"

        if isinstance(payload, dict):
            return JSONResponse(
                content=payload,
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
            )
        return JSONResponse(
            content={"message": "Ошибка отсутствующей записи", "description": payload},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )