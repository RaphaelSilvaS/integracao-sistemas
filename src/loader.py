# src/loader.py
# ============================================================
#  Loader — carrega os dados transformados no Firebase DESTINO
# ============================================================

import requests
import json


class Loader:
    """
    Carrega os dados no Firebase Realtime Database de DESTINO.
    Suporta inserção e atualização (upsert) de registros.
    """

    def __init__(self, config: dict, logger):
        self.config = config
        self.logger = logger
        self.token = None

    # ----------------------------------------------------------
    #  Autenticação
    # ----------------------------------------------------------
    def autenticar(self) -> bool:
        """Autentica no Firebase destino e obtém o token."""
        self.logger.info(f"Autenticando no {self.config['nome']}...")

        url = (
            "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            f"?key={self.config['api_key']}"
        )

        payload = {
            "email": self.config["email"],
            "password": self.config["password"],
            "returnSecureToken": True,
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            data = response.json()

            if "idToken" in data:
                self.token = data["idToken"]
                self.logger.sucesso(f"Autenticado com sucesso no {self.config['nome']}")
                return True
            else:
                erro = data.get("error", {}).get("message", "Erro desconhecido")
                self.logger.erro(f"Falha na autenticação no destino: {erro}")
                return False

        except requests.exceptions.ConnectionError:
            self.logger.erro("Sem conexão ou URL do Firebase destino inválida.")
            return False
        except Exception as e:
            self.logger.erro(f"Erro inesperado na autenticação: {e}")
            return False

    # ----------------------------------------------------------
    #  Carga de uma coleção
    # ----------------------------------------------------------
    def carregar_colecao(self, colecao: str, registros: dict) -> int:
        """
        Carrega todos os registros de uma coleção no Firebase destino.
        Usa PUT por registro para preservar os IDs originais.

        Args:
            colecao:   Nome da coleção de destino
            registros: Dicionário { id: dados }

        Returns:
            Número de registros carregados com sucesso
        """
        if not self.token:
            self.logger.erro("Não autenticado. Chame autenticar() primeiro.")
            return 0

        if not registros:
            self.logger.aviso(f"Nenhum registro para carregar em '{colecao}'")
            return 0

        self.logger.info(
            f"Carregando {len(registros)} registros em '{colecao}' "
            f"no {self.config['nome']}..."
        )

        carregados = 0

        for id_registro, dados in registros.items():
            url = (
                f"{self.config['url']}/migrado/{colecao}/{id_registro}.json"
                f"?auth={self.token}"
            )

            try:
                response = requests.put(url, json=dados, timeout=10)

                if response.status_code == 200:
                    carregados += 1
                    self.logger.contadores["carregados"] += 1
                    self.logger.info(f"  ✔ Registro '{id_registro}' carregado")
                elif response.status_code == 401:
                    self.logger.erro(
                        "Token inválido ou sem permissão de escrita no destino."
                    )
                    break
                else:
                    self.logger.erro(
                        f"Erro HTTP {response.status_code} "
                        f"ao carregar '{id_registro}'"
                    )

            except requests.exceptions.Timeout:
                self.logger.erro(f"Timeout ao carregar registro '{id_registro}'")
            except Exception as e:
                self.logger.erro(f"Erro ao carregar '{id_registro}': {e}")

        self.logger.sucesso(
            f"'{colecao}': {carregados}/{len(registros)} registros carregados"
        )
        return carregados

    # ----------------------------------------------------------
    #  Carga completa
    # ----------------------------------------------------------
    def carregar_tudo(self, dados_transformados: dict) -> dict:
        """
        Carrega todas as coleções no Firebase destino.

        Returns:
            Dicionário { colecao: quantidade_carregada }
        """
        resultados = {}

        for colecao, registros in dados_transformados.items():
            total = self.carregar_colecao(colecao, registros)
            resultados[colecao] = total
            self.logger.separador()

        return resultados

    # ----------------------------------------------------------
    #  Salvar metadados da migração
    # ----------------------------------------------------------
    def salvar_metadados(self, resumo: dict):
        """
        Salva um resumo da migração no Firebase destino,
        permitindo rastreabilidade.
        """
        if not self.token:
            return

        url = (
            f"{self.config['url']}/migracoes.json"
            f"?auth={self.token}"
        )

        try:
            requests.post(url, json=resumo, timeout=10)
            self.logger.sucesso("Metadados da migração salvos no destino.")
        except Exception as e:
            self.logger.aviso(f"Não foi possível salvar metadados: {e}")
