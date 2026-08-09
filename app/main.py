from fastapi import FastAPI
from app.database import Base, engine
from app.routes.auth_routes import router as auth_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.document_routes import router as document_router
from app.routes.report_routes import router as report_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.routes.frontend_routes import router as frontend_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.alert_routes import router as alert_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Compliance Intelligence API")
app.include_router(alert_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(document_router)
app.include_router(report_router)
app.include_router(frontend_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(
    directory="frontend"
)



@app.get("/")
def root():
    return {"message": "Backend is running successfully"}


@app.get("/login")
def login_page(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/register")
def register_page(request: Request):

    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


@app.get("/dashboard")
def dashboard_page(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@app.get("/uploadpage")
def upload_page(request: Request):

    return templates.TemplateResponse(
        "uploadpage.html",
        {"request": request}
    )