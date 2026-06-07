import os
import shutil

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Document, User

from app.pdf_utils import extract_text_from_pdf

from app.extractors.water_report_extractor import (
    extract_water_report_data
)

from app.extractors.air_report_extractor import (
    extract_air_report_data
)

from app.models import ExtractedReport
from app.models import AirReport

from app.compliance_engine import (
    calculate_compliance_score
)

from app.air_compliance_engine import (
    calculate_air_compliance_score
)

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================
# TEST ROUTE
# =========================

@router.get("/")
def get_documents():

    return {
        "message": "Documents route working"
    }


# =========================
# UPLOAD DOCUMENT
# =========================

@router.post("/upload")
def upload_document(

    document_type: str = Form(...),

    report_period: str = Form(...),

    file: UploadFile = File(...),

    db: Session = Depends(get_db)

):

    user = db.query(User).first()

    if not user:

        return {
            "message":
            "No user found. Please register first."
        }

    file_path = os.path.join(

        UPLOAD_FOLDER,

        file.filename

    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    document = Document(

        document_type=document_type,

        report_period=report_period,

        file_name=file.filename,

        file_path=file_path,

        user_id=user.id

    )

    db.add(document)

    db.commit()

    db.refresh(document)

    return {

        "message":
        "Document uploaded successfully",

        "document_id":
        document.id,

        "file_name":
        document.file_name
    }


# =========================
# GET ALL DOCUMENTS
# =========================

@router.get("/all")
def get_all_documents(

    db: Session = Depends(get_db)

):

    documents = db.query(Document).all()

    result = []

    for doc in documents:

        result.append({

            "id":
            doc.id,

            "document_type":
            doc.document_type,

            "report_period":
            doc.report_period,

            "file_name":
            doc.file_name,

            "uploaded_at":
            doc.uploaded_at

        })

    return result


# =========================
# EXTRACT PDF TEXT
# =========================

@router.get("/extract/{document_id}")
def extract_document_text(

    document_id: int,

    db: Session = Depends(get_db)

):

    document = (

        db.query(Document)

        .filter(
            Document.id == document_id
        )

        .first()

    )

    if not document:

        return {
            "message":
            "Document not found"
        }

    text = extract_text_from_pdf(
        document.file_path
    )

    return {

        "document_id":
        document.id,

        "file_name":
        document.file_name,

        "extracted_text":
        text
    }


# =========================
# ANALYZE DOCUMENT
# =========================

@router.get("/analyze/{document_id}")
def analyze_document(

    document_id: int,

    db: Session = Depends(get_db)

):

    document = (

        db.query(Document)

        .filter(
            Document.id == document_id
        )

        .first()

    )

    if not document:

        return {
            "message":
            "Document not found"
        }

    text = extract_text_from_pdf(
        document.file_path
    )

    doc_type = (
        document.document_type.lower()
    )

    # =========================
    # WATER REPORT
    # =========================

    if doc_type == "water report":

        extracted_data = (
            extract_water_report_data(text)
        )

        compliance = (
            calculate_compliance_score(
                extracted_data
            )
        )

        # SAVE WATER REPORT

        report = ExtractedReport(

            document_id=document.id,

            company_name=
            extracted_data["company_name"],

            sample_type=
            extracted_data["sample_type"],

            collection_date=
            extracted_data["collection_date"],

            analysis_date=
            extracted_data["analysis_date"],

            ph=
            extracted_data["ph"],

            tds=
            extracted_data["tds"],

            cod=
            extracted_data["cod"],

            bod=
            extracted_data["bod"],

            overall_status=
            extracted_data["overall_status"],

            remarks=
            extracted_data["remarks"],

            compliance_score=
            compliance["score"]

        )

        db.add(report)

        db.commit()

        db.refresh(report)

        return {

            "document_id":
            document.id,

            "document_type":
            document.document_type,

            "file_name":
            document.file_name,

            "saved_report_id":
            report.id,

            "analysis":
            extracted_data,

            "compliance": {

                "score":
                compliance["score"],

                "alerts":
                compliance["alerts"]
            }
        }

    # =========================
    # AIR REPORT
    # =========================

    elif doc_type == "air report":

        extracted_data = (
            extract_air_report_data(text)
        )

        compliance = (
            calculate_air_compliance_score(
                extracted_data
            )
        )

        air_report = AirReport(

            document_id=document.id,

            company_name=
            extracted_data["company_name"],

            monitoring_date=
            extracted_data["monitoring_date"],

            pm25=
            extracted_data["pm25"],

            pm10=
            extracted_data["pm10"],

            so2=
            extracted_data["so2"],

            nox=
            extracted_data["nox"],

            co=
            extracted_data["co"],

            overall_status=
            extracted_data["overall_status"],

            remarks=
            extracted_data["remarks"],

            compliance_score=
            compliance["score"]

        )

        db.add(air_report)

        db.commit()

        db.refresh(air_report)

        return {

            "document_id":
            document.id,

            "document_type":
            document.document_type,

            "file_name":
            document.file_name,

            "saved_air_report_id":
            air_report.id,

            "analysis":
            extracted_data,

            "compliance": {

                "score":
                compliance["score"],

                "alerts":
                compliance["alerts"]
            }
        }

    # =========================
    # UNSUPPORTED
    # =========================

    else:

        return {

            "message":
            f"Unsupported report type: {document.document_type}"

        }