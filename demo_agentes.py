"""
Pipeline ETL Multi-Agente — Modo Demo (sem Firebase)

Sistema A: SQLite local  →  agentes  →  Sistema B: JSON local
Validação inteligente: Claude (Anthropic)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from agents.base_agent import AgentStatus
from agents.demo_extraction_agent import DemoExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.demo_transformation_agent import DemoTransformationAgent
from agents.demo_loading_agent import DemoLoadingAgent
from agents.monitoring_agent import MonitoringAgent


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        api_key = input("Chave da API Anthropic (Claude): ").strip()
        if not api_key:
            print("Chave da API é obrigatória.")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("  PIPELINE ETL MULTI-AGENTE — MODO DEMO")
    print("  Sistema A: SQLite local")
    print("  Sistema B: JSON local")
    print("  Validação IA: Claude (Anthropic)")
    print("=" * 60)

    agentes = [
        DemoExtractionAgent(db_path="dados/sistema_a.db"),
        ValidationAgent(api_key=api_key),
        DemoTransformationAgent(),
        DemoLoadingAgent(output_dir="dados/sistema_b"),
        MonitoringAgent(),
    ]

    context = {}
    relatorios = []
    pipeline_ok = True

    for agente in agentes:
        print(f"\n  [{agente.name}]")
        print(f"  {agente.description}")

        resultado = agente.run(context)
        relatorios.append(agente.report())

        if agente.status == AgentStatus.ERROR:
            print(f"  ERRO: {agente.error}")
            pipeline_ok = False
            agentes_criticos = ("Extração", "Validação")
            if any(c in agente.name for c in agentes_criticos):
                break
        else:
            context.update(resultado)

    context["agentes_executados"] = relatorios
    if not pipeline_ok:
        context["pipeline_erro"] = True

    print("\n" + "=" * 60)
    print("  SUMÁRIO DE EXECUÇÃO")
    print("=" * 60)
    for r in relatorios:
        icone = "OK  " if r["status"] == "success" else "ERRO"
        dur = f"{r['duration_seconds']}s" if r["duration_seconds"] is not None else "N/A"
        print(f"  [{icone}] {r['agent']:<38} {dur:>6}")
    print("=" * 60)

    if context.get("relatorio_gerado"):
        print(f"\n  Relatório: {context['relatorio_gerado']}")

    print(f"\n  Status final: {'SUCESSO' if pipeline_ok else 'ERRO'}\n")


if __name__ == "__main__":
    main()
