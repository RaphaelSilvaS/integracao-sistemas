"""
SISTEMA A — Pipeline ETL em Python
Valida, transforma e carrega produtos no Firebase (Sistema B via REST API).

Uso:
    python seed_firebase.py
"""

import requests
import json
from datetime import datetime

# ─── Configuração do Firebase (Sistema B) ────────────────────────────────────
FIREBASE_DB_URL = "https://projeto-integrador-303c5-default-rtdb.firebaseio.com"

# ─── Dados brutos do Sistema A ────────────────────────────────────────────────
PRODUTOS_SISTEMA_A = [
    {"name": "Camiseta Básica Branca",   "description": "Camiseta 100% algodão, corte regular, ideal para o dia a dia. Disponível em vários tamanhos.", "price": 49.90},
    {"name": "Calça Jeans Slim",          "description": "Calça jeans slim fit com elastano para maior conforto. Perfeita para looks casuais e modernos.", "price": 129.90},
    {"name": "Tênis Casual Branco",       "description": "Tênis casual estilo minimalista, solado emborrachado antiderrapante. Confortável para uso diário.", "price": 199.90},
    {"name": "Moletom Canguru Cinza",     "description": "Moletom com capuz e bolso canguru. Tecido fleece macio por dentro, perfeito para dias frios.", "price": 89.90},
    {"name": "Jaqueta Corta-Vento Preta", "description": "Jaqueta leve e resistente ao vento, com capuz removível. Ideal para atividades ao ar livre.", "price": 159.90},
    {"name": "Bermuda Tactel Azul",       "description": "Bermuda leve em tecido tactel com bolsos laterais. Ótima para praia e esportes.", "price": 59.90},
    {"name": "Vestido Floral Colorido",   "description": "Vestido midi com estampa floral, tecido viscose fluido. Elegante e confortável para qualquer ocasião.", "price": 119.90},
    {"name": "Polo Listrada Premium",     "description": "Camiseta polo com listras, gola ribana e dois botões. Estilo clássico com caimento impecável.", "price": 79.90},
]


# ─── Agente de Validação (sem API externa — regras locais) ────────────────────
def validar_produto(produto: dict) -> tuple[bool, list[str]]:
    erros = []
    if not produto.get("name") or len(produto["name"].strip()) < 3:
        erros.append("Nome inválido (mínimo 3 caracteres)")
    if not produto.get("description") or len(produto["description"].strip()) < 10:
        erros.append("Descrição inválida (mínimo 10 caracteres)")
    if not produto.get("price") or produto["price"] <= 0:
        erros.append("Preço inválido (deve ser maior que zero)")
    return len(erros) == 0, erros


# ─── Agente de Transformação ──────────────────────────────────────────────────
def transformar_produto(produto: dict) -> dict:
    return {
        "name": produto["name"].strip(),
        "description": produto["description"].strip(),
        "price": round(float(produto["price"]), 2),
        "imageURL": "",
        "_migrado_em": datetime.now().isoformat(),
        "_sistema_origem": "Sistema A (Python)",
    }


# ─── Agente de Carga ──────────────────────────────────────────────────────────
def carregar_produto(produto_transformado: dict) -> bool:
    url = f"{FIREBASE_DB_URL}/products.json"
    resp = requests.post(url, data=json.dumps(produto_transformado))
    return resp.status_code == 200


# ─── Pipeline Principal ───────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 60)
    print("  SISTEMA A — Pipeline ETL Python → Firebase")
    print("  Destino: Sistema B (Firebase Realtime Database)")
    print("=" * 60)

    # Verifica produtos existentes
    url = f"{FIREBASE_DB_URL}/products.json"
    response = requests.get(url)
    existing = response.json()
    if existing:
        print(f"\n  Banco já possui {len(existing)} produto(s).")
        print("  Deseja sobrescrever? (s/n): ", end="")
        if input().strip().lower() != "s":
            print("  Cancelado.\n")
            return

    total = len(PRODUTOS_SISTEMA_A)
    carregados = 0
    invalidos = 0

    print(f"\n  Processando {total} produtos do Sistema A...\n")

    for produto in PRODUTOS_SISTEMA_A:
        nome = produto.get("name", "?")

        # Etapa 1: Validação
        valido, erros = validar_produto(produto)
        if not valido:
            print(f"  [INVALIDO] {nome}")
            for e in erros:
                print(f"             - {e}")
            invalidos += 1
            continue

        # Etapa 2: Transformação
        produto_transformado = transformar_produto(produto)

        # Etapa 3: Carga no Firebase (Sistema B)
        sucesso = carregar_produto(produto_transformado)
        if sucesso:
            print(f"  [OK] {nome} — R$ {produto['price']:.2f}")
            carregados += 1
        else:
            print(f"  [ERRO] {nome} — falha ao carregar no Firebase")

    print("\n" + "=" * 60)
    print(f"  Carregados:  {carregados}/{total}")
    print(f"  Inválidos:   {invalidos}/{total}")
    print(f"  Firebase:    {FIREBASE_DB_URL}/products.json")
    print("=" * 60)
    print("\n  Sistema B (Flutter) já pode ler os produtos no app.\n")


if __name__ == "__main__":
    main()
