from fastapi import APIRouter, Request, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.config import settings

from src.site_api.views import *

html_route = APIRouter(prefix="/site")
templates = Jinja2Templates(directory=settings.DIRECTORY_NAME + "/templates")


@html_route.get(
    path="/catalog",
    response_class=HTMLResponse,
    tags=["</> HTML запросы сайта"],
    summary="Страница каталога сайта"
)
def index(request: Request):
    branches = get_branches_info()
    categories = get_categories_info()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"branches": branches, "categories": categories, "domain": settings.full_domain}
    )


@html_route.get(
    path="/catalog/{product_id}",
    response_class=HTMLResponse,
    tags=["</> HTML запросы сайта"],
    summary="Страница изделия на сатйе"
)
def product_page(request: Request, product_id: int = Path(gt=0)):
    branches = get_branches_info()
    categories = get_categories_info()
    product_info = get_product_info_by_id(product_id)

    return templates.TemplateResponse(
        request=request,
        name="product.html",
        context={
            "branches": branches,
            "categories": categories,
            "product": product_info,
            "domain": settings.full_domain
        }) if product_info is not None else templates.TemplateResponse(

        request=request,
        name="error_page.html",
        context={
            "branches": branches,
            "categories": categories,
            "domain": settings.full_domain
        }
    )


@html_route.get(
    path="/faq",
    response_class=HTMLResponse,
    tags=["</> HTML запросы сайта"],
    summary="Страница faq сайта"
)
def index(request: Request):
    branches = get_branches_info()
    categories = get_categories_info()

    return templates.TemplateResponse(
        request=request,
        name="faq.html",
        context={"branches": branches, "categories": categories, "domain": settings.full_domain}
    )


@html_route.get(
    path="/about",
    response_class=HTMLResponse,
    tags=["</> HTML запросы сайта"],
    summary="Страница о компании сайта"
)
def index(request: Request):
    branches = get_branches_info()
    categories = get_categories_info()

    return templates.TemplateResponse(
        request=request,
        name="about_company.html",
        context={"branches": branches, "categories": categories, "domain": settings.full_domain}
    )


@html_route.get(
    path="/new_order",
    response_class=HTMLResponse,
    tags=["</> HTML запросы сайта"],
    summary="Страница для создания заказа"
)
def index(request: Request):
    branches = get_branches_info()
    categories = get_categories_info()

    return templates.TemplateResponse(
        request=request,
        name="order_page.html",
        context={"branches": branches, "categories": categories, "domain": settings.full_domain}
    )