from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from app.database import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    company_name = Column(String(150), nullable=True)
    industry_type = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)

    role = Column(String(50), nullable=True)
    production_type = Column(String(100), nullable=True)
    water_source = Column(String(100), nullable=True)
    etp_available = Column(String(10), nullable=True)

    # CTO fields
    cto_available = Column(String(10), nullable=True)
    cto_number = Column(String(100), nullable=True)
    cto_issue_date = Column(Date, nullable=True)
    cto_expiry_date = Column(Date, nullable=True)

    is_verified = Column(Boolean, default=False)


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

