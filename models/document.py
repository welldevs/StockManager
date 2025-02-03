from pydantic import BaseModel
from typing import Optional

class DocumentModel(BaseModel):
    DOCUMENTOID: int
    DOCSERIEID: Optional[str]
    EMPRESAID: int
    CLIENTEID: int
    NROCARGA: int
    PRODUTOID: int
    CATEGORIA: Optional[str]
    FAMILIAID: int
    PADRAOEMBCOMPRA: int
    QTDEMBVENDA: int
    QUANTIDADE: int
    VLRITEMUNITARIOVENDA: float
    VLRITEMTOTALVENDA: float
    PRAZOPAGAMENTO: int
    DTAFATURAMENTO: Optional[str]
    DTAINCLUSAO: Optional[str]
    USUINCLUSAO: Optional[str]
    SEQMOVTOESTQ: int