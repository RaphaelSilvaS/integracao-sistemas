# tests/test_integration.py
# ============================================================
#  Testes automatizados — valida as regras de transformação
# ============================================================

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.transformer import Transformer
from src.logger import Logger


def criar_logger():
    return Logger(log_dir="logs/tests")


# ----------------------------------------------------------
#  Testes de Produto
# ----------------------------------------------------------
class TestTransformerProduto:

    def setup_method(self):
        self.logger = criar_logger()
        self.transformer = Transformer(self.logger)

    def test_produto_valido(self):
        dados = {
            "name": "Camiseta",
            "description": "Camiseta azul tamanho M",
            "price": 49.90,
            "imageURL": "https://exemplo.com/img.jpg",
        }
        resultado = self.transformer._transformar_produtos("id1", dados)
        assert resultado is not None
        assert resultado["name"] == "Camiseta"
        assert resultado["price"] == 49.90
        assert resultado["_sistema"] == "Sistema X"
        assert "_migrado_em" in resultado
        print("✅ test_produto_valido passou")

    def test_produto_sem_nome(self):
        dados = {
            "name": "",
            "description": "Descrição qualquer",
            "price": 10.0,
            "imageURL": "https://exemplo.com/img.jpg",
        }
        resultado = self.transformer._transformar_produtos("id2", dados)
        assert resultado is None
        print("✅ test_produto_sem_nome passou")

    def test_produto_preco_negativo(self):
        dados = {
            "name": "Produto X",
            "description": "Descrição qualquer",
            "price": -5.0,
            "imageURL": "https://exemplo.com/img.jpg",
        }
        resultado = self.transformer._transformar_produtos("id3", dados)
        assert resultado is None
        print("✅ test_produto_preco_negativo passou")

    def test_produto_preco_texto(self):
        dados = {
            "name": "Produto Y",
            "description": "Descrição válida",
            "price": "abc",
            "imageURL": "https://exemplo.com/img.jpg",
        }
        resultado = self.transformer._transformar_produtos("id4", dados)
        assert resultado is None
        print("✅ test_produto_preco_texto passou")

    def test_produto_normaliza_espacos(self):
        dados = {
            "name": "  Calça Jeans  ",
            "description": "  Jeans slim fit  ",
            "price": 99.99,
            "imageURL": "  https://exemplo.com/img.jpg  ",
        }
        resultado = self.transformer._transformar_produtos("id5", dados)
        assert resultado is not None
        assert resultado["name"] == "Calça Jeans"
        assert resultado["description"] == "Jeans slim fit"
        print("✅ test_produto_normaliza_espacos passou")


# ----------------------------------------------------------
#  Testes de Pedido
# ----------------------------------------------------------
class TestTransformerPedido:

    def setup_method(self):
        self.logger = criar_logger()
        self.transformer = Transformer(self.logger)

    def test_pedido_valido(self):
        dados = {
            "total": 149.90,
            "date": "2024-01-15T10:30:00",
            "products": [
                {"id": "p1", "productId": "abc", "name": "Camiseta", "quantity": 2, "price": 49.90},
                {"id": "p2", "productId": "def", "name": "Calça",    "quantity": 1, "price": 50.10},
            ],
        }
        resultado = self.transformer._transformar_pedidos("ord1", dados)
        assert resultado is not None
        assert resultado["total"] == 149.90
        assert len(resultado["products"]) == 2
        print("✅ test_pedido_valido passou")

    def test_pedido_sem_produtos(self):
        dados = {
            "total": 50.0,
            "date": "2024-01-15T10:30:00",
            "products": [],
        }
        resultado = self.transformer._transformar_pedidos("ord2", dados)
        assert resultado is None
        print("✅ test_pedido_sem_produtos passou")

    def test_pedido_total_zero(self):
        dados = {
            "total": 0,
            "date": "2024-01-15T10:30:00",
            "products": [{"id": "p1", "productId": "abc", "name": "X", "quantity": 1, "price": 10}],
        }
        resultado = self.transformer._transformar_pedidos("ord3", dados)
        assert resultado is None
        print("✅ test_pedido_total_zero passou")


# ----------------------------------------------------------
#  Executar testes manualmente
# ----------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  EXECUTANDO TESTES DE INTEGRAÇÃO")
    print("="*50 + "\n")

    # Testes de produto
    print("📦 Testes de Produto:")
    tp = TestTransformerProduto()
    for metodo in [m for m in dir(tp) if m.startswith("test_")]:
        tp.setup_method()
        try:
            getattr(tp, metodo)()
        except AssertionError as e:
            print(f"❌ {metodo} FALHOU: {e}")
        except Exception as e:
            print(f"❌ {metodo} ERRO: {e}")

    print("\n🛒 Testes de Pedido:")
    to = TestTransformerPedido()
    for metodo in [m for m in dir(to) if m.startswith("test_")]:
        to.setup_method()
        try:
            getattr(to, metodo)()
        except AssertionError as e:
            print(f"❌ {metodo} FALHOU: {e}")
        except Exception as e:
            print(f"❌ {metodo} ERRO: {e}")

    print("\n✅ Todos os testes concluídos!\n")
