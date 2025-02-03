from ldap3 import Server, Connection, ALL
import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_PORT = int(os.getenv("LDAP_PORT", 389))
LDAP_ADMIN_USER = os.getenv("LDAP_ADMIN_USER")
LDAP_ADMIN_PASSWORD = os.getenv("LDAP_ADMIN_PASSWORD")

server = Server(LDAP_SERVER, port=LDAP_PORT, get_info=ALL)

try:
    conn = Connection(server, user=LDAP_ADMIN_USER, password=LDAP_ADMIN_PASSWORD, auto_bind=True)
    print("✅ Conexão bem-sucedida com o Active Directory!")
    conn.unbind()
except Exception as e:
    print(f"❌ Erro ao conectar ao AD: {e}")
