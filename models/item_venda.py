
class ItemVenda:

    def __init__(self, produto, quantidade):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        if not produto.ativo:
            raise ValueError("Produto inativo não pode ser vendido.")

        self.produto_id = produto.id
        self.nome_produto = produto.nome
        self.quantidade = quantidade

        # Guarda o preço praticado no momento da venda
        self.valor_unitario = produto.preco_venda

        self.subtotal = self.calcular_subtotal()

    def calcular_subtotal(self):
        return round(self.quantidade * self.valor_unitario, 2)

    def to_document(self):
        return {
            "produto_id": self.produto_id,
            "nome_produto": self.nome_produto,
            "quantidade": self.quantidade,
            "valor_unitario": self.valor_unitario,
            "subtotal": self.subtotal
        }

    def __str__(self):
        return (
            f"{self.nome_produto} | "
            f"Quantidade: {self.quantidade} | "
            f"Subtotal: R$ {self.subtotal:.2f}"
        )
