import os
import ldap3
import logging
import time
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPBindError, LDAPException
from collections import defaultdict

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("auth.log"),  # Salva logs em arquivo
        logging.StreamHandler()  # Imprime logs no console
    ]
)

# Configurações LDAP
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_PORT = int(os.getenv("LDAP_PORT", 389))

# Segurança: limitar tentativas para evitar brute-force
MAX_ATTEMPTS = 5
BLOCK_TIME = 300  # 5 minutos

failed_attempts = defaultdict(int)
blocked_users = {}

if not LDAP_SERVER:
    logging.error("❌ Configuração LDAP incompleta! Verifique LDAP_SERVER.")
    raise ValueError("Configuração de ambiente incompleta.")

def authenticate_user(email: str, password: str, client_ip: str = "unknown"):
    """Autentica um usuário no LDAP pelo e-mail e retorna um dicionário se for bem-sucedido."""
    
    logging.info(f"🔍 [{client_ip}] Tentativa de login para {email}")

    if not email or not password:
        logging.warning(f"❌ [{client_ip}] Tentativa de login com credenciais vazias.")
        return None  # Falha de autenticação

    current_time = time.time()

    if email in blocked_users and current_time < blocked_users[email]:
        logging.warning(f"🚫 [{client_ip}] Usuário {email} está temporariamente bloqueado.")
        return None  # Usuário bloqueado

    try:
        logging.info(f"🔍 [{client_ip}] Tentando autenticação via LDAP: {email}")

        server = Server(LDAP_SERVER, port=LDAP_PORT, get_info=ALL)
        conn = Connection(server, user=email, password=password, auto_bind=True)

        if conn.bound:
            logging.info(f"✅ [{client_ip}] Autenticação bem-sucedida para {email}")
            conn.unbind()

            # Resetar tentativas falhas se o login for bem-sucedido
            failed_attempts.pop(email, None)
            blocked_users.pop(email, None)

            return {"username": email, "message": "Autenticado com sucesso!"}

    except LDAPBindError:
        logging.warning(f"🔑 [{client_ip}] Falha ao autenticar {email}.")
    except LDAPException as e:
        logging.error(f"⚠️ [{client_ip}] Erro no LDAP ao autenticar {email}: {e}")

    # Se a autenticação falhar, contar tentativa
    failed_attempts[email] += 1
    logging.warning(f"⚠️ [{client_ip}] Falha total na autenticação para {email}. Tentativa {failed_attempts[email]}/{MAX_ATTEMPTS}")

    if failed_attempts[email] >= MAX_ATTEMPTS:
        blocked_users[email] = current_time + BLOCK_TIME
        logging.warning(f"🚫 [{client_ip}] Usuário {email} bloqueado por {BLOCK_TIME} segundos.")

    return None  # Falha de autenticação
