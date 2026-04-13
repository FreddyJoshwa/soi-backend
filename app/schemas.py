from typing import Optional, Literal
from datetime import date
from pydantic import BaseModel, EmailStr, Field, model_validator


class SendOTPRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=6)


class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)
    confirm_password: str

    company_name: str
    industry_type: str
    city: str
    district: str
    state: str
    address: Optional[str] = None

    role: str
    production_type: str
    water_source: str
    etp_available: str

    # CTO fields
    cto_available: Literal["Yes", "No"]
    cto_number: Optional[str] = None
    cto_issue_date: Optional[date] = None
    cto_expiry_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_fields(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        if self.cto_available == "Yes":
            if not self.cto_number or not self.cto_number.strip():
                raise ValueError("CTO number is required when CTO is available")
            if not self.cto_issue_date:
                raise ValueError("CTO issue date is required when CTO is available")
            if not self.cto_expiry_date:
                raise ValueError("CTO expiry date is required when CTO is available")
            if self.cto_expiry_date <= self.cto_issue_date:
                raise ValueError("CTO expiry date must be after CTO issue date")

        return self


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