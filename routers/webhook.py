from fastapi import APIRouter, status, BackgroundTasks
from schemas.webhook_schemas import ProductWebhook
from database.connection import  LocalSession
from database.models import WebHooks


router = APIRouter(prefix="/webhook", tags=["WebHooks"])

def process_response(wh_id: str, name: str, threshold: int, stock: int, product_id:str):
    with LocalSession() as db:
        webhook = db.get(WebHooks, wh_id)
        if webhook is None:
            db.add(WebHooks(id = wh_id, 
                name = name, 
                threshold = threshold,
                stock = stock,
                product_id = product_id))
            db.commit()
        return True
    return True


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def get_webhook(response: ProductWebhook, background: BackgroundTasks):
    
    background.add_task(process_response, response.id,
                response.name,
                response.threshold, 
                response.stock,
                response.product_id)


    return {"status": "Delivered"}
