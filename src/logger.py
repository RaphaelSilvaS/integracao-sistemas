# src/logger.py
# ============================================================
#  Sistema de Logs — registra todas as operações da integração
# ============================================================

import os
import logging
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)


class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"integracao_{timestamp}.log")

        # Configura o logger
        self.logger = logging.getLogger("integracao_firebase")
        self.logger.setLevel(logging.DEBUG)

        # Handler para arquivo (sem cores)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        self.logger.addHandler(fh)

        self.log_file = log_file
        self.contadores = {
            "extraidos": 0,
            "transformados": 0,
            "carregados": 0,
            "erros": 0,
            "ignorados": 0,
        }

    def _print(self, cor, prefixo, msg):
        hora = datetime.now().strftime("%H:%M:%S")
        print(f"{cor}[{hora}] {prefixo} {msg}{Style.RESET_ALL}")

    def info(self, msg):
        self._print(Fore.CYAN, "ℹ️ ", msg)
        self.logger.info(msg)

    def sucesso(self, msg):
        self._print(Fore.GREEN, "✅", msg)
        self.logger.info(f"[SUCESSO] {msg}")

    def aviso(self, msg):
        self._print(Fore.YELLOW, "⚠️ ", msg)
        self.logger.warning(msg)

    def erro(self, msg):
        self._print(Fore.RED, "❌", msg)
        self.logger.error(msg)
        self.contadores["erros"] += 1

    def titulo(self, msg):
        linha = "=" * 60
        print(f"\n{Fore.MAGENTA}{linha}")
        print(f"  {msg}")
        print(f"{linha}{Style.RESET_ALL}\n")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"  {msg}")
        self.logger.info(f"{'='*60}")

    def separador(self):
        print(f"{Fore.WHITE}{'-' * 60}{Style.RESET_ALL}")
        self.logger.info("-" * 60)

    def relatorio_final(self):
        self.titulo("RELATÓRIO FINAL DA INTEGRAÇÃO")
        dados = [
            ("Registros extraídos",    self.contadores["extraidos"],    Fore.CYAN),
            ("Registros transformados", self.contadores["transformados"], Fore.BLUE),
            ("Registros carregados",   self.contadores["carregados"],   Fore.GREEN),
            ("Registros ignorados",    self.contadores["ignorados"],    Fore.YELLOW),
            ("Erros encontrados",      self.contadores["erros"],        Fore.RED),
        ]
        for label, valor, cor in dados:
            print(f"  {cor}{label}: {Style.BRIGHT}{valor}{Style.RESET_ALL}")
            self.logger.info(f"{label}: {valor}")

        taxa = 0
        if self.contadores["extraidos"] > 0:
            taxa = (self.contadores["carregados"] / self.contadores["extraidos"]) * 100

        print(f"\n  {Fore.MAGENTA}Taxa de sucesso: {Style.BRIGHT}{taxa:.1f}%{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Log salvo em: {self.log_file}{Style.RESET_ALL}\n")
        self.logger.info(f"Taxa de sucesso: {taxa:.1f}%")
        self.logger.info(f"Log salvo em: {self.log_file}")
