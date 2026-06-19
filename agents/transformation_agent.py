from datetime import datetime
from agents.base_agent import BaseAgent


class TransformationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Agente de Transformacao",
            description="Valida campos, normaliza dados e adiciona metadados de migracao.",
        )

    def execute(self, context: dict) -> dict:
        dados = context.get("dados_brutos", {})
        produtos_transformados = []
        invalidos = 0

        for produto in dados.get("products", []):
            if not produto.get("name") or not produto.get("description") or not produto.get("price"):
                invalidos += 1
                continue
            if float(produto.get("price", 0)) <= 0:
                invalidos += 1
                continue

            produtos_transformados.append({
                "name": str(produto["name"]).strip().title(),
                "description": str(produto["description"]).strip(),
                "price": round(float(produto["price"]), 2),
                "imageURL": produto.get("imageURL", ""),
                "_migrado_em": datetime.now().isoformat(),
                "_sistema_origem": "Sistema A (SQLite)",
            })

        print(f"    Transformados: {len(produtos_transformados)} validos, {invalidos} invalidos")

        return {
            "dados_transformados": produtos_transformados,
            "total_transformado": len(produtos_transformados),
            "total_invalido": invalidos,
        }
