from fastapi import APIRouter,status
from fastapi.responses import JSONResponse
from src.admin_api.branches.views import *
from src.admin_api.branches.dto_models import *

admin_route = APIRouter(prefix="/admin")


@admin_route.get(
    path="/branches",
    tags=["Филиалы🏘️"],
    name="Получить данные обо всех филиалах",
    summary="При помощи данного запроса должна производиться загрузка данных о филиалах, включая все их поля "
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
    summary="При помощи данного запроса должна производиться создание филиала на основе поступившей с админ приложения"
            "информации (имя, адрес, телефонЮ возможность осуществить заказ) и его сохранение в БД.",
    response_class=JSONResponse
)
def post_branch(new_branch: BranchesAddDTO):
    post_result = create_branch(new_branch)
    return JSONResponse(content={"message": post_result}, status_code=status.HTTP_200_OK)


@admin_route.put(
    path="/branches/update",
    tags=["Филиалы🏘️"],
    name="Изменить филиал",
    summary="При помощи данного запроса должна производиться изменение филиала на основе поступившей с админ приложения"
            "информации (имя, адрес, телефонЮ возможность осуществить заказ) и его сохранение в БД. При отправке"
            "данного запроса система админ приложения должна отправить JSON объект филиала со старым id и новыми"
            "данными.",
    response_class=JSONResponse
)
def put_branch(current_branch: BranchesDTO):
    put_result = update_branch(current_branch)
    return JSONResponse(content={"message": put_result}, status_code=status.HTTP_200_OK)
