from pydantic import BaseModel
from typing import Optional
from datetime import date

class InvoiceSchema(BaseModel):
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
    DTAFATURAMENTO: Optional[date]
    DTAINCLUSAO: Optional[date]
    USUINCLUSAO: Optional[str]
    SEQMOVTOESTQ: int

    class Config:
        from_attributes = True  # Permite conversão entre SQLAlchemy e Pydantic
