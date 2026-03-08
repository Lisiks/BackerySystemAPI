from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from src.config import settings

html_route = APIRouter(prefix="/site")
templates = Jinja2Templates(directory=settings.DIRECTORY_NAME + "/templates")


@html_route.get("/")
def index(request: Request):
    pass
    return templates.TemplateResponse(
         request=request, name="base_template.html"
    )