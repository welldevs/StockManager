import sys
import os
from fastapi import FastAPI

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routers import invoices, stock, auth, entry

app = FastAPI()

# Incluir roteadores
app.include_router(auth.router)
app.include_router(invoices.router)
app.include_router(stock.router)
app.include_router(entry.router)

@app.get("/")
def home():
    return {"message": "API is running"}