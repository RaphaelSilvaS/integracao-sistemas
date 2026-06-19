import json
import os
from datetime import datetime

from agents.base_agent import BaseAgent


class MonitoringAgent(BaseAgent):
    """Sub-agente que consolida métricas e gera relatório final do pipeline."""

    def __init__(self):
        super().__init__(
            name="Agente de Monitoramento",
            description="Coleta métricas de todos os agentes e gera relatório consolidado em JSON.",
        )

    def execute(self, context: dict) -> dict:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        relatorio = {
            "pipeline": "ETL Multi-Agente — Firebase → Firebase",
            "timestamp": datetime.now().isoformat(),
            "sistema_origem": "Sistema A (Firebase Origem)",
            "sistema_destino": "Sistema B (Firebase Destino)",
            "etapas": {
                "extracao": {
                    "colecoes": context.get("colecoes_extraidas", []),
                    "total_registros": context.get("total_registros_extraidos", 0),
                },
                "validacao_ia": {
                    "qualidade_score": context.get("qualidade_score", 0),
                    "anomalias_detectadas": context.get("anomalias_detectadas", []),
                    "decisao": context.get("decisao_ia", "N/A"),
                    "detalhes": context.get("validacao_ia", {}),
                },
                "transformacao": {
                    "colecoes": context.get("colecoes_transformadas", []),
                    "total_registros": context.get("total_registros_transformados", 0),
                },
                "carga": {
                    "colecoes": context.get("colecoes_carregadas", []),
                    "total_registros": context.get("total_registros_carregados", 0),
                },
            },
            "agentes_executados": context.get("agentes_executados", []),
            "status_pipeline": "SUCESSO" if not context.get("pipeline_erro") else "ERRO",
        }

        os.makedirs("dados/relatorios", exist_ok=True)
        caminho = f"dados/relatorios/relatorio_{timestamp}.json"

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)

        self._imprimir_resumo(relatorio)

        return {
            "relatorio_gerado": caminho,
            "status_pipeline": relatorio["status_pipeline"],
        }

    def _imprimir_resumo(self, relatorio: dict) -> None:
        etapas = relatorio["etapas"]
        print("\n" + "=" * 60)
        print("  RELATÓRIO FINAL DO PIPELINE")
        print("=" * 60)
        print(f"  Status         : {relatorio['status_pipeline']}")
        print(f"  Sistema Origem : {relatorio['sistema_origem']}")
        print(f"  Sistema Destino: {relatorio['sistema_destino']}")
        print("-" * 60)
        print(f"  Extraídos      : {etapas['extracao']['total_registros']} registros")
        print(f"  Qualidade IA   : {etapas['validacao_ia']['qualidade_score']}/100")
        print(f"  Anomalias IA   : {len(etapas['validacao_ia']['anomalias_detectadas'])}")
        print(f"  Transformados  : {etapas['transformacao']['total_registros']} registros")
        print(f"  Carregados     : {etapas['carga']['total_registros']} registros")
        print("=" * 60)
