
class Estoque:

    def __init__(
        self,
        produto_id,
        quantidade=0,
        quantidade_minima=0,
        id=None
    ):
        self.id = id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.quantidade_minima = quantidade_minima

    def adicionar_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser positiva.")

        self.quantidade += quantidade

    def retirar_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser positiva.")

        if quantidade > self.quantidade:
            raise ValueError("Estoque insuficiente.")

        self.quantidade -= quantidade

    def consultar_quantidade(self):
        return self.quantidade

    def verificar_estoque_baixo(self):
        return self.quantidade <= self.quantidade_minima

    def to_document(self):
        return {
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "quantidade_minima": self.quantidade_minima
        }

    def __str__(self):
        return (
            f"Produto ID: {self.produto_id} | "
            f"Quantidade: {self.quantidade} | "
            f"Mínimo: {self.quantidade_minima}"
        )
