import json
import os
from datetime import datetime

from agents.base_agent import BaseAgent


class DemoLoadingAgent(BaseAgent):
    """Sub-agente de carga para modo demo — Sistema B é JSON local."""

    def __init__(self, output_dir: str = "dados/sistema_b"):
        super().__init__(
            name="Agente de Carga (Demo)",
            description="Grava os dados transformados no Sistema B (arquivos JSON locais).",
        )
        self.output_dir = output_dir

    def execute(self, context: dict) -> dict:
        dados = context.get("dados_transformados", {})
        os.makedirs(self.output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivos_gerados = []

        for colecao, registros in dados.items():
            caminho = os.path.join(self.output_dir, f"{colecao}_{timestamp}.json")
            payload = {
                "sistema": "Sistema B — JSON Local",
                "colecao": colecao,
                "timestamp": timestamp,
                "total": len(registros),
                "dados": registros,
            }
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            arquivos_gerados.append(caminho)
            print(f"    {colecao}: {len(registros)} registros → {caminho}")

        total = sum(len(v) for v in dados.values())

        return {
            "colecoes_carregadas": list(dados.keys()),
            "total_registros_carregados": total,
            "arquivos_sistema_b": arquivos_gerados,
        }
