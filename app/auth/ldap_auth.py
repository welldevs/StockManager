import os
import logging
from ldap3 import Server, Connection, ALL, NTLM
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configuração do servidor LDAP
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_PORT = int(os.getenv("LDAP_PORT", 389))
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")
LDAP_USER_DN = os.getenv("LDAP_USER_DN")
LDAP_ADMIN_USER = os.getenv("LDAP_ADMIN_USER")
LDAP_ADMIN_PASSWORD = os.getenv("LDAP_ADMIN_PASSWORD")

# Configuração do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Instância do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

router = APIRouter(prefix="/v1/auth", tags=["Auth"])

# Função para validar credenciais no AD
def authenticate_user(username: str, password: str):
    user_dn = f"cn={username},{LDAP_USER_DN},{LDAP_BASE_DN}"
    
    server = Server(LDAP_SERVER, port=LDAP_PORT, get_info=ALL)
    conn = Connection(server, user_dn, password, authentication=NTLM)

    if not conn.bind():
        logger.warning(f"Falha na autenticação do usuário {username}")
        return None

    logger.info(f"Usuário {username} autenticado com sucesso no AD")
    return {"username": username}

# Função para criar um token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Rota para login via AD
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Função para obter usuário autenticado a partir do token JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    return {"username": username}
