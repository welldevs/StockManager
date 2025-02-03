import os
import ldap3
import logging
from ldap3 import Server, Connection, ALL, NTLM

# Configurar logs para debug
logging.basicConfig(level=logging.DEBUG)

LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_PORT = int(os.getenv("LDAP_PORT", 389))
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")
LDAP_USER_DN = os.getenv("LDAP_USER_DN")

def authenticate_user(username: str, password: str):
    """Autentica um usuário no LDAP."""
    
    # Testar diferentes formatos de DN do usuário
    possible_user_dns = [
        f"CN={username},{LDAP_USER_DN}",
        f"{username}@vilanova.com.br",  # Formato UPN
        f"VILANOVA\\{username}"  # NTLM
    ]

    for user_dn in possible_user_dns:
        try:
            logging.info(f"Tentando autenticar {user_dn} no LDAP {LDAP_SERVER}:{LDAP_PORT}")

            server = Server(LDAP_SERVER, port=LDAP_PORT, get_info=ALL)
            conn = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)

            if conn.bind():
                logging.info(f"✅ Usuário {username} autenticado com sucesso!")
                return {"username": username, "message": "Autenticado com sucesso!"}
            
            logging.warning(f"❌ Falha na autenticação de {username}")
        except ldap3.core.exceptions.LDAPException as e:
            logging.error(f"Erro ao autenticar {username}: {e}")

    return {"detail": "Credenciais inválidas"}
