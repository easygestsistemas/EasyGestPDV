
from abc import ABC, abstractmethod


class Pagamento(ABC):

    def __init__(self, valor_total):
        if valor_total <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        self.valor_total = round(valor_total, 2)
        self.status = "PENDENTE"

    @abstractmethod
    def processar(self):
        pass

    def consultar_status(self):
        return self.status

    def to_document(self):
        return {
            "tipo": self.__class__.__name__,
            "valor": self.valor_total,
            "status": self.status
        }
