from pydantic import BaseModel, ConfigDict
from typing import Literal, List
from datetime import datetime

class MovementsResponse(BaseModel):
    product_id: str
    movement_date: datetime
    movement: Literal["add", "subtract"]
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class MovementsListResponse(BaseModel):
    movements: List[MovementsResponse]