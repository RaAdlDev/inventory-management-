from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.products_schemas import Product, ProductUpdate
from schemas.stock_schemas import StockUpdate
from database.models import Products, Stock, Transactions
from services.webhook_services import shoot_webhook
from fastapi import BackgroundTasks

def new_product(db: Session, data: Product):
    verify = db.scalar(select(Products).where(Products.name == data.name))
    if verify is None:
        new = Products(name = data.name, description = data.description, unit_price = data.unit_price, threshold = data.threshold)
        db.add(new)
        db.flush()
        n_stock = Stock(product_id = new.product_id, stock = 0)
        db.add(n_stock)
        db.commit()
        db.refresh(new)
        return new
    return None

def get_products(db: Session):
    products =  db.execute(select(Products)).scalars().all()
    return products


def transactions(db: Session, data: StockUpdate, background:BackgroundTasks):
    stock = db.get(Stock, data.product_id)
    if stock:
        if data.operation == "add":
            stock.stock += data.quantity
        if data.operation == "subtract":
            if  stock.stock - data.quantity < 0:
                return None
            stock.stock -= data.quantity
        db.add(Transactions(product_id = data.product_id,
                movement = data.operation,
                quantity = data.quantity,
                ))
        db.commit()
        db.refresh(stock)
        product = db.get(Products, data.product_id)
        if stock.stock < product.threshold:
            background.add_task(shoot_webhook, stock.stock, product.name, product.threshold, product.product_id)
        return stock.stock
    return None

def find_product(db: Session, search:str):
    products = db.execute(select(Products).where(Products.name.ilike(f"%{search}%"))).scalars().all()
    return products

def delete_product(db: Session, p_id: str):
    out = db.get(Products, p_id)
    if out:
        db.delete(out)
        db.commit()
        return True
    return None

def update_product(db: Session, p_id: str, data: ProductUpdate):
    product = db.get(Products, p_id)
    if product:
        if data.name is not None:
            product.name = data.name
        if data.description is not None:
            product.description = data.description
        if data.unit_price is not None:
            product.unit_price = data.unit_price
        if data.threshold is not None:
            product.threshold = data.threshold
        db.commit()
        db.refresh(product)
        return product
    return None

def get_low(db: Session):
    low_stock = db.execute(select(Products).join(Stock, Products.product_id == Stock.product_id )
                .where(Products.threshold > Stock.stock)).scalars().all()
    return {"Products": [{"Product": p.name, "Stock": p.stock, "Threshold": p.threshold} for p in low_stock]}

def get_movements(db: Session):
    movements = db.execute(select(Transactions)).scalars().all()
    return movements

def search_movement(db: Session, product_id: str):
    movements = db.execute(select(Transactions).where(Transactions.product_id == product_id)).scalars().all()
    return movements



