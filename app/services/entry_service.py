import logging
from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from typing import List
from fastapi import HTTPException
from app.models.entry import EntryModel  # Modelo correto

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_entry(db: Session, page: int, page_size: int) -> List[dict]:
    logger.info(f"Recebida solicitação para fetch_entry - Página: {page}, Tamanho da Página: {page_size}")

    # Verificação de parâmetros de entrada
    if page < 1:
        logger.warning("Número da página inválido (menor que 1)")
        raise HTTPException(status_code=400, detail="O número da página deve ser maior que 0")

    page_size = max(1, min(page_size, 100))  # Garante que page_size esteja entre 1 e 100
    offset = (page - 1) * page_size

    try:
        # Construindo a consulta com `select()`
        query = select(EntryModel).offset(offset).limit(page_size)
        results = db.execute(query).scalars().all()

        logger.info(f"Consulta executada com sucesso - Retornados {len(results)} registros")
    except exc.SQLAlchemyError as e:
        logger.error(f"Erro ao consultar o banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")

    if not results:
        logger.warning("Nenhum registro encontrado para os parâmetros informados.")
        return []

    # Converter resultados para dicionário
    data = [entry.__dict__ for entry in results]
    for item in data:
        item.pop("_sa_instance_state", None)  # Remove metadado do SQLAlchemy

    logger.info("Retornando dados de entrada com sucesso.")
    return data
