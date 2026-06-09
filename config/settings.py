# config/settings.py
# ============================================================
#  CONFIGURAÇÕES DOS DOIS PROJETOS FIREBASE
#  Substitua as URLs e chaves pelos seus projetos reais
# ============================================================

# ----------------------------
#  SISTEMA X — ORIGEM
# ----------------------------
FIREBASE_ORIGEM = {
    "nome": "Sistema X (Origem)",
    # URL do seu Firebase Realtime Database de ORIGEM
    # Exemplo: https://meu-projeto-origem-default-rtdb.firebaseio.com
    "url": "https://shop-app-fl-default-rtdb.firebaseio.com",

    # Chave da API Web do projeto Firebase de ORIGEM
    # Encontre em: Firebase Console → Configurações do projeto → Chave de API da Web
    "api_key": "AIzaSyBjzyh1DgWZBm0968oZ89MPOiZofA02Gd4",

    # Credenciais de um usuário com permissão de LEITURA no banco de ORIGEM
    "email": "seu-email-origem@email.com",
    "password": "sua-senha-origem",

    # Coleções que serão extraídas
    "colecoes": ["products", "orders"],
}

# ----------------------------
#  SISTEMA Y — DESTINO
# ----------------------------
FIREBASE_DESTINO = {
    "nome": "Sistema Y (Destino)",
    # URL do seu Firebase Realtime Database de DESTINO
    # Exemplo: https://meu-projeto-destino-default-rtdb.firebaseio.com
    "url": "https://SEU-PROJETO-DESTINO-default-rtdb.firebaseio.com",

    # Chave da API Web do projeto Firebase de DESTINO
    "api_key": "SUA_API_KEY_DESTINO",

    # Credenciais de um usuário com permissão de ESCRITA no banco de DESTINO
    "email": "seu-email-destino@email.com",
    "password": "sua-senha-destino",
}

# ----------------------------
#  CONFIGURAÇÕES GERAIS
# ----------------------------
LOG_DIR = "logs"
LOG_LEVEL = "INFO"   # DEBUG | INFO | WARNING | ERROR
