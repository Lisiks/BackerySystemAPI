from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.site_api.views import *
from src.site_api.dto_models import *

site_data_route = APIRouter(prefix="/sitedata")


@site_data_route.get(
    path="/branches",
    tags=["Запросы для контента сайта📂"],
    name="Получить информацию о филиалах",
    summary="При помощи данного запроса осуществляется передача контактной информации о филиалах организации "
            "(id, адрес, телефон) необходимых для отображения в подвале сайта и на форме для оформления заказа.",
    response_class=JSONResponse
)
def get_branches_data_for_site():
    branches = get_branches_info()
    return JSONResponse(content={"branches": branches}, status_code=status.HTTP_200_OK)


@site_data_route.get(
    path="/categories",
    tags=["Запросы для контента сайта📂"],
    name="Получить информацию о категориях",
    summary="При помощи данного запроса осуществляется передача необходимой для отображения на сайте информации о "
            "категориях товаров (id, имя категории, порядок отображения).",
    response_class=JSONResponse
)
def get_category_data_for_site():
    categories = get_categories_info()
    return JSONResponse(content={"categories": categories}, status_code=status.HTTP_200_OK)