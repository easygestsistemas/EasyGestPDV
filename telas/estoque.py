
import tkinter as tk
from tkinter import ttk, messagebox

from bson import ObjectId
from models.estoque import Estoque


class TelaEstoque:

    def __init__(self, parent, banco):

        self.parent = parent
        self.banco = banco

        self.produtos = banco["produtos"]
        self.estoques = banco["estoques"]

        self.produto_selecionado = None

        self.criar_interface()
        self.listar_estoque()

    def criar_interface(self):

        tk.Label(
            self.parent,
            text="Controle de Estoque",
            font=("Segoe UI", 22, "bold"),
            fg="#193B65",
            bg="#F3F5F9"
        ).pack(anchor="w", padx=35, pady=(30, 5))

        tk.Label(
            self.parent,
            text="Gerencie entradas, saídas e quantidades disponíveis.",
            font=("Segoe UI", 10),
            fg="#718096",
            bg="#F3F5F9"
        ).pack(anchor="w", padx=35, pady=(0, 20))

        # Formulário
        formulario = tk.Frame(
            self.parent,
            bg="white",
            padx=20,
            pady=15
        )

        formulario.pack(fill="x", padx=35, pady=5)

        tk.Label(
            formulario,
            text="Movimentação de estoque",
            font=("Segoe UI", 13, "bold"),
            fg="#193B65",
            bg="white"
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        tk.Label(
            formulario,
            text="Produto",
            bg="white",
            font=("Segoe UI", 9)
        ).grid(row=1, column=0, sticky="w", pady=6)

        self.combo_produto = ttk.Combobox(
            formulario,
            state="readonly",
            font=("Segoe UI", 10),
            width=35
        )

        self.combo_produto.grid(
            row=1, column=1, sticky="ew", padx=10, pady=6
        )

        tk.Label(
            formulario,
            text="Quantidade",
            bg="white",
            font=("Segoe UI", 9)
        ).grid(row=1, column=2, sticky="w", pady=6)

        self.entrada_quantidade = tk.Entry(
            formulario,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            width=15
        )

        self.entrada_quantidade.grid(
            row=1, column=3, sticky="ew", padx=10, pady=6, ipady=5
        )

        tk.Label(
            formulario,
            text="Estoque mínimo",
            bg="white",
            font=("Segoe UI", 9)
        ).grid(row=2, column=0, sticky="w", pady=6)

        self.entrada_minimo = tk.Entry(
            formulario,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            width=15
        )

        self.entrada_minimo.grid(
            row=2, column=1, sticky="w", padx=10, pady=6, ipady=5
        )

        botoes = tk.Frame(formulario, bg="white")
        botoes.grid(
            row=3, column=0, columnspan=4, sticky="w", pady=(15, 0)
        )

        self.criar_botao(
            botoes, "Registrar entrada",
            self.registrar_entrada, "#26845B"
        )

        self.criar_botao(
            botoes, "Registrar saída",
            self.registrar_saida, "#B45353"
        )

        self.criar_botao(
            botoes, "Atualizar lista",
            self.listar_estoque, "#64748B"
        )

        formulario.grid_columnconfigure(1, weight=1)

        # Tabela
        area_tabela = tk.Frame(
            self.parent,
            bg="white",
            padx=15,
            pady=15
        )

        area_tabela.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

        tk.Label(
            area_tabela,
            text="Produtos em estoque",
            font=("Segoe UI", 13, "bold"),
            fg="#193B65",
            bg="white"
        ).pack(anchor="w", pady=(0, 12))

        colunas = (
            "produto",
            "codigo",
            "quantidade",
            "minimo",
            "situacao"
        )

        self.tabela = ttk.Treeview(
            area_tabela,
            columns=colunas,
            show="headings"
        )

        self.tabela.heading("produto", text="Produto")
        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("quantidade", text="Quantidade")
        self.tabela.heading("minimo", text="Estoque mínimo")
        self.tabela.heading("situacao", text="Situação")

        self.tabela.column("produto", width=220)
        self.tabela.column("codigo", width=150)
        self.tabela.column("quantidade", width=110)
        self.tabela.column("minimo", width=120)
        self.tabela.column("situacao", width=120)

        self.tabela.tag_configure(
            "baixo",
            foreground="#B45353"
        )

        self.tabela.tag_configure(
            "normal",
            foreground="#26845B"
        )

        self.tabela.pack(fill="both", expand=True)

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_produto
        )

        # Carrega os produtos no seletor
        self.carregar_produtos()

    def criar_botao(self, pai, texto, comando, cor):

        tk.Button(
            pai,
            text=texto,
            command=comando,
            bg=cor,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side="left", padx=(0, 8))

    def carregar_produtos(self):

        documentos = list(
            self.produtos.find({"ativo": True}).sort("nome", 1)
        )

        self.lista_produtos = {}

        opcoes = []

        for produto in documentos:

            nome = produto["nome"]

            self.lista_produtos[nome] = produto["_id"]
            opcoes.append(nome)

            # Cria o registro de estoque se ainda não existir
            self.estoques.update_one(
                {"produto_id": produto["_id"]},
                {
                    "$setOnInsert": {
                        "quantidade": 0,
                        "quantidade_minima": 0
                    }
                },
                upsert=True
            )

        self.combo_produto["values"] = opcoes

    def listar_estoque(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        self.carregar_produtos()

        for produto in self.produtos.find().sort("nome", 1):

            estoque = self.estoques.find_one({
                "produto_id": produto["_id"]
            })

            if estoque is None:
                quantidade = 0
                minimo = 0
            else:
                quantidade = estoque.get("quantidade", 0)
                minimo = estoque.get("quantidade_minima", 0)

            baixo = quantidade <= minimo

            situacao = "Estoque baixo" if baixo else "Normal"

            self.tabela.insert(
                "",
                "end",
                iid=str(produto["_id"]),
                values=(
                    produto.get("nome", ""),
                    produto.get("codigo_barras", ""),
                    quantidade,
                    minimo,
                    situacao
                ),
                tags=("baixo" if baixo else "normal",)
            )

    def selecionar_produto(self, evento):

        selecionados = self.tabela.selection()

        if not selecionados:
            return

        self.produto_selecionado = selecionados[0]

        produto = self.produtos.find_one({
            "_id": ObjectId(self.produto_selecionado)
        })

        if produto:
            self.combo_produto.set(produto["nome"])

            estoque = self.estoques.find_one({
                "produto_id": produto["_id"]
            })

            self.entrada_minimo.delete(0, tk.END)

            if estoque:
                self.entrada_minimo.insert(
                    0,
                    str(estoque.get("quantidade_minima", 0))
                )

    def obter_dados(self):

        nome = self.combo_produto.get()

        if not nome or nome not in self.lista_produtos:
            raise ValueError("Selecione um produto.")

        try:
            quantidade = int(self.entrada_quantidade.get())
            minimo = int(self.entrada_minimo.get() or "0")
        except ValueError:
            raise ValueError("Informe quantidades inteiras válidas.")

        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        if minimo < 0:
            raise ValueError("O estoque mínimo não pode ser negativo.")

        produto_id = self.lista_produtos[nome]

        estoque = Estoque(
            produto_id=produto_id,
            quantidade=0,
            quantidade_minima=minimo
        )

        return produto_id, quantidade, estoque

    def registrar_entrada(self):

        try:
            produto_id, quantidade, estoque = self.obter_dados()

            self.estoques.update_one(
                {"produto_id": produto_id},
                {
                    "$inc": {"quantidade": quantidade},
                    "$set": {
                        "quantidade_minima": estoque.quantidade_minima
                    },
                    "$setOnInsert": {
                        "produto_id": produto_id
                    }
                },
                upsert=True
            )

            messagebox.showinfo(
                "EasyGest PDV",
                "Entrada registrada com sucesso!"
            )

            self.limpar_formulario()
            self.listar_estoque()

        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def registrar_saida(self):

        try:
            produto_id, quantidade, estoque = self.obter_dados()

            resultado = self.estoques.update_one(
                {
                    "produto_id": produto_id,
                    "quantidade": {"$gte": quantidade}
                },
                {
                    "$inc": {"quantidade": -quantidade},
                    "$set": {
                        "quantidade_minima": estoque.quantidade_minima
                    }
                }
            )

            if resultado.matched_count == 0:
                messagebox.showwarning(
                    "Estoque insuficiente",
                    "Não existe quantidade suficiente para essa saída."
                )
                return

            messagebox.showinfo(
                "EasyGest PDV",
                "Saída registrada com sucesso!"
            )

            self.limpar_formulario()
            self.listar_estoque()

        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def limpar_formulario(self):

        self.produto_selecionado = None
        self.combo_produto.set("")
        self.entrada_quantidade.delete(0, tk.END)
        self.entrada_minimo.delete(0, tk.END)

        for item in self.tabela.selection():
            self.tabela.selection_remove(item)
