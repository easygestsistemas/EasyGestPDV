
from models.pagamento import Pagamento


class PIX(Pagamento):

    def __init__(self, valor_total, identificador_transacao):
        super().__init__(valor_total)

        if not identificador_transacao:
            raise ValueError("Informe o identificador da transação.")

        self.identificador_transacao = identificador_transacao

    def processar(self):
        # Simulação de confirmação do PIX
        self.status = "APROVADO"
        return self.status

    def to_document(self):
        documento = super().to_document()

        documento.update({
            "identificador_transacao": self.identificador_transacao
        })

        return documento

    def __str__(self):
        return (
            f"Pagamento via PIX | "
            f"Total: R$ {self.valor_total:.2f} | "
            f"Transação: {self.identificador_transacao}"
        )
