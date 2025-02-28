import json
import redis.asyncio as redis
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from schemas.supplies import SuppliesSchema
from services.supplies_service import fetch_supplies
from auth.jwt_bearer import JWTBearer  # 🔐 Proteção JWT

# Configuração do Redis
redis_client = redis.Redis(host="redis_container", port=6379, db=0, decode_responses=True)

router = APIRouter(
    prefix="/v1/supplies",
    tags=["Supplies"],
    dependencies=[Depends(JWTBearer())]  # 🔐 Protegendo todas as rotas com JWT
)

@router.get("/", response_model=List[SuppliesSchema])
async def get_supplies(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    cache_key = f"Supplies:page:{page}:size:{page_size}"

    # 🔍 Verifica se os dados estão no cache do Redis
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)  # ✅ Retorna os dados do cache

    try:
        # 🔄 ✅ Adicionando `await` para chamar corretamente a função assíncrona
        supplies_data = await fetch_supplies(db, page, page_size)
        if not supplies_data:
            raise HTTPException(status_code=404, detail="Nenhum item de suprimentos encontrado.")

        # 🟢 Salva os dados no cache Redis por 5 minutos
        await redis_client.setex(cache_key, 300, json.dumps(supplies_data, default=str))

        return supplies_data  # ✅ Agora retorna a lista corretamente
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
