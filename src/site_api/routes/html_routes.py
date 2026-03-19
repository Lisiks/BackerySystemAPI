from fastapi import APIRouter, Request, Path
from fastapi.templating import Jinja2Templates
from src.config import settings

from src.site_api.views import *

html_route = APIRouter(prefix="/site")
templates = Jinja2Templates(directory=settings.DIRECTORY_NAME + "/templates")


@html_route.get("/catalog")
def index(request: Request):
    branches = get_branches_info()
    categories = get_categories_info()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"branches": branches, "categories": categories, "domain": settings.full_domain}
    )


@html_route.get("/catalog/{product_id}")
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
        }
    )