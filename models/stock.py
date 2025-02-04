from pydantic import BaseModel
from typing import Optional

class StockModel(BaseModel):
    EMPRESAID: int
    PRODUTOID: int
    FORNECEDORID: int
    CATEGORIA: Optional[str]
    FAMILIAID: int
    QTDESTQUNITARIO: int
    PADRAOEMBCOMPRA: int
    QTDESTQEMBCOMPRA: float
    VLRCUSTOLIQUIDO: float
    CUSTOLIQUNITARIO: float
    DIASSEMVENDA: Optional[str]

    class Config:
        from_attributes = True
