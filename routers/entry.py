import json
import redis.asyncio as redis
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from schemas.entry import EntrySchema
from services.entry_service import fetch_entry
from auth.jwt_bearer import JWTBearer  # 🔐 Proteção JWT

# Configuração do Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

router = APIRouter(
    prefix="/v1/entry",
    tags=["Entry"],
    dependencies=[Depends(JWTBearer())]  # 🔐 Protegendo todas as rotas com JWT
)

@router.get("/", response_model=List[EntrySchema])
async def get_entry(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    cache_key = f"entry:page:{page}:size:{page_size}"

    # 🔍 Verifica se os dados estão no cache do Redis
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)  # ✅ Converte JSON armazenado para lista de dicionários

    try:
        # 🔄 Chama o serviço para buscar no banco
        entry_data = fetch_entry(db, page, page_size)
        if not entry_data:
            raise HTTPException(status_code=404, detail="Nenhuma entrada encontrada.")

        # ✅ Converte objetos Pydantic para dicionários antes de salvar no Redis
        serialized_data = [entry.dict() for entry in entry_data]

        # 🟢 Salva os dados no cache Redis por 5 minutos
        await redis_client.setex(cache_key, 300, json.dumps(serialized_data, default=str))

        return entry_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
