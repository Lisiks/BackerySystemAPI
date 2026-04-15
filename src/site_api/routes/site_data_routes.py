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


@site_data_route.get(
    path="/orders",
    tags=["Заказы🧾"],
    name="Получить все заказы текущего пользователя",
    summary="При помощи данного запроса должно производиться получение всех заказов текущего пользователя "
            "по access JWT.",
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
            " по access JWT.",
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
            create_order(user.id, order_data, session)

        return JSONResponse(
            content={"message": "ok"},
            status_code=status.HTTP_201_CREATED
        )

    except HTTPException:
        return JSONResponse(
            content={"message": "AuthError"},
            status_code=status.HTTP_403_FORBIDDEN
        )
    except NoBranchError:
        return JSONResponse(
            content={"message": "UncorrectBranch"},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    except UnavaliableBranch:
        return JSONResponse(
            content={"message": "UnavaliableBranch"},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

    except UnavaliableProducts as e:
        return JSONResponse(
            content={"message": "UnavaliableProduct", "products": e.args[0]},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@site_data_route.put(
    path="/orders/cancel/{order_id}",
    tags=["Заказы🧾"],
    name="Отменить заказ",
    summary="При помощи данного запроса должна производиться отмена заказа текущего пользователя по access JWT.",
    response_model=OrderCancelResponseDTO,
    response_class=JSONResponse
)
def cancel_order(
    order_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        access_token = credentials.credentials

        with session_fabric() as session:
            user = validate_access_token(access_token, session)
            result = cancel_user_order(user.id, order_id, session)

        return JSONResponse(
            content=result.model_dump(),
            status_code=status.HTTP_200_OK
        )

    except HTTPException as e:
        return JSONResponse(
            content={"message": "Ошибка валидации", "description": e.detail},
            status_code=e.status_code
        )

    except NoRecordError as e:
        return JSONResponse(
            content={"message": "Ошибка отсутствующей записи", "description": e.args},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


@site_data_route.post(
    path='/support',
    tags=["Запросы для фронтенда сайта ⚙️"],
    name="Отправить сообщение на почту поддержки",
    response_class=JSONResponse
)
def create_support_msg(support_message: SupportMessage):
    try:
        send_support_message(support_message.username, support_message.message_theme, support_message.message_text, support_message.user_email)
        return JSONResponse(
            content={"message": "ok"},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return JSONResponse(
            content={"message": "ServerError"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


