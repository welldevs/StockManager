from datetime import datetime, timedelta
from jose import JWTError, jwt

# Chave secreta para assinatura do JWT
SECRET_KEY = "vilastockmanager"  # 🔴 ALTERE PARA UMA CHAVE SEGURA
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token válido por 1 hora

# Gera um token JWT para o usuário autenticado
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decodifica e valida um token JWT
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Retorna os dados do usuário autenticado
    except JWTError:
        return None
