from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from src.config import settings

from src.site_api.views import get_categories_info, get_branches_info

html_route = APIRouter(prefix="/site")
templates = Jinja2Templates(directory=settings.DIRECTORY_NAME + "/templates")


@html_route.get("/")
def index(request: Request):
    branches = get_branches_info()
    categories = get_categories_info()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"branches": branches, "categories": categories}
    )