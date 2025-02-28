import logging
import json
import redis.asyncio as redis
from sqlalchemy.orm import Session
from sqlalchemy import text, exc
from datetime import datetime, date
from typing import List
from fastapi import HTTPException
from schemas.invoice import InvoiceSchema

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configuração do Redis
redis_client = redis.Redis(
    host="redis_container",
    port=6379,
    db=0,
    decode_responses=True
)

CACHE_EXPIRE_TIME = 300  # 5 minutos

async def fetch_invoices(db: Session, page: int, page_size: int) -> List[InvoiceSchema]:
    logger.info(f"Recebida solicitação para fetch_invoices - Página: {page}, Tamanho da Página: {page_size}")

    if page < 1:
        raise HTTPException(status_code=400, detail="O número da página deve ser maior que 0")
    
    if page_size < 1:
        page_size = 10
    elif page_size > 100:
        page_size = 100

    cache_key = f"invoice:page:{page}:size:{page_size}"

    # 🟢 Tenta recuperar do cache
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        logger.info(f"Dados carregados do cache para a página {page}, tamanho {page_size}")
        cached_data = json.loads(cached_data)

        # Convertendo chaves para MAIÚSCULAS e datas para formato correto
        formatted_data = []
        for item in cached_data:
            item = {k.upper(): v for k, v in item.items()}
            if "DTAFATURAMENTO" in item and item["DTAFATURAMENTO"]:
                item["DTAFATURAMENTO"] = date.fromisoformat(item["DTAFATURAMENTO"][:10])  # Mantém apenas a data
            if "DTAINCLUSAO" in item and item["DTAINCLUSAO"]:
                item["DTAINCLUSAO"] = date.fromisoformat(item["DTAINCLUSAO"][:10])  # Mantém apenas a data
            formatted_data.append(item)

        return [InvoiceSchema(**item) for item in formatted_data]

    # 🟢 Consulta ao banco
    query = text(f"SELECT * FROM hub.SM_FATURAMENTO_ERP OFFSET {(page - 1) * page_size} ROWS FETCH NEXT {page_size} ROWS ONLY")

    try:
        result = db.execute(query)
        rows = result.fetchall()
        column_names = [col.upper() for col in result.keys()]
        logger.info(f"Consulta SQL executada com sucesso - Retornados {len(rows)} registros")
    except exc.SQLAlchemyError as e:
        logger.error(f"Erro ao consultar o banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")

    if not rows:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado.")

    # 🟢 Padronizando os dados para JSON serializável
    data = []
    for row in rows:
        row_dict = dict(zip(column_names, row))

        # Convertendo DATETIME para DATE
        if isinstance(row_dict.get("DTAFATURAMENTO"), datetime):
            row_dict["DTAFATURAMENTO"] = row_dict["DTAFATURAMENTO"].date()  # Apenas a data
        if isinstance(row_dict.get("DTAINCLUSAO"), datetime):
            row_dict["DTAINCLUSAO"] = row_dict["DTAINCLUSAO"].date()  # Apenas a data

        data.append(row_dict)

    # 🟢 Salva no Redis com JSON formatado corretamente
    await redis_client.setex(cache_key, CACHE_EXPIRE_TIME, json.dumps(data, default=str))

    logger.info(f"Dados armazenados no cache para a página {page}, tamanho {page_size}")

    return [InvoiceSchema(**item) for item in data]  # Retorna objetos Pydantic
