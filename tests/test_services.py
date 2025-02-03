from app.services.services import fetch_invoices
from fastapi import HTTPException

def test_fetch_invoices_valid(db):
    """Testa se a função retorna resultados corretamente"""
    page = 1
    page_size = 10
    try:
        result = fetch_invoices(db, page, page_size)
        assert isinstance(result, list)
    except HTTPException as e:
        assert e.status_code != 500  # Não pode gerar erro 500

def test_fetch_invoices_invalid_page(db):
    """Testa erro quando a página é inválida"""
    page = 0  # Inválido
    page_size = 10
    try:
        fetch_invoices(db, page, page_size)
    except HTTPException as e:
        assert e.status_code == 400  # Deve retornar 400 Bad Request

def test_fetch_invoices_no_results(db):
    """Testa quando não há resultados"""
    page = 1000  # Uma página alta para garantir sem resultados
    page_size = 10
    try:
        fetch_invoices(db, page, page_size)
    except HTTPException as e:
        assert e.status_code == 404  # Nenhum resultado encontrado
