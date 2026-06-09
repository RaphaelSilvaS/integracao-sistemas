# demo.py
# ============================================================
#  MODO DEMO — roda o pipeline completo sem Firebase
#  Usa arquivos JSON locais como origem e destino
#  Ideal para demonstracao e avaliacao do projeto
# ============================================================

import sys
import json
import os
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from src.transformer import Transformer
from src.logger import Logger


# ----------------------------------------------------------
#  Extractor local — le de demo/origem.json
# ----------------------------------------------------------
class DemoExtractor:
    """Simula o Extractor, mas le os dados de um arquivo JSON local."""

    def __init__(self, arquivo: str, logger):
        self.arquivo = arquivo
        self.logger = logger

    def autenticar(self) -> bool:
        self.logger.sucesso(f"[DEMO] Lendo dados locais de '{self.arquivo}'")
        return True

    def extrair_tudo(self) -> dict:
        self.logger.titulo("ETAPA 2 — EXTRACAO (arquivo local → memoria)")

        if not os.path.exists(self.arquivo):
            self.logger.erro(f"Arquivo '{self.arquivo}' nao encontrado.")
            return {}

        with open(self.arquivo, encoding="utf-8") as f:
            dados = json.load(f)

        for colecao, registros in dados.items():
            total = len(registros)
            self.logger.sucesso(f"'{colecao}': {total} registros carregados do JSON")
            self.logger.contadores["extraidos"] += total

        return dados


# ----------------------------------------------------------
#  Loader local — salva em demo/destino.json
# ----------------------------------------------------------
class DemoLoader:
    """Simula o Loader, mas grava os dados em um arquivo JSON local."""

    def __init__(self, arquivo: str, logger):
        self.arquivo = arquivo
        self.logger = logger

    def autenticar(self) -> bool:
        self.logger.sucesso(f"[DEMO] Destino configurado: '{self.arquivo}'")
        return True

    def carregar_tudo(self, dados_transformados: dict) -> dict:
        self.logger.titulo("ETAPA 4 — CARGA (memoria → arquivo local)")

        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)

        resultados = {}
        for colecao, registros in dados_transformados.items():
            total = len(registros)
            resultados[colecao] = total
            self.logger.sucesso(f"'{colecao}': {total} registros gravados")
            self.logger.contadores["carregados"] += total

        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_transformados, f, ensure_ascii=False, indent=2)

        self.logger.sucesso(f"Dados salvos em '{self.arquivo}'")
        return resultados

    def salvar_metadados(self, resumo: dict):
        metadados_path = self.arquivo.replace("destino.json", "metadados.json")
        with open(metadados_path, "w", encoding="utf-8") as f:
            json.dump(resumo, f, ensure_ascii=False, indent=2)
        self.logger.sucesso(f"Metadados salvos em '{metadados_path}'")


# ----------------------------------------------------------
#  Pipeline demo
# ----------------------------------------------------------
def main():
    print("\n" + "=" * 60)
    print("  MODO DEMO — Integracao entre Sistemas com IA")
    print("  Pipeline ETL: Sistema X (JSON) → Sistema Y (JSON)")
    print("=" * 60 + "\n")

    logger = Logger(log_dir="logs")
    inicio = datetime.now()

    # ── ETAPA 1: AUTENTICACAO ──────────────────────────────
    logger.titulo("ETAPA 1 — AUTENTICACAO")

    extractor = DemoExtractor("demo/origem.json", logger)
    loader    = DemoLoader("demo/destino.json", logger)

    if not extractor.autenticar():
        return sys.exit(1)
    if not loader.autenticar():
        return sys.exit(1)

    logger.separador()

    # ── ETAPA 2: EXTRACT ──────────────────────────────────
    dados_brutos = extractor.extrair_tudo()

    if not dados_brutos:
        logger.aviso("Nenhum dado extraido. Encerrando.")
        return sys.exit(1)

    logger.separador()

    # ── ETAPA 3: TRANSFORM ────────────────────────────────
    logger.titulo("ETAPA 3 — TRANSFORMACAO (validacao e normalizacao)")
    transformer = Transformer(logger)
    dados_transformados = transformer.transformar(dados_brutos)

    logger.separador()

    # ── ETAPA 4: LOAD ──────────────────────────────────────
    resultados = loader.carregar_tudo(dados_transformados)

    # ── ETAPA 5: METADADOS ─────────────────────────────────
    fim = datetime.now()
    duracao = (fim - inicio).total_seconds()

    resumo = {
        "modo":       "DEMO",
        "inicio":     inicio.isoformat(),
        "fim":        fim.isoformat(),
        "duracao_s":  round(duracao, 2),
        "colecoes":   resultados,
        "totais": {
            "extraidos":     logger.contadores["extraidos"],
            "transformados": logger.contadores["transformados"],
            "carregados":    logger.contadores["carregados"],
            "ignorados":     logger.contadores["ignorados"],
            "erros":         logger.contadores["erros"],
        },
    }

    loader.salvar_metadados(resumo)

    logger.info(f"Duracao total: {duracao:.2f} segundos")
    logger.relatorio_final()

    print("\n  Arquivos gerados:")
    print("    demo/destino.json   — dados migrados e validados")
    print("    demo/metadados.json — resumo da execucao\n")

    sys.exit(0 if logger.contadores["erros"] == 0 else 1)


if __name__ == "__main__":
    main()
