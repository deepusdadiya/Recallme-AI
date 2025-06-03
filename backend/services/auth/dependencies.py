from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from services.auth.token_service import decode_token
from alchemist.postgresql.functions import User
from alchemist.postgresql.resource import get_db
import os
from uuid import UUID
from starlette.status import HTTP_401_UNAUTHORIZED

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")  # Adjust if different
JWT_SECRET = os.getenv("JWT_SECRET")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("✅ Token extracted in get_current_user:", token)
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# JWT_SECRET = os.getenv("JWT_SECRET")

# def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
#         print("Decoded payload:", payload)
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
#         return UUID(user_id)
#     except JWTError:
#         raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate token")