from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(
    directory="frontend"
)

@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )