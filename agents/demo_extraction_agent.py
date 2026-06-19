import sqlite3
import os

from agents.base_agent import BaseAgent


class DemoExtractionAgent(BaseAgent):
    """Sub-agente de extração para modo demo — Sistema A é um banco SQLite local."""

    def __init__(self, db_path: str = "dados/sistema_a.db"):
        super().__init__(
            name="Agente de Extração (Demo)",
            description="Cria e lê o Sistema A (SQLite local) com dados de exemplo.",
        )
        self.db_path = db_path

    def execute(self, context: dict) -> dict:
        os.makedirs("dados", exist_ok=True)
        self._criar_banco()

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM produtos")
        produtos = [dict(row) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT p.*, GROUP_CONCAT(i.produto_nome) as produtos
            FROM pedidos p
            LEFT JOIN itens_pedido i ON p.id = i.pedido_id
            GROUP BY p.id
        """)
        pedidos_raw = [dict(row) for row in cursor.fetchall()]
        pedidos = []
        for p in pedidos_raw:
            p["produtos"] = p["produtos"].split(",") if p["produtos"] else []
            pedidos.append(p)

        conn.close()

        dados_brutos = {"products": produtos, "orders": pedidos}
        total = len(produtos) + len(pedidos)

        print(f"    Sistema A: {self.db_path}")
        print(f"    Extraídos: {len(produtos)} produtos, {len(pedidos)} pedidos")

        return {
            "dados_brutos": dados_brutos,
            "colecoes_extraidas": list(dados_brutos.keys()),
            "total_registros_extraidos": total,
        }

    def _criar_banco(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                descricao TEXT,
                imageURL TEXT,
                preco REAL
            );
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY,
                total REAL,
                data TEXT
            );
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY,
                pedido_id INTEGER,
                produto_nome TEXT,
                quantidade INTEGER,
                preco_unit REAL
            );
            DELETE FROM produtos;
            DELETE FROM pedidos;
            DELETE FROM itens_pedido;
        """)

        produtos = [
            (1, "Camiseta Polo",   "Camiseta de algodão polo", "http://img.com/1.jpg", 79.90),
            (2, "Calça Jeans",     "Calça slim fit",            "http://img.com/2.jpg", 149.90),
            (3, "Tênis Running Pro","Tênis para corrida",       "http://img.com/3.jpg", 299.90),
            (4, "",                "Produto sem nome",          "http://img.com/4.jpg", 49.90),
            (5, "Preço negativo",  "Produto com preço inválido","http://img.com/5.jpg", -15.00),
        ]
        cursor.executemany(
            "INSERT INTO produtos VALUES (?,?,?,?,?)", produtos
        )

        pedidos = [
            (1, 229.80, "2024-01-15T10:30:00"),
            (2, 299.90, "2024-01-16T11:00:00"),
            (3, 0.00,   "2024-01-17T09:00:00"),
        ]
        cursor.executemany("INSERT INTO pedidos VALUES (?,?,?)", pedidos)

        itens = [
            (1, 1, "Camiseta Polo",    1, 79.90),
            (2, 1, "Calça Jeans",      1, 149.90),
            (3, 2, "Tênis Running Pro",1, 299.90),
        ]
        cursor.executemany("INSERT INTO itens_pedido VALUES (?,?,?,?,?)", itens)

        conn.commit()
        conn.close()
