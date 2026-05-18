from pydantic import BaseModel, field_validator
from typing import Literal


class StockUpdate(BaseModel):
    product_id: str
    quantity: int
    operation: Literal["add", "subtract"]

    @field_validator("quantity")
    @classmethod
    def must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Must Be A Real Value")
        return v
