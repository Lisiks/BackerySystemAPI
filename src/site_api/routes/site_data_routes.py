from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.site_api.views import get_branches_info
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
