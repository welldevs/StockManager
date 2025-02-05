from pydantic import BaseModel
from typing import Optional
from datetime import date

class StockSchema(BaseModel):
    EMPRESAID: int
    PRODUTOID: int
    FORNECEDORID: Optional[int]
    CATEGORIA: Optional[str]
    FAMILIAID: Optional[int]
    QTDESTQUNITARIO: Optional[int]
    PADRAOEMBCOMPRA: Optional[int]
    QTDESTQEMBCOMPRA: Optional[float]
    VLRCUSTOLIQUIDO: Optional[float]
    CUSTOLIQUNITARIO: Optional[float]
    DIASSEMVENDA: Optional[str]

    class Config:
        from_attributes = True  # Permite conversão de SQLAlchemy para Pydantic
