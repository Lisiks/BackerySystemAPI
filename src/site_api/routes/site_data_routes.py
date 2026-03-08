from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.site_api.views import *
from src.site_api.dto_models import *

site_data_route = APIRouter(prefix="/sitedata")
