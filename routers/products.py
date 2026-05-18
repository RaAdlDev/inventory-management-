from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from database.connection import get_db
from core.security import decode_token, verify_admin
from schemas.products_schemas import Product, ProductUpdate, ProductListResponse, ProductResponse
from schemas.stock_schemas import StockUpdate
from services.products_services import new_product, get_products, transactions, find_product, delete_product, update_product, get_low, get_movements, search_movement
from typing import Optional
from sqlalchemy.orm import Session
from schemas.movements_schemas import MovementsListResponse

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=ProductListResponse)
async def see_products(name: Optional[str] = None, db: Session = Depends(get_db), current: str = Depends(decode_token)):
    if name:
        product = find_product(db, name)
        return {"products": product}
    products = get_products(db)
    return {"products": products}
    

@router.post("/add")
async def add_products(data: Product,db: Session= Depends(get_db), v_admin:bool = Depends(verify_admin)):
    verify = new_product(db, data)
    if verify is None:
        raise HTTPException(status_code=409, detail= "The Product Already Exists")
    return verify



@router.patch("/transaction")
async def add_stock(data: StockUpdate,  background: BackgroundTasks, db: Session = Depends(get_db), current: str = Depends(decode_token)):
    verify = transactions(db, data, background)
    if verify is None:
        raise HTTPException(status_code=400, detail="Please Check The Info")
    return {"stock": verify}

@router.get("/low_stock")
async def low_stock( db: Session = Depends(get_db), v_admin: bool = Depends(verify_admin)):
    return  get_low(db)


@router.delete("/delete/{id}")
async def out_product(id: str, db: Session = Depends(get_db),  v_admin: bool = Depends(verify_admin)):
    verify = delete_product(db, id)
    if verify is None:
        raise HTTPException(status_code=404, detail= "Product Not Found")
    return {"status": "successful request"}

@router.patch("/update/{id}", response_model=ProductResponse)
async def patch_product(id: str, data: ProductUpdate,  db: Session = Depends(get_db), v_admin: bool = Depends(verify_admin)):
    verify = update_product(db, id, data)
    if verify is None:
        raise HTTPException(status_code=404, detail= "Product Not Found")
    return verify

@router.get("/movements", response_model=MovementsListResponse)
async def movements(product_id: Optional[str] = None,  db: Session = Depends(get_db), v_admin: bool = Depends(verify_admin)):
    if product_id:
        return {"movements": search_movement(db, id)}
    return {"movements":get_movements(db) } 

    



