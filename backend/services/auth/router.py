from fastapi import APIRouter, Depends, HTTPException, Form, Body
from sqlalchemy.orm import Session
from alchemist.postgresql.resource import get_db
from .schema import SignupRequest, OTPVerifyRequest, LoginRequest
from .service import create_user, verify_user_otp, authenticate_user
from services.auth.token_service import create_access_token

router = APIRouter()

@router.post("/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    create_user(db, req.email, req.password)
    return {"status": "OTP sent to your email"}

@router.post("/verify")
def verify(req: OTPVerifyRequest, db: Session = Depends(get_db)):
    ok, msg = verify_user_otp(db, req.email, req.otp)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "Email verified successfully"}

from fastapi import APIRouter, Depends, Request, HTTPException, Form
from sqlalchemy.orm import Session
from alchemist.postgresql.resource import get_db
from services.auth.token_service import create_access_token

router = APIRouter()

@router.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db),
    form_email: str = Form(None),
    form_password: str = Form(None)
):
    try:
        json_data = await request.json()
        print("Received JSON data:", json_data)
        email = json_data.get("email")
        password = json_data.get("password")
    except Exception:
        email = form_email
        password = form_password

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "sub": user.email,
        "user_id": str(user.id)
    }
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}


from fastapi.security import OAuth2PasswordRequestForm

@router.post("/token")
def login_with_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "sub": user.email,
        "user_id": str(user.id)
    }
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}