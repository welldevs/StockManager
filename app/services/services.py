import logging
from sqlalchemy.orm import Session
from sqlalchemy import text, exc
from datetime import datetime
from models.document import DocumentModel
from typing import List
from fastapi import HTTPException

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_invoices(db: Session, page: int, page_size: int) -> List[dict]:
    logger.info(f"Recebida solicitação para fetch_invoices - Página: {page}, Tamanho da Página: {page_size}")

    if page < 1:
        logger.warning("Número da página inválido (menor que 1)")
        raise HTTPException(status_code=400, detail="O número da página deve ser maior que 0")
    
    if page_size < 1:
        page_size = 10
    elif page_size > 100:
        page_size = 100

    # Detecta se o banco é SQLite
    if "sqlite" in str(db.bind.url):
        query = text(f"SELECT * FROM SM_FATURAMENTO_ERP LIMIT {page_size} OFFSET {(page - 1) * page_size}")
    else:
        query = text(f"SELECT * FROM hub.SM_FATURAMENTO_ERP OFFSET {(page - 1) * page_size} ROWS FETCH NEXT {page_size} ROWS ONLY")

    try:
        results = db.execute(query).fetchall()
        logger.info(f"Consulta SQL executada com sucesso - Retornados {len(results)} registros")
    except exc.SQLAlchemyError as e:
        logger.error(f"Erro ao consultar o banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")

    if not results:
        logger.warning("Nenhum registro encontrado para os parâmetros informados.")
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado para os parâmetros informados.")

    data = []
    for row in results:
        row_dict = {column: value for column, value in zip(DocumentModel.__annotations__.keys(), row)}
        if isinstance(row_dict.get("DTAFATURAMENTO"), datetime):
            row_dict["DTAFATURAMENTO"] = row_dict["DTAFATURAMENTO"].isoformat()
        if isinstance(row_dict.get("DTAINCLUSAO"), datetime):
            row_dict["DTAINCLUSAO"] = row_dict["DTAINCLUSAO"].isoformat()
        data.append(row_dict)

    logger.info("Retornando dados da API com sucesso.")
    return data
