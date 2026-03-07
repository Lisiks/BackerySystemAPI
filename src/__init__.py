from fastapi import FastAPI
from src.admin_api.routes import admin_route
from src.login_api.routes import login_route
from src.site_api.routes import site_route

app = FastAPI(
    title="Система для оформления и обработки онлайн заказов в пекарне API",
    description=("В данной документации содержится информация обо всех используемых"
                 "в разработке API рутах, их параметрах и назначении."),
    version="1.0.0",
    debug=True,
    docs_url="/"
)

app.include_router(admin_route)
app.include_router(login_route)
app.include_router(site_route)
