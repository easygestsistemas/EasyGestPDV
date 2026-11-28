class Produto:
    def __init__(self, nome, descricao, codigo_barras, preco_venda, custo = 0, ativo = True, id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.codigo_barras = codigo_barras
        self.preco_venda = preco_venda
        self.custo = custo
        self.ativo = ativo

    def atualizar_preco(self, novo_preco):
        if novo_preco <= 0:
            raise ValueError("O preço deve ser maior que zero.")

        self.preco_venda = novo_preco

    def ativar(self):
        self.ativo = True

    def desativar(self):
        self.ativo = False

    def consultar_preco(self):
        return self.preco_venda

    def to_document(self):
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "codigo_barras": self.codigo_barras,
            "preco_venda": self.preco_venda,
            "custo": self.custo,
            "ativo": self.ativo
        }

    def __str__(self):
        return (
            f"Produto: {self.nome} | "
            f"Preço: R$ {self.preco_venda:.2f} | "
            f"Ativo: {self.ativo}"
        )