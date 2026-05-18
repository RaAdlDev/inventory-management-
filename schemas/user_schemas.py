from pydantic import BaseModel, ConfigDict, field_validator
import re
from typing import List

class User(BaseModel):
    username: str
    phone: str
    password: str
    

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("The Password Must Be At Least 8 Characters Length")
        return v
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r"^\+?[\d\s\-]{7,15}$", v):
            raise ValueError("Número de teléfono inválido")
        return v

class UserResponse(BaseModel):
    user_id: str
    username: str
    phone: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class UserListResponse(BaseModel):
    users: List[UserResponse]


