import random
from datetime import datetime, timedelta


def generate_otp() -> str:
    return str(random.randint(1000, 9999))


def get_otp_expiry(minutes: int = 5) -> datetime:
    return datetime.utcnow() + timedelta(minutes=minutes)