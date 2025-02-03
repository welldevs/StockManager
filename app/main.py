import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from app.routers import invoices, stock

app = FastAPI()

# Incluindo o roteador de invoices
app.include_router(invoices.router)
app.include_router(stock.router)

@app.get("/")
def home():
    return {"message": "API is running"}