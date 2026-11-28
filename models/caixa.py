from datetime import datetime


class Caixa:
    """Representa um período de operação do caixa do EasyGest PDV."""

    def __init__(self, saldo_inicial, id=None):
        self.id = id
        self.saldo_inicial = self._valor_monetario(saldo_inicial)
        self.saldo_final = None
        self.total_vendas = 0.0
        self.total_dinheiro = 0.0
        self.total_cartao = 0.0
        self.total_pix = 0.0
        self.total_sangrias = 0.0
        self.vendas = []
        self.sangrias = []
        self.status = "ABERTO"
        self.data_abertura = datetime.now()
        self.data_fechamento = None

    @staticmethod
    def _valor_monetario(valor):
        try:
            valor = round(float(valor), 2)
        except (TypeError, ValueError):
            raise ValueError("Informe um valor monetário válido.")
        return valor

    @staticmethod
    def _obter_valor(objeto, *chaves, padrao=None):
        for chave in chaves:
            if isinstance(objeto, dict) and chave in objeto:
                return objeto[chave]
            if hasattr(objeto, chave):
                return getattr(objeto, chave)
        return padrao

    def registrar_venda(self, venda, pagamento):
        """Atualiza os totais do caixa a partir de uma venda e seu pagamento."""
        if self.status != "ABERTO":
            raise ValueError("Não é possível registrar venda em um caixa fechado.")

        valor = self._valor_monetario(
            self._obter_valor(venda, "valor_total", "total", "valor", padrao=0)
        )
        tipo = str(
            self._obter_valor(pagamento, "tipo", "forma_pagamento", "forma", padrao="")
        ).strip().upper()

        self.total_vendas = round(self.total_vendas + valor, 2)

        if "DINHEIRO" in tipo:
            self.total_dinheiro = round(self.total_dinheiro + valor, 2)
        elif "PIX" in tipo:
            self.total_pix = round(self.total_pix + valor, 2)
        elif "CART" in tipo or "CRÉDITO" in tipo or "CREDITO" in tipo or "DÉBITO" in tipo or "DEBITO" in tipo:
            self.total_cartao = round(self.total_cartao + valor, 2)

        identificador = self._obter_valor(venda, "id", "_id")
        if identificador is not None:
            self.vendas.append(str(identificador))

    def registrar_sangria(self, valor, justificativa, usuario=None):
        if self.status != "ABERTO":
            raise ValueError("Não é possível registrar sangria em um caixa fechado.")

        valor = self._valor_monetario(valor)
        if valor <= 0:
            raise ValueError("O valor da sangria deve ser maior que zero.")
        if valor > self.consultar_saldo():
            raise ValueError("O valor da sangria é maior que o saldo físico disponível.")
        if not str(justificativa).strip():
            raise ValueError("Informe a justificativa da sangria.")

        registro = {
            "valor": valor,
            "justificativa": str(justificativa).strip(),
            "data": datetime.now()
        }
        if usuario:
            registro["usuario"] = usuario
        self.sangrias.append(registro)
        self.total_sangrias = round(self.total_sangrias + valor, 2)
        return registro

    def consultar_saldo(self):
        return round(
            self.saldo_inicial + self.total_dinheiro - self.total_sangrias,
            2
        )

    def fechar_caixa(self):
        if self.status != "ABERTO":
            raise ValueError("Este caixa já está fechado.")
        self.saldo_final = self.consultar_saldo()
        self.data_fechamento = datetime.now()
        self.status = "FECHADO"
        return self.saldo_final

    def to_document(self):
        return {
            "saldo_inicial": self.saldo_inicial,
            "saldo_final": self.saldo_final,
            "total_vendas": self.total_vendas,
            "total_dinheiro": self.total_dinheiro,
            "total_cartao": self.total_cartao,
            "total_pix": self.total_pix,
            "total_sangrias": self.total_sangrias,
            "vendas": self.vendas,
            "sangrias": self.sangrias,
            "status": self.status,
            "data_abertura": self.data_abertura,
            "data_fechamento": self.data_fechamento
        }

    def __str__(self):
        return (
            f"Caixa | Status: {self.status} | "
            f"Saldo inicial: R$ {self.saldo_inicial:.2f} | "
            f"Saldo físico: R$ {self.consultar_saldo():.2f}"
        )
