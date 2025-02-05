from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EntryModel(Base):
    __tablename__ = "sm_entradas_erp"
    __table_args__ = {"schema": "HUB"}

    DOCUMENTO = Column(Integer, primary_key=True, index=True)
    DOCSERIEID = Column(String(10), nullable=True)
    CGO = Column(Integer, nullable=True)
    FORNECEDORID = Column(Integer, nullable=True)
    NOMERAZAO = Column(String(200), nullable=True)
    EMPRESAID = Column(Integer, nullable=True)
    SEQNF = Column(Integer, nullable=True)
    DATAEMISSAO = Column(Date, nullable=True)
    DATAENTRADA = Column(Date, nullable=True)
    CATEGORIA = Column(String(100), nullable=True)
    PRODUTOID = Column(Integer, nullable=True)
    FAMILIAID = Column(Integer, nullable=True)
    PADRAOEMBCOMPRA = Column(String(50), nullable=True)
    QTDEMBALAGEM = Column(Integer, nullable=True)
    EMBALAGEM = Column(String(50), nullable=True)
    QTDSOLICITADA = Column(Integer, nullable=True)
    QTDUNITARIO = Column(Integer, nullable=True)
    VLRUNID = Column(String(20), nullable=True)
    VALORITEM = Column(Numeric(18, 2), nullable=True)
    SEQMOVTOESTQ = Column(Integer, nullable=True)
    PRAZOFORNECEDOR = Column(Integer, nullable=True)
