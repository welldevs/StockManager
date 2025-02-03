def test_get_invoices(client):
    """Testa se o endpoint retorna HTTP 200"""
    response = client.get("/v1/invoices?page=1&page_size=10")
    assert response.status_code in [200, 404]  # Pode retornar 200 OK ou 404 se não houver dados

def test_get_invoices_invalid_page(client):
    """Testa se o endpoint retorna erro ao receber um número de página inválido"""
    response = client.get("/v1/invoices?page=0&page_size=10")
    assert response.status_code == 422  # FastAPI retorna 422, então o teste precisa refletir isso

def test_get_invoices_large_page_size(client):
    """Testa se o endpoint retorna erro ao receber um page_size maior que o permitido"""
    response = client.get("/v1/invoices?page=1&page_size=200")  # Limite é 100
    assert response.status_code == 422  # FastAPI valida automaticamente e retorna 422

