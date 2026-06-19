"""
Script para popular o Firebase com produtos de exemplo.
Executa apenas uma vez para criar a base inicial de produtos.

Uso:
    python seed_firebase.py
"""

import requests
import json

FIREBASE_DB_URL = "https://projeto-integrador-303c5-default-rtdb.firebaseio.com"

PRODUTOS = [
    {
        "name": "Camiseta Básica Branca",
        "description": "Camiseta 100% algodão, corte regular, ideal para o dia a dia. Disponível em vários tamanhos.",
        "price": 49.90,
        "imageURL": "",
    },
    {
        "name": "Calça Jeans Slim",
        "description": "Calça jeans slim fit com elastano para maior conforto. Perfeita para looks casuais e modernos.",
        "price": 129.90,
        "imageURL": "",
    },
    {
        "name": "Tênis Casual Branco",
        "description": "Tênis casual estilo minimalista, solado emborrachado antiderrapante. Confortável para uso diário.",
        "price": 199.90,
        "imageURL": "",
    },
    {
        "name": "Moletom Canguru Cinza",
        "description": "Moletom com capuz e bolso canguru. Tecido fleece macio por dentro, perfeito para dias frios.",
        "price": 89.90,
        "imageURL": "",
    },
    {
        "name": "Jaqueta Corta-Vento Preta",
        "description": "Jaqueta leve e resistente ao vento, com capuz removível. Ideal para atividades ao ar livre.",
        "price": 159.90,
        "imageURL": "",
    },
    {
        "name": "Bermuda Tactel Azul",
        "description": "Bermuda leve em tecido tactel com bolsos laterais. Ótima para praia e esportes.",
        "price": 59.90,
        "imageURL": "",
    },
    {
        "name": "Vestido Floral Colorido",
        "description": "Vestido midi com estampa floral, tecido viscose fluido. Elegante e confortável para qualquer ocasião.",
        "price": 119.90,
        "imageURL": "",
    },
    {
        "name": "Polo Listrada Premium",
        "description": "Camiseta polo com listras, gola ribana e dois botões. Estilo clássico com caimento impecável.",
        "price": 79.90,
        "imageURL": "",
    },
]


def seed():
    url = f"{FIREBASE_DB_URL}/products.json"

    print("Verificando produtos existentes...")
    response = requests.get(url)
    existing = response.json()

    if existing:
        print(f"Banco já possui {len(existing)} produto(s). Deseja sobrescrever? (s/n): ", end="")
        resposta = input().strip().lower()
        if resposta != "s":
            print("Operação cancelada.")
            return

    print(f"\nAdicionando {len(PRODUTOS)} produtos ao Firebase...")

    for produto in PRODUTOS:
        resp = requests.post(url, data=json.dumps(produto))
        if resp.status_code == 200:
            print(f"  [OK] {produto['name']}")
        else:
            print(f"  [ERRO] {produto['name']} — status {resp.status_code}")

    print(f"\nConcluido! {len(PRODUTOS)} produtos adicionados.")
    print(f"Acesse: {FIREBASE_DB_URL}/products.json para verificar.")


if __name__ == "__main__":
    seed()
