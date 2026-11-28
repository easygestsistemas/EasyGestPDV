
import tkinter as tk
from tkinter import ttk, messagebox
from telas.pagamento import TelaPagamento
from models.item_venda import ItemVenda
from models.venda import Venda
from models.dinheiro import Dinheiro
from models.cartao import Cartao
from models.pix import PIX
from telas.usuarios import TelaUsuarios


class TelaPDV:

    def __init__(self, parent, banco):
        self.parent = parent
        self.produtos = banco["produtos"]
        self.estoques = banco["estoques"]
        self.banco = banco

        self.venda = Venda()
        self.itens_carrinho = []

        self.criar_interface()
        self.carregar_produtos()

    def criar_interface(self):

        titulo = tk.Label(
            self.parent,
            text="Frente de Caixa",
            font=("Arial", 20, "bold"),
            bg="#F3F5F9",
            fg="#193B65"
        )
        titulo.pack(anchor="w", pady=(0, 20))

        area_produto = tk.LabelFrame(
            self.parent,
            text="Adicionar produto",
            bg="#F3F5F9",
            padx=15,
            pady=15
        )
        area_produto.pack(fill="x", pady=5)

        tk.Label(
            area_produto,
            text="Produto:",
            bg="#F3F5F9"
        ).grid(row=0, column=0, sticky="w")

        self.combo_produtos = ttk.Combobox(
            area_produto,
            state="readonly",
            width=45
        )
        self.combo_produtos.grid(
            row=1, column=0, padx=(0, 15), pady=5
        )

        tk.Label(
            area_produto,
            text="Quantidade:",
            bg="#F3F5F9"
        ).grid(row=0, column=1, sticky="w")

        self.campo_quantidade = ttk.Entry(
            area_produto,
            width=12
        )
        self.campo_quantidade.insert(0, "1")
        self.campo_quantidade.grid(
            row=1, column=1, padx=(0, 15), pady=5
        )

        tk.Button(
            area_produto,
            text="Adicionar",
            bg="#193B65",
            fg="white",
            relief="flat",
            padx=15,
            command=self.adicionar_item
        ).grid(row=1, column=2, pady=5)

        area_carrinho = tk.LabelFrame(
            self.parent,
            text="Itens da venda",
            bg="#F3F5F9",
            padx=15,
            pady=15
        )
        area_carrinho.pack(fill="both", expand=True, pady=15)

        colunas = (
            "produto",
            "quantidade",
            "valor",
            "subtotal"
        )

        self.tabela = ttk.Treeview(
            area_carrinho,
            columns=colunas,
            show="headings",
            height=10
        )

        self.tabela.heading("produto", text="Produto")
        self.tabela.heading("quantidade", text="Quantidade")
        self.tabela.heading("valor", text="Valor unitário")
        self.tabela.heading("subtotal", text="Subtotal")

        self.tabela.column("produto", width=350)
        self.tabela.column("quantidade", width=100, anchor="center")
        self.tabela.column("valor", width=130, anchor="center")
        self.tabela.column("subtotal", width=130, anchor="center")

        self.tabela.pack(fill="both", expand=True)

        tk.Button(
            area_carrinho,
            text="Remover item selecionado",
            bg="#C0392B",
            fg="white",
            relief="flat",
            padx=10,
            command=self.remover_item
        ).pack(anchor="e", pady=(10, 0))

        rodape = tk.Frame(
            self.parent,
            bg="#F3F5F9"
        )
        rodape.pack(fill="x", pady=10)

        self.label_total = tk.Label(
            rodape,
            text="Total: R$ 0,00",
            font=("Arial", 20, "bold"),
            bg="#F3F5F9",
            fg="#193B65"
        )
        self.label_total.pack(side="left")

        tk.Button(
            rodape,
            text="Limpar venda",
            bg="#7F8C8D",
            fg="white",
            relief="flat",
            padx=15,
            command=self.limpar_venda
        ).pack(side="right")

        tk.Button(
            rodape,
            text="Finalizar venda",
            bg="#27864A",
            fg="white",
            relief="flat",
            padx=15,
            command=self.finalizar_venda
        ).pack(side="right", padx=10)

    def carregar_produtos(self):

        lista = list(
            self.produtos.find({"ativo": True})
        )

        self.lista_produtos = {}

        opcoes = []

        for produto in lista:
            descricao = (
                f"{produto['nome']} "
                f"- R$ {produto['preco_venda']:.2f}"
            )

            opcoes.append(descricao)
            self.lista_produtos[descricao] = produto

        self.combo_produtos["values"] = opcoes

        if opcoes:
            self.combo_produtos.current(0)

    def adicionar_item(self):

        selecionado = self.combo_produtos.get()

        if not selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione um produto."
            )
            return

        try:
            quantidade = int(self.campo_quantidade.get())

            if quantidade <= 0:
                raise ValueError

            produto_dados = self.lista_produtos[selecionado]

            estoque = self.estoques.find_one({
                "produto_id": produto_dados["_id"]
            })

            if not estoque or estoque["quantidade"] < quantidade:
                messagebox.showwarning(
                    "Estoque insuficiente",
                    "Não há quantidade suficiente em estoque."
                )
                return

            produto = type(
                "ProdutoTemporario",
                (),
                {
                    "id": produto_dados["_id"],
                    "nome": produto_dados["nome"],
                    "preco_venda": produto_dados["preco_venda"],
                    "ativo": produto_dados["ativo"]
                }
            )()

            item = ItemVenda(produto, quantidade)

            self.itens_carrinho.append(item)
            self.venda.adicionar_item(item)

            self.atualizar_tabela()

            self.campo_quantidade.delete(0, tk.END)
            self.campo_quantidade.insert(0, "1")

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Informe uma quantidade inteira válida."
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível adicionar o produto:\n{erro}"
            )

    def atualizar_tabela(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for indice, item in enumerate(self.itens_carrinho):
            self.tabela.insert(
                "",
                "end",
                iid=str(indice),
                values=(
                    item.nome_produto,
                    item.quantidade,
                    f"R$ {item.valor_unitario:.2f}",
                    f"R$ {item.subtotal:.2f}"
                )
            )

        self.label_total.config(
            text=f"Total: R$ {self.venda.valor_total:.2f}"
        )

    def remover_item(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione um item para remover."
            )
            return

        indice = int(selecionado[0])

        self.itens_carrinho.pop(indice)
        self.venda = Venda()

        for item in self.itens_carrinho:
            self.venda.adicionar_item(item)

        self.atualizar_tabela()

    def limpar_venda(self):

        if not self.itens_carrinho:
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Deseja limpar todos os itens da venda?"
        )

        if confirmar:
            self.itens_carrinho.clear()
            self.venda = Venda()
            self.atualizar_tabela()

            tk.Button(
            rodape,
            text="Finalizar venda",
            bg="#27864A",
            fg="white",
            relief="flat",
            padx=15,
            command=self.finalizar_venda
        ).pack(side="right", padx=10)    

    
    def finalizar_venda(self):

        if not self.itens_carrinho:
            messagebox.showwarning(
                "Atenção",
                "Adicione pelo menos um produto à venda."
            )
            return

        TelaPagamento(
            self.parent,
            self.venda.valor_total,
            self.confirmar_pagamento
        )

    
    
    
    def confirmar_pagamento(self, pagamento):

        try:
            self.venda.finalizar()

            # Identifica a forma de pagamento
            tipo_pagamento = pagamento.__class__.__name__

            campos_pagamento = {
                "Dinheiro": "total_dinheiro",
                "Cartao": "total_cartao",
                "PIX": "total_pix"
            }

            campo = campos_pagamento.get(tipo_pagamento)

            if not campo:
                raise ValueError(
                    "Forma de pagamento não reconhecida."
                )

            with self.banco.client.start_session() as sessao:

                with sessao.start_transaction():

                    # Localiza o caixa aberto
                    caixa = self.banco["caixas"].find_one(
                        {"status": "ABERTO"},
                        session=sessao
                    )

                    if not caixa:
                        raise ValueError(
                            "Não existe um caixa aberto."
                        )

                    # Vincula a venda ao caixa
                    self.venda.caixa_id = caixa["_id"]

                    # Atualiza o estoque
                    for item in self.itens_carrinho:

                        resultado = self.estoques.update_one(
                            {
                                "produto_id": item.produto_id,
                                "quantidade": {
                                    "$gte": item.quantidade
                                }
                            },
                            {
                                "$inc": {
                                    "quantidade": -item.quantidade
                                }
                            },
                            session=sessao
                        )

                        if resultado.matched_count == 0:
                            raise ValueError(
                                f"Estoque insuficiente para "
                                f"{item.nome_produto}."
                            )

                    # Registra a venda
                    resultado_venda = self.banco["vendas"].insert_one(
                        self.venda.to_document(),
                        session=sessao
                    )

                    # Registra o pagamento
                    documento_pagamento = pagamento.to_document()

                    documento_pagamento["venda_id"] = (
                        resultado_venda.inserted_id
                    )

                    self.banco["pagamentos"].insert_one(
                        documento_pagamento,
                        session=sessao
                    )

                    # Atualiza o faturamento e a forma de pagamento
                    resultado_caixa = self.banco["caixas"].update_one(
                        {
                            "_id": caixa["_id"],
                            "status": "ABERTO"
                        },
                        {
                            "$inc": {
                                "total_vendas": self.venda.valor_total,
                                campo: self.venda.valor_total
                            },
                            "$push": {
                                "vendas": resultado_venda.inserted_id
                            }
                        },
                        session=sessao
                    )

                    if resultado_caixa.matched_count == 0:
                        raise ValueError(
                            "Não foi possível atualizar o caixa."
                        )

            # Confirmação ao operador
            messagebox.showinfo(
                "Venda finalizada",
                "Venda registrada com sucesso!\n\n"
                f"Total: R$ {self.venda.valor_total:.2f}\n"
                f"Pagamento: {tipo_pagamento}"
            )

            self.itens_carrinho.clear()
            self.venda = Venda()
            self.atualizar_tabela()

        except ValueError as erro:

            messagebox.showerror(
                "Não foi possível finalizar",
                str(erro)
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro ao registrar venda",
                f"Não foi possível concluir a operação:\n{erro}"
            )
    def mostrar_usuarios(self):
        if self.usuario_logado.perfil != "ADMIN":
            messagebox.showerror(
                "Acesso negado",
                "Você não tem permissão para acessar este módulo."
            )
            return

        self.limpar_conteudo()

        TelaUsuarios(
            self.conteudo,
            self.banco,
            self.usuario_logado
        )