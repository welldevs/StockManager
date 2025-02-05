from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StockModel(Base):
    __tablename__ = "sm_estoque_erp"
    __table_args__ = {"schema": "HUB"}

    EMPRESAID = Column(Integer, nullable=False)
    PRODUTOID = Column(Integer, primary_key=True, index=True)
    FORNECEDORID = Column(Integer, nullable=True)
    CATEGORIA = Column(String(100), nullable=True)
    FAMILIAID = Column(Integer, nullable=True)
    QTDESTQUNITARIO = Column(Integer, nullable=True)
    PADRAOEMBCOMPRA = Column(Integer, nullable=True)
    QTDESTQEMBCOMPRA = Column(Numeric(18, 2), nullable=True)
    VLRCUSTOLIQUIDO = Column(Numeric(18, 2), nullable=True)
    CUSTOLIQUNITARIO = Column(Numeric(18, 2), nullable=True)
    DIASSEMVENDA = Column(String(50), nullable=True)
