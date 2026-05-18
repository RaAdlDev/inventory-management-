from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from core.settings import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from database.connection import get_db
from database.models import Users
from sqlalchemy.orm import Session
from sqlalchemy import select


oauth = OAuth2PasswordBearer(tokenUrl="user/login")
password_context = CryptContext(schemes=["bcrypt"])

def hash_password(plain):
    return password_context.hash(plain)

def verify_password(plain_password, data_password):
    return password_context.verify(plain_password, data_password)

def create_token(data: dict):
    to_encode = data.copy()
    time = datetime.now(timezone.utc) + timedelta(minutes= settings.token_duration)
    to_encode.update({"exp": time})
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)

def decode_token(db: Session = Depends(get_db), token = Depends(oauth)):

    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = data.get("sub")
        if not user_id:
            raise HTTPException(status_code=404, detail="User Not Found")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Not Allowed")
    

def verify_admin(db: Session = Depends(get_db), token = Depends(oauth)):
    first_admin = db.execute(select(Users)).first()
    if not first_admin:
        return True
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = data.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid Token")
        u = db.get(Users, user_id)
        if not u: 
            raise HTTPException(status_code=404, detail="User Not Found")
        if u.role != "admin":
            raise HTTPException(status_code=403, detail="You Don't Have Authorization")
        return True
    except JWTError:
        raise HTTPException(status_code=401, detail="Not Allowed")


