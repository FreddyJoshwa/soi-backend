from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import ComplianceReport
from app.database import get_db
from app.models import User
from sqlalchemy import func
from app.models import ExtractedReport

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


# ==============================
# DASHBOARD SUMMARY
# ==============================
@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):

    user = db.query(User).order_by(User.id.desc()).first()

    latest_report = (
        db.query(ExtractedReport)
        .order_by(ExtractedReport.id.desc())
        .first()
    )

    cto_status = "Not Available"
    cto_expiry_days = 0

    if user and user.cto_expiry_date:

        today = date.today()

        days_left = (user.cto_expiry_date - today).days

        cto_expiry_days = days_left

        if days_left > 30:
            cto_status = "Active"
        elif days_left > 0:
            cto_status = "Expiring Soon"
        else:
            cto_status = "Expired"

    compliance_score = 0
    compliance_status = "No Data"
    active_alerts = 0

    if latest_report:

        compliance_score = latest_report.compliance_score
        compliance_status = latest_report.overall_status

        if latest_report.cod and latest_report.cod > 250:
            active_alerts += 1

        if latest_report.bod and latest_report.bod > 30:
            active_alerts += 1

    return {
        "compliance_score": compliance_score,
        "compliance_status": compliance_status,

        "cto_status": cto_status,
        "cto_expiry_days": cto_expiry_days,

        "generated_reports": db.query(ComplianceReport).count(),

        "active_alerts": active_alerts
    }

# ==============================
# LIVE COMPLIANCE STATUS
# ==============================
@router.get("/live-status")
def get_live_status():

    return [
        {
            "parameter": "pH",
            "value": 7.2,
            "status": "Safe"
        },
        {
            "parameter": "TDS",
            "value": 480,
            "status": "Safe"
        },
        {
            "parameter": "COD",
            "value": 260,
            "status": "Warning"
        },
        {
            "parameter": "BOD",
            "value": 40,
            "status": "Critical"
        }
    ]


# ==============================
# COMPLIANCE TREND GRAPH
# ==============================
@router.get("/trends")
def get_dashboard_trends(
    db: Session = Depends(get_db)
):

    reports = (
        db.query(ExtractedReport)
        .order_by(ExtractedReport.id.asc())
        .all()
    )

    trend_data = []

    for report in reports:

        trend_data.append({
            "report_id": report.id,
            "score": report.compliance_score,
            "analysis_date": report.analysis_date
        })

    return trend_data

# ==============================
# GENERATED REPORTS
# ==============================


@router.get("/reports")
def get_reports(db: Session = Depends(get_db)):

    reports = (
        db.query(ComplianceReport)
        .order_by(ComplianceReport.generated_date.desc())
        .all()
    )

    response = []

    for report in reports:

        response.append({
            "id": report.id,
            "title": report.title,
            "report_type": report.report_type,
            "status": report.status,
            "generated_date": report.generated_date.strftime("%Y-%m-%d")
        })

    return response


@router.post("/generate-report")
def generate_report(db: Session = Depends(get_db)):

    user = db.query(User).order_by(User.id.desc()).first()

    if not user:
        return {
            "message": "No user found"
        }

    report = ComplianceReport(
        title="Monthly Compliance Report",
        report_type="Compliance",
        status="Generated",
        user_id=user.id
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "message": "Report generated successfully",

        "report": {
            "id": report.id,
            "title": report.title,
            "generated_date": report.generated_date
        }
    }

# ==============================
# RECENT ALERTS
# ==============================

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):

    alerts = []

    user = db.query(User).order_by(User.id.desc()).first()

    if not user:
        return []

    # CTO missing
    if not user.cto_number:
        alerts.append({
            "id": 1,
            "message": "CTO details not uploaded",
            "severity": "High"
        })

    # CTO expiry check
    if user.cto_expiry_date:

        today = date.today()

        days_left = (user.cto_expiry_date - today).days

        # expired
        if days_left < 0:

            alerts.append({
                "id": 2,
                "message": "CTO expired",
                "severity": "Critical"
            })

        # expiring soon
        elif days_left <= 30:

            alerts.append({
                "id": 3,
                "message": f"CTO expires in {days_left} days",
                "severity": "Warning"
            })

    return alerts