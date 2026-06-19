from agents.base_agent import BaseAgent
from agents.extraction_agent import ExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.transformation_agent import TransformationAgent
from agents.loading_agent import LoadingAgent
from agents.monitoring_agent import MonitoringAgent


class OrchestratorAgent(BaseAgent):
    """
    Agente Orquestrador — coordena a execução sequencial de todos os sub-agentes
    e gerencia o contexto compartilhado entre eles.

    Fluxo:
        ExtractionAgent → ValidationAgent (IA) → TransformationAgent
        → LoadingAgent → MonitoringAgent
    """

    def __init__(self, config_origem: dict, config_destino: dict, logger, api_key: str):
        super().__init__(
            name="Agente Orquestrador",
            description="Coordena todos os sub-agentes do pipeline ETL multi-agente.",
        )
        self.logger = logger

        self.sub_agentes = [
            ExtractionAgent(config_origem, logger),
            ValidationAgent(api_key),
            TransformationAgent(logger),
            LoadingAgent(config_destino, logger),
            MonitoringAgent(),
        ]

    def execute(self, context: dict) -> dict:
        shared_context = dict(context)
        relatorios_agentes = []

        print("\n" + "=" * 60)
        print("  PIPELINE ETL MULTI-AGENTE")
        print("  Firebase (Sistema A) → Firebase (Sistema B)")
        print("  Validação por IA: Claude (Anthropic)")
        print("=" * 60)

        for agente in self.sub_agentes:
            print(f"\n  [{agente.name}]")
            print(f"  {agente.description}")
            print(f"  Executando...")

            resultado = agente.run(shared_context)
            relatorios_agentes.append(agente.report())

            if agente.status.value == "error":
                print(f"  ERRO: {agente.error}")
                shared_context["pipeline_erro"] = agente.error

                # Agentes críticos: extração e validação interrompem o pipeline
                if isinstance(agente, (ExtractionAgent, ValidationAgent)):
                    shared_context["agentes_executados"] = relatorios_agentes
                    MonitoringAgent().run(shared_context)
                    break
            else:
                shared_context.update(resultado)
                print(f"  Concluído.")

        shared_context["agentes_executados"] = relatorios_agentes
        return shared_context

    def imprimir_sumario(self) -> None:
        print("\n" + "=" * 60)
        print("  SUMÁRIO DE EXECUÇÃO DOS AGENTES")
        print("=" * 60)
        for agente in self.sub_agentes:
            r = agente.report()
            icone = "OK" if r["status"] == "success" else "ERRO"
            duracao = f"{r['duration_seconds']}s" if r["duration_seconds"] is not None else "N/A"
            print(f"  [{icone}] {r['agent']:<35} {duracao:>8}")
        print("=" * 60)
