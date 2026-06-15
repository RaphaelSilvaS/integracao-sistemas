# src/transformer.py
# ============================================================
#  Transformer — transforma, valida e normaliza os dados
#  antes de enviá-los ao Firebase DESTINO
# ============================================================

from datetime import datetime


class Transformer:
    """
    Responsável pela transformação e validação dos dados extraídos.
    Garante que os dados estejam no formato correto antes da carga.
    """

    def __init__(self, logger):
        self.logger = logger

    # ----------------------------------------------------------
    #  Orquestrador principal
    # ----------------------------------------------------------
    def transformar(self, dados_brutos: dict) -> dict:
        """
        Transforma todas as coleções extraídas.

        Args:
            dados_brutos: { "colecao": { id: registro } }

        Returns:
            Dados transformados no mesmo formato
        """
        self.logger.titulo("ETAPA 2 — TRANSFORMAÇÃO DOS DADOS")
        dados_transformados = {}

        transformadores = {
            "products": self._transformar_produtos,
            "orders":   self._transformar_pedidos,
        }

        for colecao, registros in dados_brutos.items():
            self.logger.info(f"Transformando coleção '{colecao}'...")

            fn = transformadores.get(colecao, self._transformar_generico)
            resultado = {}
            ignorados = 0

            for id_registro, dados in registros.items():
                try:
                    registro_transformado = fn(id_registro, dados)
                    if registro_transformado:
                        resultado[id_registro] = registro_transformado
                        self.logger.contadores["transformados"] += 1
                    else:
                        ignorados += 1
                        self.logger.contadores["ignorados"] += 1
                except Exception as e:
                    self.logger.erro(f"Erro ao transformar registro '{id_registro}': {e}")
                    ignorados += 1
                    self.logger.contadores["ignorados"] += 1

            dados_transformados[colecao] = resultado
            self.logger.sucesso(
                f"'{colecao}': {len(resultado)} transformados, {ignorados} ignorados"
            )

        return dados_transformados

    # ----------------------------------------------------------
    #  Transformação de Produtos
    # ----------------------------------------------------------
    def _transformar_produtos(self, id_registro: str, dados: dict):
        """
        Valida e normaliza um registro de produto.
        Regras:
          - name, description, imageURL são obrigatórios
          - price deve ser numérico e positivo
          - Adiciona metadado de migração
        """
        erros = []

        # Validações obrigatórias
        if not dados.get("name", "").strip():
            erros.append("campo 'name' vazio")
        if not dados.get("description", "").strip():
            erros.append("campo 'description' vazio")
        if not dados.get("imageURL", "").strip():
            erros.append("campo 'imageURL' vazio")

        # Validação de preço
        try:
            price = float(dados.get("price", 0))
            if price <= 0:
                erros.append("'price' deve ser maior que zero")
        except (ValueError, TypeError):
            erros.append("'price' não é numérico")
            price = 0.0

        if erros:
            self.logger.aviso(f"Produto '{id_registro}' ignorado: {', '.join(erros)}")
            return None

        # Retorna registro normalizado com metadados de migração
        return {
            "name":        dados["name"].strip(),
            "description": dados["description"].strip(),
            "price":       round(price, 2),
            "imageURL":    dados["imageURL"].strip(),
            "isFavorite":  bool(dados.get("isFavorite", False)),
            "_migrado_em": datetime.now().isoformat(),
            "_origem_id":  id_registro,
            "_sistema":    "Sistema 1",
        }

    # ----------------------------------------------------------
    #  Transformação de Pedidos
    # ----------------------------------------------------------
    def _transformar_pedidos(self, id_registro: str, dados: dict):
        """
        Valida e normaliza um registro de pedido.
        Regras:
          - total deve ser numérico e positivo
          - products deve ser uma lista não vazia
          - date deve ser uma string de data válida
        """
        erros = []

        # Validação do total
        try:
            total = float(dados.get("total", 0))
            if total <= 0:
                erros.append("'total' deve ser maior que zero")
        except (ValueError, TypeError):
            erros.append("'total' não é numérico")
            total = 0.0

        # Validação dos produtos
        produtos = dados.get("products", [])
        if not isinstance(produtos, list) or len(produtos) == 0:
            erros.append("'products' deve ser uma lista não vazia")

        # Validação da data
        data_str = dados.get("date", "")
        try:
            datetime.fromisoformat(data_str)
        except (ValueError, TypeError):
            erros.append(f"'date' inválida: '{data_str}'")
            data_str = datetime.now().isoformat()

        if erros:
            self.logger.aviso(f"Pedido '{id_registro}' ignorado: {', '.join(erros)}")
            return None

        # Normaliza cada item do pedido
        produtos_normalizados = []
        for item in produtos:
            try:
                produtos_normalizados.append({
                    "id":        item.get("id", ""),
                    "productId": item.get("productId", ""),
                    "name":      str(item.get("name", "")).strip(),
                    "quantity":  int(item.get("quantity", 1)),
                    "price":     round(float(item.get("price", 0)), 2),
                })
            except Exception:
                pass  # Item malformado é simplesmente ignorado

        return {
            "total":       round(total, 2),
            "date":        data_str,
            "products":    produtos_normalizados,
            "_migrado_em": datetime.now().isoformat(),
            "_origem_id":  id_registro,
            "_sistema":    "Sistema 1",
        }

    # ----------------------------------------------------------
    #  Transformação Genérica (coleções não mapeadas)
    # ----------------------------------------------------------
    def _transformar_generico(self, id_registro: str, dados: dict):
        """
        Para coleções sem transformação específica,
        apenas adiciona metadados de migração.
        """
        if not isinstance(dados, dict):
            self.logger.aviso(f"Registro '{id_registro}' não é um objeto — ignorado.")
            return None

        return {
            **dados,
            "_migrado_em": datetime.now().isoformat(),
            "_origem_id":  id_registro,
            "_sistema":    "Sistema 1",
        }
