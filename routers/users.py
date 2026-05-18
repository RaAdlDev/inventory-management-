from fastapi import APIRouter, Depends, HTTPException
from services.users_services import register, login, promote_user, delete_u, find_employee, get_employees
from schemas.user_schemas import User, UserListResponse, UserResponse
from database.connection import get_db
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_admin
from typing import Optional
from sqlalchemy.orm import Session


router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/register")
async def user_register(data: User, db: Session = Depends(get_db), v_admin: bool = Depends(verify_admin)):
    status =  register(db, data)
    if status is None:
        raise HTTPException(status_code=409, detail="Username Already Exists")
    return {"status": "Successful Request"}


@router.post("/login")
async def u_login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    status = login(db, form)
    if status is None:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return status

@router.get("/employees", response_model=UserListResponse)
async def employees_database(search: Optional[str] = None, v_admin: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    if search:
        employee = find_employee(db, search)
        return {"users": employee}
    employees =  get_employees(db)
    return {"users": employees}

@router.patch("/promote/{id}", response_model=UserResponse)
async def promote_u(id:str, v_admin: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    status = promote_user(db, id)
    if status is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return status

@router.delete("/delete/{id}")
async def user_out(id:str, v_admin: bool = Depends(verify_admin), db: Session = Depends(get_db)):
    status = delete_u(db, id)
    if status is None:
        raise HTTPException(status_code=404, detail="User Not Found")


    return {"status": "Successful Request"}