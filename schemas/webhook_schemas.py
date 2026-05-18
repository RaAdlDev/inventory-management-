from pydantic import BaseModel, ConfigDict

class ProductWebhook(BaseModel):
    name: str
    product_id: str
    threshold: int
    stock: int
    id: str 

    model_config = ConfigDict(from_attributes=True)
