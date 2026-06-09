# src/integrator.py
# ============================================================
#  Integrator — orquestra o pipeline completo ETL
#  Extract → Transform → Load
# ============================================================

from datetime import datetime
from src.extractor import Extractor
from src.transformer import Transformer
from src.loader import Loader


class Integrator:
    """
    Pipeline ETL completo:
      1. Extract  — extrai dados do Firebase ORIGEM
      2. Transform — valida e normaliza os dados
      3. Load      — carrega os dados no Firebase DESTINO
    """

    def __init__(self, config_origem: dict, config_destino: dict, logger):
        self.logger = logger
        self.extractor   = Extractor(config_origem, logger)
        self.transformer = Transformer(logger)
        self.loader      = Loader(config_destino, logger)
        self.inicio      = None

    # ----------------------------------------------------------
    #  Pipeline principal
    # ----------------------------------------------------------
    def executar(self) -> bool:
        """
        Executa o pipeline completo de integração.

        Returns:
            True se executou sem erros críticos, False caso contrário
        """
        self.inicio = datetime.now()

        self.logger.titulo("INTEGRAÇÃO FIREBASE → FIREBASE")
        self.logger.info(f"Início: {self.inicio.strftime('%d/%m/%Y %H:%M:%S')}")
        self.logger.separador()

        # ── ETAPA 1: AUTENTICAÇÃO ──────────────────────────────
        self.logger.titulo("ETAPA 1 — AUTENTICAÇÃO")

        if not self.extractor.autenticar():
            self.logger.erro("Falha na autenticação da ORIGEM. Abortando.")
            return False

        if not self.loader.autenticar():
            self.logger.erro("Falha na autenticação do DESTINO. Abortando.")
            return False

        self.logger.separador()

        # ── ETAPA 2: EXTRACT ──────────────────────────────────
        self.logger.titulo("ETAPA 2 — EXTRAÇÃO (ORIGEM → MEMÓRIA)")

        dados_brutos = self.extractor.extrair_tudo()

        if not dados_brutos:
            self.logger.aviso("Nenhum dado extraído da origem. Encerrando.")
            return False

        self.logger.separador()

        # ── ETAPA 3: TRANSFORM ────────────────────────────────
        self.logger.titulo("ETAPA 3 — TRANSFORMAÇÃO (MEMÓRIA → MEMÓRIA)")

        dados_transformados = self.transformer.transformar(dados_brutos)

        self.logger.separador()

        # ── ETAPA 4: LOAD ──────────────────────────────────────
        self.logger.titulo("ETAPA 4 — CARGA (MEMÓRIA → DESTINO)")

        resultados = self.loader.carregar_tudo(dados_transformados)

        # ── ETAPA 5: METADADOS ─────────────────────────────────
        fim = datetime.now()
        duracao = (fim - self.inicio).total_seconds()

        resumo = {
            "inicio":     self.inicio.isoformat(),
            "fim":        fim.isoformat(),
            "duracao_s":  round(duracao, 2),
            "colecoes":   resultados,
            "totais": {
                "extraidos":    self.logger.contadores["extraidos"],
                "transformados": self.logger.contadores["transformados"],
                "carregados":   self.logger.contadores["carregados"],
                "ignorados":    self.logger.contadores["ignorados"],
                "erros":        self.logger.contadores["erros"],
            },
        }

        self.loader.salvar_metadados(resumo)

        # ── RELATÓRIO FINAL ────────────────────────────────────
        self.logger.info(f"Duração total: {duracao:.2f} segundos")
        self.logger.relatorio_final()

        return self.logger.contadores["erros"] == 0
