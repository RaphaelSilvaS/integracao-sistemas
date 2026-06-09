# src/extractor.py
# ============================================================
#  Extractor — responsável por extrair dados do Firebase ORIGEM
# ============================================================

import requests
import json


class Extractor:
    """
    Extrai dados do Firebase Realtime Database de ORIGEM.
    Utiliza a API REST do Firebase com autenticação via token.
    """

    def __init__(self, config: dict, logger):
        self.config = config
        self.logger = logger
        self.token = None

    # ----------------------------------------------------------
    #  Autenticação
    # ----------------------------------------------------------
    def autenticar(self) -> bool:
        """Autentica no Firebase e obtém o token de acesso."""
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
                self.logger.erro(f"Falha na autenticação: {erro}")
                return False

        except requests.exceptions.ConnectionError:
            self.logger.erro("Sem conexão com a internet ou URL inválida.")
            return False
        except Exception as e:
            self.logger.erro(f"Erro inesperado na autenticação: {e}")
            return False

    # ----------------------------------------------------------
    #  Extração de coleções
    # ----------------------------------------------------------
    def extrair_colecao(self, colecao: str) -> dict:
        """
        Extrai todos os registros de uma coleção do Firebase.

        Args:
            colecao: Nome da coleção (ex: 'products', 'orders')

        Returns:
            Dicionário com os dados extraídos ou {} em caso de erro
        """
        if not self.token:
            self.logger.erro("Não autenticado. Chame autenticar() primeiro.")
            return {}

        url = f"{self.config['url']}/{colecao}.json?auth={self.token}"

        self.logger.info(f"Extraindo coleção '{colecao}' do {self.config['nome']}...")

        try:
            response = requests.get(url, timeout=15)

            if response.status_code == 401:
                self.logger.erro("Token inválido ou sem permissão de leitura.")
                return {}

            if response.status_code != 200:
                self.logger.erro(f"Erro HTTP {response.status_code} ao extrair '{colecao}'")
                return {}

            dados = response.json()

            if dados is None:
                self.logger.aviso(f"Coleção '{colecao}' está vazia ou não existe.")
                return {}

            total = len(dados)
            self.logger.sucesso(f"'{colecao}': {total} registros extraídos")
            self.logger.contadores["extraidos"] += total

            return dados

        except requests.exceptions.Timeout:
            self.logger.erro(f"Timeout ao extrair coleção '{colecao}'")
            return {}
        except json.JSONDecodeError:
            self.logger.erro(f"Resposta inválida (não é JSON) para '{colecao}'")
            return {}
        except Exception as e:
            self.logger.erro(f"Erro ao extrair '{colecao}': {e}")
            return {}

    # ----------------------------------------------------------
    #  Extração completa (todas as coleções configuradas)
    # ----------------------------------------------------------
    def extrair_tudo(self) -> dict:
        """
        Extrai todas as coleções definidas em config['colecoes'].

        Returns:
            Dicionário no formato { "colecao": { dados } }
        """
        resultado = {}

        for colecao in self.config.get("colecoes", []):
            dados = self.extrair_colecao(colecao)
            if dados:
                resultado[colecao] = dados

        return resultado
