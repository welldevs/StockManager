import requests
import time

# Configuração da API
BASE_URL = "http://127.0.0.1:8001/v1/invoice"  # 🔄 Modifique se necessário
PAGE_SIZE = 100  # Define o tamanho da página

# 🔐 Adicione "Bearer " antes do token para autenticação correta
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ3ZWx0b24uZmVycmVpcmFAdmlsYW5vdmEuY29tLmJyIiwiZXhwIjoxNzM4NzYzMDYzfQ.LrkWUyamnUZ4g_Qh_QY2eWAlho_yNdse_Zokn39CTKU"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}  # 🔥 Adicionado "Bearer " antes do token

def test_pagination():
    page = 1  # Começa na primeira página
    total_requests = 0
    total_time = 0.0

    while True:
        url = f"{BASE_URL}?page={page}&page_size={PAGE_SIZE}"
        print(f"🔄 Consultando página {page}...")

        # Medir tempo de resposta
        start_time = time.time()
        response = requests.get(url, headers=HEADERS)
        elapsed_time = time.time() - start_time

        # Exibir tempo de resposta
        print(f"⏱ Tempo de resposta: {elapsed_time:.3f} segundos")

        # Atualizar estatísticas
        total_requests += 1
        total_time += elapsed_time

        # Verificar se a resposta é válida
        if response.status_code == 401:
            print("❌ Erro de autenticação! Token inválido ou expirado.")
            return
        elif response.status_code != 200:
            print(f"❌ Erro na requisição: {response.status_code} - {response.text}")
            break

        data = response.json()
        if not data:  # Se a resposta estiver vazia, significa que não há mais registros
            print("✅ Todas as páginas foram percorridas.")
            break

        page += 1  # Incrementa a página

    # Exibir estatísticas finais
    print(f"\n📊 Teste concluído!")
    print(f"📌 Total de páginas consultadas: {total_requests}")
    print(f"📌 Tempo médio de resposta: {total_time / total_requests:.3f} segundos")

if __name__ == "__main__":
    test_pagination()
