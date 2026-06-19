"""
Pipeline ETL Multi-Agente com IA
Sistema A (SQLite) -> Validacao IA (Groq/Llama) -> Sistema B (Firebase)

Uso:
    python pipeline.py
"""

import os
import sys
from dotenv import load_dotenv
from agents.orchestrator_agent import OrchestratorAgent

load_dotenv()


def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        api_key = input("Chave da API Groq: ").strip()
        if not api_key:
            print("Chave obrigatoria.")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("  PIPELINE ETL MULTI-AGENTE COM IA")
    print("  Sistema A: SQLite local")
    print("  Validacao: Groq (Llama 3 — gratuito)")
    print("  Sistema B: Firebase Realtime Database")
    print("=" * 60)

    orquestrador = OrchestratorAgent(groq_api_key=api_key)
    context = {}
    orquestrador.run(context)

    relatorios = context.get("agentes_executados", [])
    pipeline_ok = context.get("pipeline_ok", False)

    print("\n" + "=" * 60)
    print("  SUMARIO DE EXECUCAO")
    print("=" * 60)
    for r in relatorios:
        status = "OK  " if r["status"] == "success" else "ERRO"
        dur = f"{r['duration_seconds']}s" if r["duration_seconds"] else "N/A"
        print(f"  [{status}] {r['agent']:<38} {dur:>6}")

    metricas = context.get("metricas_finais", {})
    if metricas:
        print(f"\n  Extraidos:    {metricas.get('extraidos', 0)}")
        print(f"  Score IA:     {metricas.get('qualidade_score', 0)}/100")
        print(f"  Transformados:{metricas.get('transformados', 0)}")
        print(f"  Carregados:   {metricas.get('carregados', 0)}")

    print("=" * 60)
    print(f"\n  Status: {'SUCESSO' if pipeline_ok else 'ERRO'}\n")


if __name__ == "__main__":
    main()
