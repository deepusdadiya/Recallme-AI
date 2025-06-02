from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from services.auth.token_service import decode_token
from alchemist.postgresql.functions import User
from alchemist.postgresql.resource import get_db
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # Adjust if different

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_verified:
        raise HTTPException(status_code=401, detail="User not found or not verified")

    return user
