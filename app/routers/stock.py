from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.stock import StockModel
from services.stock_service import fetch_stock

router = APIRouter(prefix="/v1/stock", tags=["Stock"])

@router.get("/", response_model=List[StockModel])
def get_stock(
    db: Session = Depends(get_db),
    page: int = Query(1, alias="page", ge=1),
    page_size: int = Query(10, alias="page_size", ge=1, le=100)
):
    return fetch_stock(db, page, page_size)
