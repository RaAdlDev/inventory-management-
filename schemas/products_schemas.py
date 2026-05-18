from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from decimal import Decimal

class Product(BaseModel):
    name: str
    description: Optional[str] = None
    unit_price: Decimal
    threshold: Optional[int] = None

    @field_validator("unit_price")
    @classmethod
    def verify_price_positive(cls, v):
        if v <= 0:
            raise ValueError("Must Be A Real Value")
        return v
    @field_validator("threshold")
    @classmethod
    def verify_threshold_positive(cls, v):
        if v <= 0:
            raise ValueError("Must Be A Real Value")
        return v


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[Decimal] = None
    threshold: Optional[int] = None
    

    @field_validator("threshold")
    @classmethod
    def verify_positive(cls, v):
        if v <= 0:
            raise ValueError("Must Be A Real Value")
        return v
    @field_validator("unit_price")
    @classmethod
    def verify_unit_pricepositive(cls, v):
        if v is None:
            return v
        if v <= 0:
            raise ValueError("Must Be A Real Value")
        return v
    
class ProductResponse(BaseModel):
    name: str
    description: Optional[str]
    unit_price: Decimal
    threshold: int
    product_id: str

    model_config =  ConfigDict(from_attributes=True)

class ProductListResponse(BaseModel):
    products: List[ProductResponse]



