from typing import Optional, Literal
from datetime import date
from pydantic import BaseModel, EmailStr, Field, model_validator


class SendOTPRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=6)

class UserRegister(BaseModel):

    full_name: str
    email: EmailStr
    phone_number: str

    password: str
    confirm_password: str

    company_name: str
    industry_type: str

    state: str
    district: str
    city: str

    address: str | None = None

    cto_available: str | None = None
    cto_number: str | None = None

    cto_issue_date: date | None = None
    cto_expiry_date: date | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: str
    company_name: Optional[str] = None
    role: Optional[str] = None
    is_verified: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: UserResponse