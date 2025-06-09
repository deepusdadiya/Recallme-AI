import bcrypt, uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from alchemist.postgresql.functions import User
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

RESEND_API_KEY= os.getenv("RESEND_API_KEY")
RESEND_FROM= os.getenv("RESEND_FROM")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def generate_otp() -> str:
    return str(uuid.uuid4().int)[:6]

def send_otp_email(to_email: str, otp: str):
    try:
        response = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": RESEND_FROM,
                "to": [to_email],
                "subject": "Your Recallme-AI OTP",
                "html": f"<p>Your OTP is <strong>{otp}</strong></p>"
            },
            timeout=10.0,
            verify=False
        )
        print(f"[DEBUG] Resend API status: {response.status_code}")
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Resend email sending failed: {e}")
        raise

def create_user(db: Session, email: str, password: str):
    hashed_pw = hash_password(password)
    otp = generate_otp()
    expiry = datetime.now() + timedelta(minutes=10)

    user = User(
        email=email,
        hashed_password=hashed_pw,
        otp_code=otp,
        otp_expiry=expiry,
        is_verified=False
    )
    db.add(user)
    db.commit()
    send_otp_email(email, otp)
    return user

def verify_user_otp(db: Session, email: str, otp: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False, "User not found"
    if user.otp_code != otp:
        return False, "Incorrect OTP"
    if datetime.utcnow() > user.otp_expiry:
        return False, "OTP expired"

    user.is_verified = True
    user.otp_code = None
    db.commit()
    return True, "Verified"

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_verified:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user