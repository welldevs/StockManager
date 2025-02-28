import json
import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from services.invoice_service import fetch_invoices  # 🔄 Importa o serviço
from schemas.invoice import InvoiceSchema
from typing import List
from auth.jwt_bearer import JWTBearer  # 🔐 Proteção JWT

# Configuração do Redis
redis_client = redis.Redis(host="redis_container", port=6379, db=0, decode_responses=True)

# Definição do Router
router = APIRouter(
    tags=["Invoices"],
    dependencies=[Depends(JWTBearer())]  # 🔐 Protegendo com JWT
)

@router.get("/v1/invoice", response_model=List[InvoiceSchema])
async def read_invoices(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    cache_key = f"invoice:page:{page}:size:{page_size}"

    # 🔍 Verifica se os dados estão no cache do Redis
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)  # ✅ Garante que o JSON seja carregado corretamente

    try:
        # 🔄 Chama o serviço para buscar no banco
        invoices = await fetch_invoices(db, page, page_size)
        if not invoices:
            raise HTTPException(status_code=404, detail="Nenhuma fatura encontrada.")

        # ✅ Converte os objetos Pydantic para dicionários serializáveis
        serialized_data = [invoice.dict() for invoice in invoices]

        # 🟢 Salva os dados no cache Redis por 5 minutos (JSON formatado corretamente)
        await redis_client.setex(cache_key, 300, json.dumps(serialized_data, default=str))

        return invoices
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
