from fastapi import FastAPI
from src.admin_api.routes import admin_route
from src.login_api.routes import login_route
from src.site_api.routes.html_routes import html_route
from src.site_api.routes.site_data_routes import site_data_route
from fastapi.staticfiles import StaticFiles
from src.config import settings

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
app.include_router(html_route)
app.include_router(site_data_route)

app.mount(
    "/static",
    StaticFiles(directory=settings.DIRECTORY_NAME),
    name="static"
)