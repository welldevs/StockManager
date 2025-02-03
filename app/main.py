from fastapi import FastAPI
from app.routers import invoices

app = FastAPI()

# Incluindo o roteador de invoices
app.include_router(invoices.router)

@app.get("/")
def home():
    return {"message": "API is running"}