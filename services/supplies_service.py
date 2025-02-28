import json
import logging
import orjson
import redis.asyncio as redis
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from fastapi import HTTPException
from schemas.supplies import SuppliesSchema
from models.supplies import SuppliesModel  # ✅ Importando a Model correta

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configuração do Redis
redis_client = redis.Redis(host="redis_container", port=6379, db=0, decode_responses=True)

async def fetch_supplies(db: Session, page: int, page_size: int) -> List[SuppliesSchema]:
    """Consulta os suprimentos no banco de dados e armazena no cache Redis."""

    logger.info(f"Recebida solicitação para fetch_supplies - Página: {page}, Tamanho da Página: {page_size}")

    if page < 1:
        raise HTTPException(status_code=400, detail="O número da página deve ser maior que 0")
    if page_size < 1:
        page_size = 10
    elif page_size > 100:
        page_size = 100

    cache_key = f"supplies:page:{page}:size:{page_size}"  # 🔹 Define a chave do cache Redis

    # 🔍 Verifica se os dados já estão no Redis antes de consultar o banco
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        logger.info("🔄 Dados carregados do cache Redis")
        return json.loads(cached_data)

    try:
        # 🔄 Consulta utilizando a Model SQLAlchemy (ORM)
        offset = (page - 1) * page_size
        supplies_data = db.query(SuppliesModel).offset(offset).limit(page_size).all()
        
        if not supplies_data:
            logger.warning("Nenhum registro encontrado para os parâmetros informados.")
            return []

        # ✅ Converte os dados para `SuppliesSchema`
        serialized_data = [SuppliesSchema.from_orm(item).model_dump() for item in supplies_data]

        # 🟢 Salva os dados no cache Redis por 5 minutos
        await redis_client.setex(cache_key, 300, orjson.dumps(serialized_data).decode("utf-8"))
        logger.info("🟢 Dados de suprimentos armazenados no cache Redis")

        return serialized_data

    except SQLAlchemyError as e:
        logger.error(f"❌ Erro ao consultar o banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")

    except Exception as e:
        logger.error(f"❌ Erro inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
