from fastapi import APIRouter

router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"]
)

@router.get("/")
def get_alerts():

    return [
        {
            "id": "AL001",
            "message": "COD exceeded permissible limit",
            "severity": "Critical",
            "date": "20-06-2026",
            "status": "Open"
        },
        {
            "id": "AL002",
            "message": "CTO expires within 30 days",
            "severity": "Warning",
            "date": "18-06-2026",
            "status": "Open"
        }
    ]