from agents.base_agent import BaseAgent, AgentStatus
from agents.extraction_agent import ExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.transformation_agent import TransformationAgent
from agents.loading_agent import LoadingAgent
from agents.monitoring_agent import MonitoringAgent


class OrchestratorAgent(BaseAgent):
    def __init__(self, groq_api_key: str):
        super().__init__(
            name="Agente Orquestrador",
            description="Coordena todos os sub-agentes em sequencia e gerencia o contexto compartilhado.",
        )
        self.sub_agentes = [
            ExtractionAgent(db_path="dados/sistema_a.db"),
            ValidationAgent(api_key=groq_api_key),
            TransformationAgent(),
            LoadingAgent(),
            MonitoringAgent(),
        ]

    def execute(self, context: dict) -> dict:
        relatorios = []
        pipeline_ok = True
        agentes_criticos = ("Extracao", "Validacao")

        for agente in self.sub_agentes:
            print(f"\n  [{agente.name}]")
            print(f"  {agente.description}")

            resultado = agente.run(context)
            relatorios.append(agente.report())

            if agente.status == AgentStatus.ERROR:
                print(f"  ERRO: {agente.error}")
                pipeline_ok = False
                if any(c in agente.name for c in agentes_criticos):
                    print("  Pipeline interrompido por agente critico.")
                    break
            else:
                context.update(resultado)

        context["agentes_executados"] = relatorios
        context["pipeline_ok"] = pipeline_ok
        return context
