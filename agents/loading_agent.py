import json
import requests
from agents.base_agent import BaseAgent

FIREBASE_DB_URL = "https://projeto-integrador-303c5-default-rtdb.firebaseio.com"


class LoadingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Agente de Carga",
            description="Carrega os dados transformados no Firebase (Sistema B) via REST API.",
        )

    def execute(self, context: dict) -> dict:
        produtos = context.get("dados_transformados", [])
        if not produtos:
            raise RuntimeError("Nenhum dado transformado para carregar.")

        carregados = 0
        erros = 0

        for produto in produtos:
            resp = requests.post(
                f"{FIREBASE_DB_URL}/products.json",
                data=json.dumps(produto),
            )
            if resp.status_code == 200:
                carregados += 1
                print(f"    [OK] {produto['name']}")
            else:
                erros += 1
                print(f"    [ERRO] {produto['name']} — status {resp.status_code}")

        return {
            "total_carregado": carregados,
            "total_erro_carga": erros,
            "firebase_url": f"{FIREBASE_DB_URL}/products.json",
        }
