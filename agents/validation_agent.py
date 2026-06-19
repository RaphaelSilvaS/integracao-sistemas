import json
import re
from groq import Groq
from agents.base_agent import BaseAgent


class ValidationAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(
            name="Agente de Validacao IA",
            description="Usa IA (Groq/Llama) para detectar anomalias e avaliar qualidade dos dados.",
        )
        self.client = Groq(api_key=api_key)

    def execute(self, context: dict) -> dict:
        dados = context.get("dados_brutos", {})
        if not dados:
            raise RuntimeError("Nenhum dado disponivel para validacao.")

        amostra = {
            col: registros[:5] if isinstance(registros, list) else registros
            for col, registros in dados.items()
        }

        prompt = f"""Voce e um agente especializado em validacao de dados para pipelines ETL.

Analise os dados abaixo extraidos do Sistema A e retorne uma avaliacao estruturada.

DADOS EXTRAIDOS:
{json.dumps(amostra, ensure_ascii=False, indent=2)}

Identifique:
1. Anomalias e inconsistencias (campos vazios, valores negativos, tipos incorretos)
2. Score de qualidade geral dos dados (0 a 100)
3. Se o pipeline deve prosseguir ou ser interrompido

Responda APENAS com um JSON valido neste formato exato:
{{
  "qualidade_score": <inteiro 0-100>,
  "anomalias": ["lista de anomalias encontradas"],
  "colecoes_avaliadas": ["lista de colecoes analisadas"],
  "decisao": "prosseguir",
  "justificativa": "<motivo da decisao em portugues>"
}}"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )

        texto = response.choices[0].message.content
        match = re.search(r"\{.*\}", texto, re.DOTALL)
        if not match:
            raise RuntimeError("IA retornou resposta em formato inesperado.")

        analise = json.loads(match.group())
        print(f"    Score de qualidade: {analise.get('qualidade_score')}/100")
        print(f"    Decisao IA: {analise.get('decisao')}")
        if analise.get("anomalias"):
            for a in analise["anomalias"]:
                print(f"    - Anomalia: {a}")

        if analise.get("decisao") == "interromper":
            raise RuntimeError(
                f"IA interrompeu o pipeline: {analise.get('justificativa')}"
            )

        return {
            "validacao_ia": analise,
            "qualidade_score": analise.get("qualidade_score", 0),
            "anomalias_detectadas": analise.get("anomalias", []),
            "decisao_ia": analise.get("decisao", "prosseguir"),
        }
