from fastapi import APIRouter, Depends, HTTPException
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

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, req.email, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {
        "sub": str(user.email),
        "user_id": str(user.id)
    }
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}