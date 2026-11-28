
from models.pagamento import Pagamento


class Cartao(Pagamento):

    def __init__(self, valor_total, parcelas=1):
        super().__init__(valor_total)

        if parcelas < 1 or parcelas > 12:
            raise ValueError("O parcelamento deve ser de 1 a 12 vezes.")

        self.parcelas = parcelas
        self.valor_parcela = round(
            self.valor_total / self.parcelas, 2
        )

    def calcular_parcelas(self):
        return self.valor_parcela

    def processar(self):
        # Simulação de aprovação do cartão
        self.status = "APROVADO"
        return self.status

    def to_document(self):
        documento = super().to_document()

        documento.update({
            "parcelas": self.parcelas,
            "valor_parcela": self.valor_parcela
        })

        return documento

    def __str__(self):
        return (
            f"Pagamento com cartão | "
            f"Total: R$ {self.valor_total:.2f} | "
            f"Parcelas: {self.parcelas}x de "
            f"R$ {self.valor_parcela:.2f}"
        )
