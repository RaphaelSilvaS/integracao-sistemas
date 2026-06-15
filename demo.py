# demo.py
# ============================================================
#  PIPELINE ETL — Integracao entre Sistemas com IA
#
#  SISTEMA 1 (Origem) : banco SQLite  →  dados/sistema1.db
#                       exportado em  →  dados/sistema1_antes_etl.json
#
#  SISTEMA 2 (Destino): arquivo JSON  →  dados/sistema2_depois_etl.json
#
#  Para validar a migracao, compare os dois arquivos JSON:
#    dados/sistema1_antes_etl.json   ← dados brutos (com invalidos)
#    dados/sistema2_depois_etl.json  ← dados migrados (somente validos)
# ============================================================

import sys
import json
import os
import sqlite3
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from src.transformer import Transformer
from src.logger import Logger

PASTA_DADOS    = "dados"
SISTEMA1_DB    = os.path.join(PASTA_DADOS, "sistema1.db")
SISTEMA1_JSON  = os.path.join(PASTA_DADOS, "sistema1_antes_etl.json")
SISTEMA2_JSON  = os.path.join(PASTA_DADOS, "sistema2_depois_etl.json")
RESUMO_JSON    = os.path.join(PASTA_DADOS, "migracao_resumo.json")


# ==============================================================
#  SETUP — cria e popula o Sistema 1 (SQLite)
# ==============================================================
def criar_sistema1():
    """Cria o banco SQLite do Sistema 1 com dados de exemplo."""
    os.makedirs(PASTA_DADOS, exist_ok=True)
    conn = sqlite3.connect(SISTEMA1_DB)
    cur  = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS produtos;
        DROP TABLE IF EXISTS pedidos;
        DROP TABLE IF EXISTS itens_pedido;

        CREATE TABLE produtos (
            id          TEXT PRIMARY KEY,
            name        TEXT,
            description TEXT,
            price       REAL,
            imageURL    TEXT,
            isFavorite  INTEGER DEFAULT 0
        );

        CREATE TABLE pedidos (
            id    TEXT PRIMARY KEY,
            total REAL,
            date  TEXT
        );

        CREATE TABLE itens_pedido (
            id         TEXT PRIMARY KEY,
            pedido_id  TEXT,
            product_id TEXT,
            name       TEXT,
            quantity   INTEGER,
            price      REAL
        );
    """)

    cur.executemany(
        "INSERT INTO produtos VALUES (?,?,?,?,?,?)",
        [
            ("prod-001", "Camiseta Polo",          "Camiseta polo masculina azul",           79.90,  "https://loja.com/camiseta.jpg", 1),
            ("prod-002", "  Calca Jeans  ",        "  Calca jeans slim fit  ",              149.90,  "https://loja.com/calca.jpg",    0),
            ("prod-003", "Tenis Running Pro",      "Tenis para corrida de alta performance", 299.90, "https://loja.com/tenis.jpg",    1),
            ("prod-004", "",                       "Produto sem nome — INVALIDO",             49.90, "https://loja.com/img.jpg",      0),
            ("prod-005", "Produto Preco Negativo", "Preco invalido — INVALIDO",              -15.00, "https://loja.com/img2.jpg",     0),
        ],
    )

    cur.executemany(
        "INSERT INTO pedidos VALUES (?,?,?)",
        [
            ("ord-001", 229.80, "2024-03-15T14:30:00"),
            ("ord-002", 299.90, "2024-03-17T11:00:00"),
            ("ord-003", 0,      "2024-03-18T09:15:00"),
        ],
    )

    cur.executemany(
        "INSERT INTO itens_pedido VALUES (?,?,?,?,?,?)",
        [
            ("item-1", "ord-001", "prod-001", "Camiseta Polo",     2, 79.90),
            ("item-2", "ord-001", "prod-002", "Calca Jeans",       1, 149.90),
            ("item-3", "ord-002", "prod-003", "Tenis Running Pro", 1, 299.90),
        ],
    )

    conn.commit()
    conn.close()


def exportar_sistema1_para_json():
    """
    Exporta o conteúdo do Sistema 1 (SQLite) para JSON legível.
    Permite comparar visualmente com o Sistema 2 após a migração.
    """
    conn = sqlite3.connect(SISTEMA1_DB)
    conn.row_factory = sqlite3.Row
    cur  = conn.cursor()

    cur.execute("SELECT * FROM produtos")
    produtos = {r["id"]: dict(r) for r in cur.fetchall()}

    cur.execute("SELECT * FROM pedidos")
    pedidos_raw = {r["id"]: dict(r) for r in cur.fetchall()}

    cur.execute("SELECT * FROM itens_pedido")
    itens_raw = cur.fetchall()

    pedidos = {}
    for pid, pedido in pedidos_raw.items():
        itens = [dict(i) for i in itens_raw if i["pedido_id"] == pid]
        pedidos[pid] = {
            "total":    pedido["total"],
            "date":     pedido["date"],
            "products": [
                {"id": i["id"], "productId": i["product_id"],
                 "name": i["name"], "quantity": i["quantity"], "price": i["price"]}
                for i in itens
            ],
        }

    conn.close()

    exportado = {
        "_descricao": "SISTEMA 1 — dados ANTES da migracao ETL (inclui registros invalidos)",
        "products": produtos,
        "orders":   pedidos,
    }

    with open(SISTEMA1_JSON, "w", encoding="utf-8") as f:
        json.dump(exportado, f, ensure_ascii=False, indent=2)


def exibir_sistema1():
    """Mostra o conteudo atual do Sistema 1 no terminal."""
    conn = sqlite3.connect(SISTEMA1_DB)
    conn.row_factory = sqlite3.Row
    cur  = conn.cursor()

    print("\n  ┌─────────────────────────────────────────────────────┐")
    print("  │     SISTEMA 1 — SQLite  (sistema1.db)               │")
    print("  │     Exportado em: sistema1_antes_etl.json           │")
    print("  └─────────────────────────────────────────────────────┘")

    cur.execute("SELECT id, name, price FROM produtos")
    rows = cur.fetchall()
    print(f"\n  Tabela [produtos] — {len(rows)} registros:")
    for r in rows:
        ok = r["name"] and str(r["name"]).strip() and r["price"] > 0
        status = "✅ valido" if ok else "⚠️  INVALIDO"
        print(f"    {r['id']:10}  {str(r['name']):26}  R$ {r['price']:>7.2f}  {status}")

    cur.execute("SELECT id, total, date FROM pedidos")
    rows = cur.fetchall()
    print(f"\n  Tabela [pedidos] — {len(rows)} registros:")
    for r in rows:
        status = "✅ valido" if r["total"] > 0 else "⚠️  INVALIDO"
        print(f"    {r['id']:10}  R$ {r['total']:>7.2f}  {r['date']}  {status}")

    conn.close()
    print()


def exibir_sistema2():
    """Mostra o conteúdo gerado no Sistema 2 no terminal."""
    if not os.path.exists(SISTEMA2_JSON):
        return

    with open(SISTEMA2_JSON, encoding="utf-8") as f:
        dados = json.load(f)

    print("\n  ┌─────────────────────────────────────────────────────┐")
    print("  │     SISTEMA 2 — JSON  (sistema2_depois_etl.json)    │")
    print("  │     Somente registros validos foram migrados        │")
    print("  └─────────────────────────────────────────────────────┘")

    for colecao, registros in dados.items():
        if colecao.startswith("_"):
            continue
        print(f"\n  [{colecao}] — {len(registros)} registros migrados:")
        for rid, rec in registros.items():
            if colecao == "products":
                print(f"    {rid:10}  {rec['name']:26}  R$ {rec['price']:>7.2f}  migrado: {rec['_migrado_em'][:10]}")
            else:
                print(f"    {rid:10}  R$ {rec['total']:>7.2f}  {rec['date'][:10]}  migrado: {rec['_migrado_em'][:10]}")
    print()


# ==============================================================
#  EXTRACTOR — le do Sistema 1 (SQLite)
# ==============================================================
class Sistema1Extractor:
    def __init__(self, db_path: str, logger):
        self.db_path = db_path
        self.logger  = logger

    def autenticar(self) -> bool:
        if not os.path.exists(self.db_path):
            self.logger.erro(f"Banco '{self.db_path}' nao encontrado.")
            return False
        self.logger.sucesso(f"Sistema 1 conectado: '{self.db_path}' (SQLite)")
        return True

    def extrair_tudo(self) -> dict:
        self.logger.titulo("ETAPA 2 — EXTRACAO  [Sistema 1 → Memoria]")
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur  = conn.cursor()

        cur.execute("SELECT * FROM produtos")
        produtos = {r["id"]: dict(r) for r in cur.fetchall()}
        self.logger.sucesso(f"'products': {len(produtos)} registros extraidos do SQLite")
        self.logger.contadores["extraidos"] += len(produtos)

        cur.execute("SELECT * FROM pedidos")
        pedidos_raw = {r["id"]: dict(r) for r in cur.fetchall()}

        cur.execute("SELECT * FROM itens_pedido")
        itens_raw = cur.fetchall()

        pedidos = {}
        for pid, pedido in pedidos_raw.items():
            itens = [dict(i) for i in itens_raw if i["pedido_id"] == pid]
            pedidos[pid] = {
                "total":    pedido["total"],
                "date":     pedido["date"],
                "products": [
                    {"id": i["id"], "productId": i["product_id"],
                     "name": i["name"], "quantity": i["quantity"], "price": i["price"]}
                    for i in itens
                ],
            }

        self.logger.sucesso(f"'orders': {len(pedidos)} registros extraidos do SQLite")
        self.logger.contadores["extraidos"] += len(pedidos)

        conn.close()
        return {"products": produtos, "orders": pedidos}


# ==============================================================
#  LOADER — grava no Sistema 2 (JSON)
# ==============================================================
class Sistema2Loader:
    def __init__(self, json_path: str, resumo_path: str, logger):
        self.json_path   = json_path
        self.resumo_path = resumo_path
        self.logger      = logger

    def autenticar(self) -> bool:
        self.logger.sucesso(f"Sistema 2 pronto: '{self.json_path}' (JSON)")
        return True

    def carregar_tudo(self, dados_transformados: dict) -> dict:
        self.logger.titulo("ETAPA 4 — CARGA  [Memoria → Sistema 2]")
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)

        saida = {
            "_descricao": "SISTEMA 2 — dados DEPOIS da migracao ETL (somente registros validos)",
            **dados_transformados,
        }

        resultados = {}
        for colecao, registros in dados_transformados.items():
            total = len(registros)
            resultados[colecao] = total
            self.logger.sucesso(f"'{colecao}': {total} registros gravados no JSON")
            self.logger.contadores["carregados"] += total

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(saida, f, ensure_ascii=False, indent=2)

        self.logger.sucesso(f"Sistema 2 atualizado: '{self.json_path}'")
        return resultados

    def salvar_metadados(self, resumo: dict):
        with open(self.resumo_path, "w", encoding="utf-8") as f:
            json.dump(resumo, f, ensure_ascii=False, indent=2)
        self.logger.sucesso(f"Resumo salvo em '{self.resumo_path}'")


# ==============================================================
#  PIPELINE PRINCIPAL
# ==============================================================
def main():
    print("\n" + "=" * 60)
    print("  PIPELINE ETL — Integracao entre Sistemas com IA")
    print("  Sistema 1 (SQLite) → ETL → Sistema 2 (JSON)")
    print("=" * 60)

    # ── SETUP: cria e exibe Sistema 1 ─────────────────────
    print("\n  [SETUP] Criando Sistema 1 (SQLite)...")
    criar_sistema1()
    exportar_sistema1_para_json()
    print(f"  Banco  : {SISTEMA1_DB}")
    print(f"  Export : {SISTEMA1_JSON}")
    exibir_sistema1()

    logger = Logger(log_dir="logs")
    inicio = datetime.now()

    # ── ETAPA 1: CONEXAO ──────────────────────────────────
    logger.titulo("ETAPA 1 — CONEXAO AOS SISTEMAS")
    extractor = Sistema1Extractor(SISTEMA1_DB, logger)
    loader    = Sistema2Loader(SISTEMA2_JSON, RESUMO_JSON, logger)

    if not extractor.autenticar():
        return sys.exit(1)
    if not loader.autenticar():
        return sys.exit(1)

    logger.separador()

    # ── ETAPA 2: EXTRACT ──────────────────────────────────
    dados_brutos = extractor.extrair_tudo()
    if not dados_brutos:
        logger.aviso("Nenhum dado extraido. Encerrando.")
        return sys.exit(1)

    logger.separador()

    # ── ETAPA 3: TRANSFORM ────────────────────────────────
    logger.titulo("ETAPA 3 — TRANSFORMACAO  [Validacao e Normalizacao]")
    transformer = Transformer(logger)
    dados_transformados = transformer.transformar(dados_brutos)

    logger.separador()

    # ── ETAPA 4: LOAD ──────────────────────────────────────
    resultados = loader.carregar_tudo(dados_transformados)

    # ── METADADOS ──────────────────────────────────────────
    fim     = datetime.now()
    duracao = (fim - inicio).total_seconds()
    resumo  = {
        "sistema_origem":  f"Sistema 1 — SQLite ({SISTEMA1_DB})",
        "sistema_destino": f"Sistema 2 — JSON ({SISTEMA2_JSON})",
        "inicio":    inicio.isoformat(),
        "fim":       fim.isoformat(),
        "duracao_s": round(duracao, 2),
        "colecoes":  resultados,
        "totais": {
            "extraidos":     logger.contadores["extraidos"],
            "transformados": logger.contadores["transformados"],
            "carregados":    logger.contadores["carregados"],
            "ignorados":     logger.contadores["ignorados"],
            "erros":         logger.contadores["erros"],
        },
    }
    loader.salvar_metadados(resumo)

    logger.info(f"Duracao total: {duracao:.2f} segundos")
    logger.relatorio_final()

    # ── EXIBE SISTEMA 2 ────────────────────────────────────
    exibir_sistema2()

    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║           ARQUIVOS PARA VALIDACAO                   ║")
    print("  ╠══════════════════════════════════════════════════════╣")
    print(f"  ║  SISTEMA 1 → {SISTEMA1_JSON:<39}║")
    print(f"  ║  SISTEMA 2 → {SISTEMA2_JSON:<39}║")
    print(f"  ║  RESUMO    → {RESUMO_JSON:<39}║")
    print("  ╚══════════════════════════════════════════════════════╝\n")

    sys.exit(0 if logger.contadores["erros"] == 0 else 1)


if __name__ == "__main__":
    main()
