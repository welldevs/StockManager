from pydantic import BaseModel
from typing import Optional
from datetime import date

class EntrySchema(BaseModel):
    DOCUMENTO: int
    DOCSERIEID: Optional[str]
    CGO: Optional[int]
    FORNECEDORID: Optional[int]
    NOMERAZAO: Optional[str]
    EMPRESAID: Optional[int]
    SEQNF: Optional[int]
    DATAEMISSAO: Optional[date]
    DATAENTRADA: Optional[date]
    CATEGORIA: Optional[str]
    PRODUTOID: Optional[int]
    FAMILIAID: Optional[int]
    PADRAOEMBCOMPRA: Optional[str]
    QTDEMBALAGEM: Optional[int]
    EMBALAGEM: Optional[str]
    QTDSOLICITADA: Optional[int]
    QTDUNITARIO: Optional[int]
    VLRUNID: Optional[str]
    VALORITEM: Optional[float]
    SEQMOVTOESTQ: Optional[int]
    PRAZOFORNECEDOR: Optional[int]

    class Config:
        from_attributes = True  # Permite conversão entre SQLAlchemy e Pydantic
