"""
Script para testar a API REST do Firebase de origem.
Execucao: python testar_api.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import requests
from config.settings import FIREBASE_ORIGEM


def autenticar(config: dict) -> str:
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={config['api_key']}"
    payload = {
        "email": config["email"],
        "password": config["password"],
        "returnSecureToken": True,
    }
    resp = requests.post(url, json=payload, timeout=10)
    if resp.status_code == 200:
        return resp.json().get("idToken")
    raise RuntimeError(f"Autenticacao falhou: {resp.text}")


def testar_colecao(base_url: str, token: str, colecao: str) -> None:
    url = f"{base_url}/{colecao}.json?auth={token}"
    print(f"\n  GET {url[:60]}...")
    resp = requests.get(url, timeout=10)
    print(f"  Status: {resp.status_code}")
    if resp.status_code == 200:
        dados = resp.json()
        if dados:
            qtd = len(dados) if isinstance(dados, (list, dict)) else 1
            print(f"  Resultado: {qtd} registro(s) encontrado(s)")
            print(f"  Amostra: {str(dados)[:200]}")
        else:
            print("  Resultado: colecao vazia (null)")
    else:
        print(f"  Erro: {resp.text}")


def main():
    print("\n" + "=" * 60)
    print("  TESTE DA API REST DO FIREBASE")
    print(f"  Projeto: {FIREBASE_ORIGEM['url']}")
    print("=" * 60)

    print("\n  [1] Autenticando...")
    try:
        token = autenticar(FIREBASE_ORIGEM)
        print("  Autenticado com sucesso!")
    except RuntimeError as e:
        print(f"  ERRO: {e}")
        sys.exit(1)

    print("\n  [2] Testando colecoes...")
    for colecao in FIREBASE_ORIGEM.get("colecoes", ["products", "orders"]):
        testar_colecao(FIREBASE_ORIGEM["url"], token, colecao)

    print("\n" + "=" * 60)
    print("  API REST do Firebase funcionando!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
