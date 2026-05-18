import uuid
import httpx

async def shoot_webhook(stock: int, name: str, threshold: int, product_id: str):
    
    url = "http://localhost:8000/webhook/"


    payload = {
            "name": name,
            "product_id": product_id,
            "threshold": threshold,
            "stock": stock,
            "id": str(uuid.uuid4())
    
    }
    

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url=url, json=payload)
            print(f"Successful Request. Status {response.status_code}")
        except httpx.ReadError as esx:
            print(f"An Error Ocours {esx}")
