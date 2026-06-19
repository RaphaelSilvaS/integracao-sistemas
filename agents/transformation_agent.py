import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.base_agent import BaseAgent
from src.transformer import Transformer


class TransformationAgent(BaseAgent):
    """Sub-agente responsável por validar e normalizar os dados extraídos."""

    def __init__(self, logger):
        super().__init__(
            name="Agente de Transformação",
            description="Valida campos obrigatórios, normaliza valores e prepara dados para carga.",
        )
        self.logger = logger

    def execute(self, context: dict) -> dict:
        dados_brutos = context.get("dados_brutos", {})

        if not dados_brutos:
            raise RuntimeError("Nenhum dado disponível para transformação.")

        transformer = Transformer(self.logger)
        dados_transformados = transformer.transformar(dados_brutos)

        total_transformado = sum(len(v) for v in dados_transformados.values())

        return {
            "dados_transformados": dados_transformados,
            "colecoes_transformadas": list(dados_transformados.keys()),
            "total_registros_transformados": total_transformado,
        }
