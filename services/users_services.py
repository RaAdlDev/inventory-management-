from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from database.models import Users
from schemas.user_schemas import User
from core.security import hash_password, verify_password, create_token
from fastapi.security import OAuth2PasswordRequestForm


def register(db: Session, data: User):
    rol = "employee"
    show = db.execute(select(Users).where(or_(Users.username == data.username, Users.phone == data.phone))).all()
    admin = db.execute(select(Users)).all()
    if not admin:
        rol = "admin"
    if not show:
        db.add(Users(role = rol, username = data.username, phone = data.phone, password = hash_password(data.password)))
        db.commit()
        return True
    return None


def login(db: Session, form: OAuth2PasswordRequestForm):
    data = db.execute(select(Users).where(Users.username == form.username)).scalar_one_or_none()
    if data:
        if verify_password(form.password, data.password):
            return {"token":create_token({"sub": data.user_id}), "token_type": "bearer"}
        return None
    return None

def get_employees(db: Session):
    employees = db.execute(select(Users).where(Users.role != "admin")).scalars().all()
    return employees

def find_employee(db: Session, search: str):
    employee = db.execute(select(Users).where(Users.username.ilike(f"%{search}%"), Users.role == "employee")).scalars().all()
    return employee

def delete_u(db: Session, user_id:str):
    out = db.get(Users, user_id)
    if not out:
        return None
    db.delete(out)
    db.commit()
    return True
    
def promote_user(db: Session, user_id: str):
    user = db.get(Users, user_id)
    if not user:
        return None
    if user.role == "admin":
        return None
    user.role = "admin"
    db.commit()
    db.refresh(user)
    return user
