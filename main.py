# main.py
# ============================================================
#  Ponto de entrada — Integração Firebase → Firebase
#  Projeto Integrador — Integração entre Sistemas com IA
# ============================================================

import sys
from src.logger import Logger
from src.integrator import Integrator
from config.settings import FIREBASE_ORIGEM, FIREBASE_DESTINO, LOG_DIR


def main():
    print("\n" + "="*60)
    print("  SISTEMA DE INTEGRAÇÃO DE DADOS — Firebase → Firebase")
    print("  Projeto Integrador | Integração entre Sistemas com IA")
    print("="*60 + "\n")

    # Inicializa o logger
    logger = Logger(log_dir=LOG_DIR)

    # Cria e executa o pipeline de integração
    integrator = Integrator(
        config_origem=FIREBASE_ORIGEM,
        config_destino=FIREBASE_DESTINO,
        logger=logger,
    )

    sucesso = integrator.executar()

    # Código de saída: 0 = sucesso, 1 = erro
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
