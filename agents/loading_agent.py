import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.base_agent import BaseAgent
from src.loader import Loader


class LoadingAgent(BaseAgent):
    """Sub-agente responsável por carregar os dados transformados no Sistema B (Firebase Destino)."""

    def __init__(self, config_destino: dict, logger):
        super().__init__(
            name="Agente de Carga",
            description="Conecta ao Sistema B (Firebase Destino) e carrega todos os dados transformados.",
        )
        self.config_destino = config_destino
        self.logger = logger

    def execute(self, context: dict) -> dict:
        dados_transformados = context.get("dados_transformados", {})

        if not dados_transformados:
            raise RuntimeError("Nenhum dado transformado disponível para carga.")

        loader = Loader(self.config_destino, self.logger)

        if not loader.autenticar():
            raise RuntimeError("Falha na autenticação do Sistema B (Firebase Destino).")

        resultados = loader.carregar_tudo(dados_transformados)

        total_carregado = sum(
            r.get("carregados", 0) for r in resultados.values()
            if isinstance(r, dict)
        )

        return {
            "resultados_carga": resultados,
            "total_registros_carregados": total_carregado,
            "colecoes_carregadas": list(resultados.keys()),
        }
