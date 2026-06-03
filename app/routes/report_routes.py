from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from jinja2 import Environment, FileSystemLoader

from app.database import get_db
from app.models import User
from app.models import ExtractedReport
from app.models import AirReport

from playwright.sync_api import sync_playwright
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)

@router.get("/preview", response_class=HTMLResponse)
def preview_report(
    db: Session = Depends(get_db)
):

    # latest user
    user = (
        db.query(User)
        .order_by(User.id.desc())
        .first()
    )

    # latest water report
    water_report = (
        db.query(ExtractedReport)
        .order_by(ExtractedReport.id.desc())
        .first()
    )

    # latest air report
    air_report = (
        db.query(AirReport)
        .order_by(AirReport.id.desc())
        .first()
    )

    if not user:
        return "No user found"

    if not water_report:
        return "No water report found"

    if not air_report:
        return "No air report found"

    # overall score
    overall_score = int(
        (
            water_report.compliance_score +
            air_report.compliance_score
        ) / 2
    )

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template(
        "compliance_report.html"
    )

    html = template.render(

        company_name=user.company_name,
        industry_type=user.industry_type,
        reporting_period="June 2026",

        water_score=water_report.compliance_score,
        air_score=air_report.compliance_score,
        overall_score=overall_score,

        water_status=water_report.overall_status,
        air_status=air_report.overall_status,

        cto_number=user.cto_number,

        # Water values
        ph=water_report.ph,
        tds=water_report.tds,
        cod=water_report.cod,
        bod=water_report.bod,

        # Air values
        pm25=air_report.pm25,
        pm10=air_report.pm10,
        so2=air_report.so2,
        nox=air_report.nox,
        co=air_report.co,

        remarks=water_report.remarks
    )

    return html

@router.get("/generate-pdf")
def generate_pdf(
    db: Session = Depends(get_db)
):

    # latest user
    user = (
        db.query(User)
        .order_by(User.id.desc())
        .first()
    )

    # latest water report
    water_report = (
        db.query(ExtractedReport)
        .order_by(ExtractedReport.id.desc())
        .first()
    )

    # latest air report
    air_report = (
        db.query(AirReport)
        .order_by(AirReport.id.desc())
        .first()
    )

    if not user:
        return {
            "message": "No user found"
        }

    if not water_report:
        return {
            "message": "No water report found"
        }

    if not air_report:
        return {
            "message": "No air report found"
        }

    # overall score
    overall_score = int(
        (
            water_report.compliance_score +
            air_report.compliance_score
        ) / 2
    )

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template(
        "compliance_report.html"
    )

    html_content = template.render(

        company_name=user.company_name,
        industry_type=user.industry_type,
        reporting_period="June 2026",

        water_score=water_report.compliance_score,
        air_score=air_report.compliance_score,
        overall_score=overall_score,

        water_status=water_report.overall_status,
        air_status=air_report.overall_status,

        cto_number=user.cto_number,

        # Water values
        ph=water_report.ph,
        tds=water_report.tds,
        cod=water_report.cod,
        bod=water_report.bod,

        # Air values
        pm25=air_report.pm25,
        pm10=air_report.pm10,
        so2=air_report.so2,
        nox=air_report.nox,
        co=air_report.co,

        remarks=water_report.remarks
    )

    # create reports folder
    os.makedirs("reports", exist_ok=True)

    pdf_path = (
        f"reports/compliance_report_{user.id}.pdf"
    )

    # Generate PDF using Playwright
    with sync_playwright() as p:

        browser = p.chromium.launch()

        page = browser.new_page()

        page.set_content(
            html_content,
            wait_until="networkidle"
        )

        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True
        )

        browser.close()

    return FileResponse(
        path=pdf_path,
        filename="TNPCB_Compliance_Report.pdf",
        media_type="application/pdf"
    )