from datetime import datetime
from agents.base_agent import BaseAgent


class DemoTransformationAgent(BaseAgent):
    """Sub-agente de transformação para modo demo — valida e normaliza sem dependências externas."""

    def __init__(self):
        super().__init__(
            name="Agente de Transformação (Demo)",
            description="Valida campos obrigatórios, normaliza valores e rejeita registros inválidos.",
        )

    def execute(self, context: dict) -> dict:
        dados_brutos = context.get("dados_brutos", {})
        timestamp = datetime.now().isoformat()

        produtos_ok, produtos_rej = [], []
        for p in dados_brutos.get("products", []):
            nome = str(p.get("nome", "")).strip()
            preco = p.get("preco", 0)
            if nome and isinstance(preco, (int, float)) and preco > 0:
                produtos_ok.append({
                    **p,
                    "nome": nome,
                    "preco": round(float(preco), 2),
                    "migrado_em": timestamp,
                })
            else:
                produtos_rej.append(p)

        pedidos_ok, pedidos_rej = [], []
        for p in dados_brutos.get("orders", []):
            total = p.get("total", 0)
            itens = p.get("produtos", [])
            data = str(p.get("data", ""))
            valido = (
                isinstance(total, (int, float)) and total > 0
                and isinstance(itens, list) and len(itens) > 0
                and "T" in data
            )
            if valido:
                pedidos_ok.append({**p, "migrado_em": timestamp})
            else:
                pedidos_rej.append(p)

        dados_transformados = {"products": produtos_ok, "orders": pedidos_ok}
        total = len(produtos_ok) + len(pedidos_ok)
        rejeitados = len(produtos_rej) + len(pedidos_rej)

        print(f"    Aprovados : {total} registros")
        print(f"    Rejeitados: {rejeitados} registros")

        return {
            "dados_transformados": dados_transformados,
            "colecoes_transformadas": list(dados_transformados.keys()),
            "total_registros_transformados": total,
            "total_rejeitados": rejeitados,
            "produtos_rejeitados": produtos_rej,
            "pedidos_rejeitados": pedidos_rej,
        }
