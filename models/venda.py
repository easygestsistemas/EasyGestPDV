
from datetime import datetime


class Venda:

    def __init__(self, caixa_id=None, id=None):
        self.id = id
        self.caixa_id = caixa_id
        self.data = datetime.now()
        self.itens = []
        self.valor_total = 0.0
        self.status = "PENDENTE"

    def adicionar_item(self, item):
        self.itens.append(item)
        self.calcular_total()

    def remover_item(self, indice):
        if indice < 0 or indice >= len(self.itens):
            raise IndexError("Item não encontrado.")

        self.itens.pop(indice)
        self.calcular_total()

    def calcular_total(self):
        self.valor_total = round(
            sum(item.subtotal for item in self.itens), 2
        )

        return self.valor_total

    def consultar_itens(self):
        return self.itens

    def finalizar(self):
        if not self.itens:
            raise ValueError("Não é possível finalizar uma venda vazia.")

        self.calcular_total()
        self.status = "FINALIZADA"

    def cancelar(self):
        self.status = "CANCELADA"

    def to_document(self):
        return {
            "caixa_id": self.caixa_id,
            "data": self.data,
            "itens": [
                item.to_document() for item in self.itens
            ],
            "valor_total": self.valor_total,
            "status": self.status
        }

    def __str__(self):
        return (
            f"Venda | "
            f"Itens: {len(self.itens)} | "
            f"Total: R$ {self.valor_total:.2f} | "
            f"Status: {self.status}"
        )
