from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.database import get_db
from models.document import DocumentModel
from services.services import fetch_invoices
from typing import List

router = APIRouter(prefix="/v1/invoices", tags=["Invoices"])

@router.get("/", response_model=List[DocumentModel])
def get_invoices(
    db: Session = Depends(get_db),
    page: int = Query(1, alias="page", ge=1),
    page_size: int = Query(10, alias="page_size", ge=1, le=100)
):
    return fetch_invoices(db, page, page_size)
