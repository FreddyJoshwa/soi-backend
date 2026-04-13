import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")


def send_otp_email(to_email: str, otp: str):
    subject = "Your OTP Code"
    body = f"""
    Hello,

    Your OTP is: {otp}

    This OTP will expire in 5 minutes.

    Thank you.
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Email send failed:", e)