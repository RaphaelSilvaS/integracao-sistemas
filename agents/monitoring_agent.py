import json
import os
from datetime import datetime
from agents.base_agent import BaseAgent


class MonitoringAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Agente de Monitoramento",
            description="Consolida metricas e gera relatorio final do pipeline.",
        )

    def execute(self, context: dict) -> dict:
        relatorio = {
            "timestamp": datetime.now().isoformat(),
            "pipeline": "Sistema A (SQLite) -> Validacao IA (Groq/Llama) -> Sistema B (Firebase)",
            "metricas": {
                "extraidos": context.get("total_extraido", 0),
                "qualidade_score": context.get("qualidade_score", 0),
                "anomalias": context.get("anomalias_detectadas", []),
                "transformados": context.get("total_transformado", 0),
                "invalidos": context.get("total_invalido", 0),
                "carregados": context.get("total_carregado", 0),
                "erros_carga": context.get("total_erro_carga", 0),
            },
            "decisao_ia": context.get("decisao_ia", "N/A"),
            "firebase_destino": context.get("firebase_url", "N/A"),
        }

        os.makedirs("dados/relatorios", exist_ok=True)
        nome = f"dados/relatorios/relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(nome, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)

        print(f"    Relatorio salvo: {nome}")
        return {"relatorio_gerado": nome, "metricas_finais": relatorio["metricas"]}
