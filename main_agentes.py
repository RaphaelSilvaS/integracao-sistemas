"""
Ponto de entrada do pipeline ETL Multi-Agente.

Sistemas:
  - Sistema A: Firebase Realtime Database (Origem)
  - Sistema B: Firebase Realtime Database (Destino)
  - Validação por IA: Claude (Anthropic)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from src.logger import Logger
from config.settings import FIREBASE_ORIGEM, FIREBASE_DESTINO
from agents.orchestrator_agent import OrchestratorAgent


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        api_key = input("Chave da API Anthropic (Claude): ").strip()
        if not api_key:
            print("Chave da API é obrigatória.")
            sys.exit(1)

    logger = Logger()

    orquestrador = OrchestratorAgent(
        config_origem=FIREBASE_ORIGEM,
        config_destino=FIREBASE_DESTINO,
        logger=logger,
        api_key=api_key,
    )

    orquestrador.run({})
    orquestrador.imprimir_sumario()


if __name__ == "__main__":
    main()
