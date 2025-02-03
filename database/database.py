from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do .env
load_dotenv()

# Obter credenciais do banco de dados
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT", "1521")  # Porta padrão do Oracle
db_service = os.getenv("DB_SERVICE")  # Nome do serviço Oracle

# Criar a URL de conexão
DATABASE_URL = f"oracle+cx_oracle://{db_user}:{db_password}@{db_host}:{db_port}/?service_name={db_service}"

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos ORM
Base = declarative_base()

def get_db():
    """Dependência para obter uma sessão do banco de dados no FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
