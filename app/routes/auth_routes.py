from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, OTPVerification
from app.schemas import (
    SendOTPRequest,
    VerifyOTPRequest,
    UserRegister,
    UserLogin,
    TokenResponse,
)
from app.auth import hash_password, verify_password, create_access_token
from app.utils import generate_otp, get_otp_expiry
from app.email_utils import send_otp_email

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/send-otp")
def send_otp(data: SendOTPRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    db.query(OTPVerification).filter(OTPVerification.email == data.email).delete()
    db.commit()

    otp = generate_otp()

    otp_entry = OTPVerification(
        email=data.email,
        otp_code=otp,
        is_verified=False,
        expires_at=get_otp_expiry(5)
    )

    db.add(otp_entry)
    db.commit()

    send_otp_email(data.email, otp)

    return {
        "message": "OTP sent to email successfully"
    }


@router.post("/verify-otp")
def verify_otp(data: VerifyOTPRequest, db: Session = Depends(get_db)):
    otp_entry = (
        db.query(OTPVerification)
        .filter(OTPVerification.email == data.email)
        .order_by(OTPVerification.id.desc())
        .first()
    )

    if not otp_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP not found"
        )

    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP expired"
        )

    if otp_entry.otp_code != data.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    otp_entry.is_verified = True
    db.commit()

    return {"message": "OTP verified successfully"}


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    existing_phone = db.query(User).filter(User.phone_number == user_data.phone_number).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    verified_otp = (
        db.query(OTPVerification)
        .filter(
            OTPVerification.email == user_data.email,
            OTPVerification.is_verified == True
        )
        .order_by(OTPVerification.id.desc())
        .first()
    )

    if not verified_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify OTP before registering"
        )

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password=hash_password(user_data.password),

        company_name=user_data.company_name,
        industry_type=user_data.industry_type,
        city=user_data.city,
        district=user_data.district,
        state=user_data.state,
        address=user_data.address,

        role=user_data.role,
        production_type=user_data.production_type,
        water_source=user_data.water_source,
        etp_available=user_data.etp_available,

        cto_available=user_data.cto_available,
        cto_number=user_data.cto_number,
        cto_issue_date=user_data.cto_issue_date,
        cto_expiry_date=user_data.cto_expiry_date,

        is_verified=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.query(OTPVerification).filter(OTPVerification.email == user_data.email).delete()
    db.commit()

    token = create_access_token({"sub": str(new_user.id)})

    return {
        "message": "User registered successfully",
        "access_token": token,
        "token_type": "bearer",
        "user": new_user
    }


@router.post("/login", response_model=TokenResponse)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": str(user.id)})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }