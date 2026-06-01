import os
import shutil

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Document, User

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.get("/")
def get_documents():
    return {
        "message": "Documents route working"
    }


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
            "message": "No user found. Please register first."
        }

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

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
        "message": "Document uploaded successfully",
        "document_id": document.id,
        "file_name": document.file_name
    }


@router.get("/all")
def get_all_documents(
    db: Session = Depends(get_db)
):
    documents = db.query(Document).all()

    result = []

    for doc in documents:
        result.append({
            "id": doc.id,
            "document_type": doc.document_type,
            "report_period": doc.report_period,
            "file_name": doc.file_name,
            "uploaded_at": doc.uploaded_at
        })

    return result