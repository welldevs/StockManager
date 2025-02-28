from pydantic import BaseModel
from typing import Optional
from datetime import date

class SuppliesSchema(BaseModel):  # Renomeado para SuppliesSchema
    PEDIDOID: Optional[int]
    NROEMPRESA: Optional[int]
    IDFORNECEDOR: Optional[int]
    RAZAOFORNECEDOR: Optional[str]
    IDCOMPRADOR: Optional[int]
    COMPRADOR: Optional[str]
    SITUACAOPED: Optional[str]
    DTAEMISSAO: Optional[date]
    DTARECEBTO: Optional[date]
    PZOPAGAMENTO: Optional[str]
    VLRTOTPEDIDO: Optional[float]
    VLRTOTRECEBIDO: Optional[float]
    SEQNROPEDIDOSUP: Optional[int]
    SEQPRODUTO: Optional[int]
    DESCCOMPLETA: Optional[str]
    QTDTOTRECEBIDA: Optional[int]
    QTDTOTCANCELADA: Optional[int]
    SITUACAOITEM: Optional[str]
    QTDAPROVADA: Optional[int]

    class Config:
        from_attributes = True  # Permite conversão entre SQLAlchemy e Pydantic
