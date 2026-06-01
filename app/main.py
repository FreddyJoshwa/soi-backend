from fastapi import FastAPI
from app.database import Base, engine
from app.routes.auth_routes import router as auth_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.document_routes import router as document_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Compliance Intelligence API")

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(document_router)

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}