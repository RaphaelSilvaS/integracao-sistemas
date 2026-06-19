import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.base_agent import BaseAgent
from src.extractor import Extractor


class ExtractionAgent(BaseAgent):
    """Sub-agente responsável por extrair dados do Sistema A (Firebase Origem)."""

    def __init__(self, config_origem: dict, logger):
        super().__init__(
            name="Agente de Extração",
            description="Conecta ao Sistema A (Firebase Origem) e extrai todas as coleções.",
        )
        self.config_origem = config_origem
        self.logger = logger
        self._extractor = None

    def execute(self, context: dict) -> dict:
        self._extractor = Extractor(self.config_origem, self.logger)

        if not self._extractor.autenticar():
            raise RuntimeError("Falha na autenticação do Sistema A (Firebase Origem).")

        dados_brutos = self._extractor.extrair_tudo()

        if not dados_brutos:
            raise RuntimeError("Nenhum dado extraído do Sistema A.")

        total = sum(len(v) for v in dados_brutos.values())
        colecoes = list(dados_brutos.keys())

        return {
            "dados_brutos": dados_brutos,
            "colecoes_extraidas": colecoes,
            "total_registros_extraidos": total,
        }
