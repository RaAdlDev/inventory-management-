from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped, relationship
import uuid
from sqlalchemy import ForeignKey, Numeric, Enum
from typing import Optional, List, Literal
from decimal import Decimal
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass


class WebHooks(Base):
    __tablename__ = "webhooks"
    id: Mapped[str] = mapped_column(primary_key=True, default= lambda: str(uuid.uuid4()))
    name: Mapped[str] 
    product_id: Mapped[str] = mapped_column(ForeignKey("products.product_id", ondelete="CASCADE"))
    threshold: Mapped[int]
    stock: Mapped[int]


class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[str] = mapped_column(primary_key= True, default=lambda: str(uuid.uuid4()))
    role: Mapped[str] = mapped_column(default="employee")
    username: Mapped[str] = mapped_column(unique=True) 
    phone: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] 
    

class Products(Base):
    __tablename__ = "products"
    product_id: Mapped[str] = mapped_column(primary_key= True, default=lambda: str(uuid.uuid4()))
    threshold: Mapped[int] = mapped_column(default = 0)
    name: Mapped[str] = mapped_column(unique=True)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[Optional[str]]
    

    stock: Mapped["Stock"] = relationship(back_populates="product", uselist=False,  cascade="all, delete-orphan")

class Stock(Base):
    __tablename__ = "stock"
    product_id: Mapped[str] = mapped_column(ForeignKey("products.product_id", ondelete="CASCADE"), primary_key=True)
    stock: Mapped[int] 

    product: Mapped["Products"] = relationship(back_populates="stock")
    transactions: Mapped[List["Transactions"]] = relationship(back_populates="product_stock")

class Transactions(Base):
    __tablename__ = "transactions"
    transactions_id: Mapped[str] = mapped_column(primary_key= True, default=lambda: str(uuid.uuid4()))
    product_id: Mapped[str] = mapped_column(ForeignKey("stock.product_id", ondelete="CASCADE"))
    movement_date: Mapped[datetime] = mapped_column(default= datetime.now(timezone.utc))
    movement: Mapped[Literal["add", "subtract"]] =  mapped_column(
        Enum("add", "subtract", name="movement_types"))
    quantity: Mapped[int]

    product_stock: Mapped[Stock] = relationship(back_populates="transactions")
    



