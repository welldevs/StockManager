from fastapi import FastAPI
from routers import invoice, stock, auth, entry

# Configuração da API com melhor documentação
app = FastAPI(
    title="Stock Manager API",
    description="API para gerenciamento de estoque, faturas e autenticação.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Auth", "description": "Endpoints de autenticação"},
        {"name": "Invoices", "description": "Gerenciamento de faturas"},
        {"name": "Stock", "description": "Gerenciamento de estoque"},
        {"name": "Entry", "description": "Gerenciamento de entradas"}
    ],
)

# Ocultar a rota `/` da documentação
@app.get("/", include_in_schema=False)
def home():
    return {"message": "API is running"}

# Incluir roteadores com prefixo e tags organizadas
app.include_router(auth.router,     tags=["Auth"])
app.include_router(invoice.router,  tags=["Invoices"])
app.include_router(stock.router,    tags=["Stock"])
app.include_router(entry.router,    tags=["Entry"])
