from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.document import DocumentModel
from services.services import fetch_invoices

router = APIRouter(prefix="/v1/invoices", tags=["Invoices"])

@router.get("/", response_model=List[DocumentModel])
def get_invoices(
    db: Session = Depends(get_db),
    page: int = Query(1, alias="page", ge=1),
    page_size: int = Query(10, alias="page_size", ge=1, le=100)
):
    query = text(f"SELECT * FROM hub.SM_FATURAMENTO_ERP OFFSET {(page - 1) * page_size} ROWS FETCH NEXT {page_size} ROWS ONLY")
    return fetch_invoices(db, query)