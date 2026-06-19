import sqlite3
import os
from agents.base_agent import BaseAgent


class ExtractionAgent(BaseAgent):
    def __init__(self, db_path: str = "dados/sistema_a.db"):
        super().__init__(
            name="Agente de Extracao",
            description="Extrai dados brutos do Sistema A (SQLite) para o pipeline.",
        )
        self.db_path = db_path

    def execute(self, context: dict) -> dict:
        os.makedirs("dados", exist_ok=True)
        self._criar_banco_se_necessario()

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        products = [dict(row) for row in cursor.fetchall()]

        cursor.execute("SELECT * FROM orders")
        orders = [dict(row) for row in cursor.fetchall()]

        conn.close()

        print(f"    Extraidos: {len(products)} produtos, {len(orders)} pedidos")

        return {
            "dados_brutos": {
                "products": products,
                "orders": orders,
            },
            "total_extraido": len(products) + len(orders),
        }

    def _criar_banco_se_necessario(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                price REAL,
                imageURL TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                total REAL,
                date TEXT,
                user_id TEXT
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            produtos = [
                ("prod-001", "Camiseta Basica Branca", "Camiseta 100% algodao, corte regular, ideal para o dia a dia.", 49.90, ""),
                ("prod-002", "Calca Jeans Slim", "Calca jeans slim fit com elastano para maior conforto.", 129.90, ""),
                ("prod-003", "Tenis Casual Branco", "Tenis casual estilo minimalista, solado emborrachado.", 199.90, ""),
                ("prod-004", "Moletom Canguru Cinza", "Moletom com capuz e bolso canguru. Tecido fleece macio.", 89.90, ""),
                ("prod-005", "Jaqueta Corta-Vento Preta", "Jaqueta leve e resistente ao vento, com capuz removivel.", 159.90, ""),
                ("prod-006", "Bermuda Tactel Azul", "Bermuda leve em tecido tactel com bolsos laterais.", 59.90, ""),
                ("prod-007", "Vestido Floral Colorido", "Vestido midi com estampa floral, tecido viscose fluido.", 119.90, ""),
                ("prod-008", "Polo Listrada Premium", "Camiseta polo com listras, gola ribana e dois botoes.", 79.90, ""),
            ]
            cursor.executemany(
                "INSERT INTO products VALUES (?, ?, ?, ?, ?)", produtos
            )

            pedidos = [
                ("ord-001", 229.80, "2026-06-01T14:30:00", "user-001"),
                ("ord-002", 199.90, "2026-06-05T11:00:00", "user-002"),
                ("ord-003", 89.90,  "2026-06-10T09:15:00", "user-001"),
            ]
            cursor.executemany(
                "INSERT INTO orders VALUES (?, ?, ?, ?)", pedidos
            )

        conn.commit()
        conn.close()
