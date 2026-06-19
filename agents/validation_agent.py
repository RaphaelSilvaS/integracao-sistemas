import json
import re
import anthropic

from agents.base_agent import BaseAgent


class ValidationAgent(BaseAgent):
    """Sub-agente que usa IA (Claude) para analisar a qualidade dos dados extraídos."""

    def __init__(self, api_key: str):
        super().__init__(
            name="Agente de Validação IA",
            description="Usa Claude (Anthropic) para detectar anomalias e avaliar qualidade dos dados.",
        )
        self.client = anthropic.Anthropic(api_key=api_key)

    def execute(self, context: dict) -> dict:
        dados_brutos = context.get("dados_brutos", {})

        if not dados_brutos:
            raise RuntimeError("Nenhum dado disponível para validação.")

        # Prepara amostra para não exceder tokens
        amostra = {}
        for colecao, registros in dados_brutos.items():
            amostra[colecao] = registros[:5] if isinstance(registros, list) else registros

        prompt = f"""Você é um agente especializado em validação de dados para pipelines ETL.

Analise a amostra de dados abaixo, extraída do Sistema A (Firebase), e retorne uma avaliação estruturada.

DADOS EXTRAÍDOS:
{json.dumps(amostra, ensure_ascii=False, indent=2)}

Identifique:
1. Anomalias e inconsistências (campos vazios, valores negativos, tipos incorretos)
2. Score de qualidade geral dos dados (0 a 100)
3. Se o pipeline deve prosseguir ou ser interrompido

Responda APENAS com um JSON válido neste formato exato:
{{
  "qualidade_score": <inteiro 0-100>,
  "anomalias": ["lista de anomalias encontradas"],
  "colecoes_avaliadas": ["lista de coleções analisadas"],
  "decisao": "prosseguir" ou "interromper",
  "justificativa": "<motivo da decisão em português>"
}}"""

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        texto = response.content[0].text
        match = re.search(r"\{.*\}", texto, re.DOTALL)
        if not match:
            raise RuntimeError("IA retornou resposta em formato inesperado.")

        analise = json.loads(match.group())

        if analise.get("decisao") == "interromper":
            raise RuntimeError(
                f"Validação IA interrompeu o pipeline: {analise.get('justificativa')}"
            )

        return {
            "validacao_ia": analise,
            "qualidade_score": analise.get("qualidade_score", 0),
            "anomalias_detectadas": analise.get("anomalias", []),
            "decisao_ia": analise.get("decisao", "prosseguir"),
        }
