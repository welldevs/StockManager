from sqlalchemy import Column, Integer, String, Date, Numeric, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SuppliesModel(Base):
    __tablename__ = "SM_PEDCOMPRAS_ERP"
    __table_args__ = (
        PrimaryKeyConstraint("PEDIDOID", "SEQPRODUTO", "SEQNROPEDIDOSUP"),  # ✅ Composite Primary Key
        {"schema": "HUB"}  # ✅ Ensuring the correct schema
    )

    PEDIDOID = Column(Integer, nullable=False, index=True)  # Order ID
    SEQPRODUTO = Column(Integer, nullable=False, index=True)  # Product Sequence
    SEQNROPEDIDOSUP = Column(Integer, nullable=False)  # Supplier Order Number
    NROEMPRESA = Column(Integer, nullable=False)
    IDFORNECEDOR = Column(Integer, nullable=False)
    RAZAOFORNECEDOR = Column(String(100), nullable=False)
    IDCOMPRADOR = Column(Integer, nullable=False)
    COMPRADOR = Column(String(50), nullable=False)
    SITUACAOPED = Column(String(20), nullable=False)
    DTAEMISSAO = Column(Date, nullable=False)
    DTARECEBTO = Column(Date, nullable=False)
    PZOPAGAMENTO = Column(String(40), nullable=True)
    VLRTOTPEDIDO = Column(Numeric(15, 2), nullable=False)
    VLRTOTRECEBIDO = Column(Numeric(15, 2), nullable=True)
    DESCCOMPLETA = Column(String(150), nullable=False)
    CATEGORIA = Column(String(100), nullable=True)
    QTDSOLICITADA = Column(Integer, nullable=False)
    QTDEMBALAGEM = Column(Integer, nullable=False)
    VLREMBITEM = Column(Numeric(10, 2), nullable=False)
    QTDTOTRECEBIDA = Column(Integer, nullable=True)
    QTDTOTCANCELADA = Column(Integer, nullable=True)
    SITUACAOITEM = Column(String(30), nullable=False)
    QTDAPROVADA = Column(Integer, nullable=False)
