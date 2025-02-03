from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from auth.jwt_handler import verify_token

class JWTBearer(HTTPBearer):
    """Middleware para verificar o token JWT"""
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Esquema de autenticação inválido")
            return verify_token(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Token não encontrado")
