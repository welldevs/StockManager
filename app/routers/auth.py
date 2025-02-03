from fastapi import APIRouter, Depends, HTTPException
from auth.ldap_auth import authenticate_user
from auth.jwt_handler import create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    """Autenticação via LDAP e geração de token JWT"""
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = create_access_token({"sub": request.username})
    return {"access_token": token, "token_type": "bearer"}
