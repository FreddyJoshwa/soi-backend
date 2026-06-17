from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from app.database import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Float, Text


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(
        String(120),
        unique=True,
        nullable=False,
        index=True
    )

    phone_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    company_name = Column(
        String(150),
        nullable=True
    )

    industry_type = Column(
        String(100),
        nullable=True
    )

    state = Column(
        String(100),
        nullable=True
    )

    district = Column(
        String(100),
        nullable=True
    )

    city = Column(
        String(100),
        nullable=True
    )

    address = Column(
        String(255),
        nullable=True
    )

    cto_available = Column(
        String(10),
        nullable=True
    )

    cto_number = Column(
        String(100),
        nullable=True
    )

    cto_issue_date = Column(
        Date,
        nullable=True
    )

    cto_expiry_date = Column(
        Date,
        nullable=True
    )

    is_verified = Column(
        Boolean,
        default=False
    )
class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), nullable=False, index=True)
    otp_code = Column(String(6), nullable=False)
    is_verified = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ComplianceReport(Base):
    __tablename__ = "compliance_reports"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    report_type = Column(String(100), nullable=False)

    status = Column(String(50), default="Generated")

    generated_date = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    document_type = Column(String(100))
    report_period = Column(String(50))

    file_name = Column(String(255))
    file_path = Column(String(500))

    upload_status = Column(String(50), default="Uploaded")

    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))

class ExtractedReport(Base):
    __tablename__ = "extracted_reports"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id"))

    company_name = Column(String(255))
    sample_type = Column(String(255))

    collection_date = Column(String(100))
    analysis_date = Column(String(100))

    ph = Column(Float)
    tds = Column(Float)
    cod = Column(Float)
    bod = Column(Float)

    overall_status = Column(String(100))

    remarks = Column(Text)

    compliance_score = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document")


class AirReport(Base):
    __tablename__ = "air_reports"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id"))

    company_name = Column(String(255))

    monitoring_date = Column(String(100))

    pm25 = Column(Float)
    pm10 = Column(Float)

    so2 = Column(Float)
    nox = Column(Float)
    co = Column(Float)

    overall_status = Column(String(100))

    remarks = Column(String(1000))

    compliance_score = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )