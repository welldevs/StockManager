import logging
from sqlalchemy.orm import Session
from sqlalchemy import text, exc
from typing import List
from fastapi import HTTPException
from models.stock import StockModel

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_stock(db: Session, page: int, page_size: int) -> List[dict]:
    logger.info(f"Recebida solicitação para fetch_stock - Página: {page}, Tamanho da Página: {page_size}")
    
    if page < 1:
        logger.warning("Número da página inválido (menor que 1)")
        raise HTTPException(status_code=400, detail="O número da página deve ser maior que 0")
    if page_size < 1:
        page_size = 10
    elif page_size > 100:
        page_size = 100

    # Ajustando query para diferentes bancos (SQLite vs Oracle)
    if "sqlite" in str(db.bind.url):
        query = text(f"SELECT * FROM hub.sm_estoque_erp LIMIT {page_size} OFFSET {(page - 1) * page_size}")
    else:
        query = text(f"SELECT * FROM hub.sm_estoque_erp OFFSET {(page - 1) * page_size} ROWS FETCH NEXT {page_size} ROWS ONLY")
    
    try:
        results = db.execute(query).fetchall()
        logger.info(f"Consulta SQL executada com sucesso - Retornados {len(results)} registros")
    except exc.SQLAlchemyError as e:
        logger.error(f"Erro ao consultar o banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")
    
    if not results:
        logger.warning("Nenhum registro encontrado para os parâmetros informados.")
        return []

    data = []
    for row in results:
        row_dict = {column: value for column, value in zip(StockModel.__annotations__.keys(), row)}
        data.append(row_dict)

    logger.info("Retornando dados de estoque com sucesso.")
    return data
