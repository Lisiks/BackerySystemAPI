from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.site_api.views import *
from src.site_api.dto_models import *

site_data_route = APIRouter(prefix="/sitedata")


@site_data_route.get(
    path="/product",
    tags=["Запросы для фронтенда сайта ⚙️"],
    name="Получить доступные изделия по категориям",
    summary="При помощи данного запроса на сайт загружается информация по доступным товарам по категориям",
    response_class=JSONResponse
)
def get_available_products():
    products = get_all_available_products_by_category()
    return JSONResponse(content=products, status_code=status.HTTP_200_OK)
