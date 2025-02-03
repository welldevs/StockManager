import pytest
import sys
import os
# Adiciona o caminho raiz para garantir que `app/` seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.testclient import TestClient
from app.database.database import Base, get_db
from app.main import app

# Criar banco de dados SQLite em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir Base corretamente
Base = declarative_base()

# Criar um mock da tabela para os testes
class MockFaturamentoERP(Base):
    __tablename__ = "SM_FATURAMENTO_ERP"

    DOCUMENTOID = Column(Integer, primary_key=True, index=True)
    DOCSERIEID = Column(String(50))
    EMPRESAID = Column(Integer)
    CLIENTEID = Column(Integer)
    NROCARGA = Column(Integer)
    PRODUTOID = Column(Integer)
    CATEGORIA = Column(String(100))
    FAMILIAID = Column(Integer)
    PADRAOEMBCOMPRA = Column(Integer)
    QTDEMBVENDA = Column(Integer)
    QUANTIDADE = Column(Integer)
    VLRITEMUNITARIOVENDA = Column(Float)
    VLRITEMTOTALVENDA = Column(Float)
    PRAZOPAGAMENTO = Column(Integer)
    DTAFATURAMENTO = Column(DateTime)
    DTAINCLUSAO = Column(DateTime)
    USUINCLUSAO = Column(String(20))
    SEQMOVTOESTQ = Column(Integer)

@pytest.fixture(scope="function")
def db():
    """Cria uma sessão do banco de dados para testes"""
    Base.metadata.create_all(bind=engine)  # Criar tabelas antes do teste
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # Remover tabelas após o teste

@pytest.fixture(scope="function")
def client():
    """Cria um cliente de teste do FastAPI"""
    return TestClient(app)
