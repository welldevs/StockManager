from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.entry import EntryModel
from app.schemas.entry import EntrySchema  # Agora a importação está correta
from app.services.entry_service import fetch_entry
from app.auth.jwt_bearer import JWTBearer  # 🔒 Proteção com JWT

router = APIRouter(
    prefix="/v1/entry",
    tags=["entry"],
    dependencies=[Depends(JWTBearer())]  # 🔐 Proteção nas rotas
)

@router.get("/", response_model=List[EntrySchema])
def get_entry(
    db: Session = Depends(get_db),
    page: int = Query(1, alias="page", ge=1),
    page_size: int = Query(10, alias="page_size", ge=1, le=100)
):
    entry_data = fetch_entry(db, page, page_size)

    # Converte para a estrutura Pydantic correta
    return [EntrySchema(**entry) for entry in entry_data] if entry_data else []
