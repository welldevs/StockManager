from fastapi import APIRouter, Depends, HTTPException, Request
from auth.ldap_auth import authenticate_user
from auth.jwt_handler import create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(request: Request, login_data: LoginRequest):
    """Autenticação via LDAP e geração de token JWT"""
    
    client_ip = request.client.host  # Obtém o IP do cliente

    user = authenticate_user(login_data.email, login_data.password, client_ip)
    if user is None:  # Se o login falhar, retorna erro 401
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = create_access_token({"sub": login_data.email})
    return {"access_token": token, "token_type": "bearer"}
