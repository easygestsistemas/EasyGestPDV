
from models.pagamento import Pagamento


class Dinheiro(Pagamento):

    def __init__(self, valor_total, valor_recebido):
        super().__init__(valor_total)

        if valor_recebido < self.valor_total:
            raise ValueError("Valor recebido insuficiente.")

        self.valor_recebido = round(valor_recebido, 2)
        self.troco = round(
            self.valor_recebido - self.valor_total, 2
        )

    def processar(self):
        self.status = "APROVADO"
        return self.status

    def to_document(self):
        documento = super().to_document()

        documento.update({
            "valor_recebido": self.valor_recebido,
            "troco": self.troco
        })

        return documento

    def __str__(self):
        return (
            f"Pagamento em dinheiro | "
            f"Total: R$ {self.valor_total:.2f} | "
            f"Recebido: R$ {self.valor_recebido:.2f} | "
            f"Troco: R$ {self.troco:.2f}"
        )
