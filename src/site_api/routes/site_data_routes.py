from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.errors import NoRecordError
from src.site_api.views import (get_all_available_products_by_category, add_product_to_favorites,
                                delete_product_from_favorites)
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
    summary="Добавляет товар в избранное для текущего пользователя по access JWT token.",
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
            user_id = user.id

        add_product_to_favorites(user_id, favorite_product.product_id)

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
        return JSONResponse(
            content={"message": "Ошибка валидации", "description": str(e)},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except NoRecordError as e:
        return JSONResponse(
            content={"message": "Ошибка отсутствующей записи", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@site_data_route.delete(
    path="/favorites/delete/{product_id}",
    tags=["Избранное❤️"],
    name="Удалить товар из избранного",
    summary="Удаляет товар из избранного для текущего пользователя по access JWT token.",
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
            user_id = user.id

        delete_product_from_favorites(user_id, product_id)

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
        return JSONResponse(
            content={"message": "Ошибка валидации", "description": str(e)},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except NoRecordError as e:
        return JSONResponse(
            content={"message": "Ошибка отсутствующей записи", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )