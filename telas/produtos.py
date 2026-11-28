
import tkinter as tk
from tkinter import ttk, messagebox

from models.produto import Produto
from bson import ObjectId


class TelaProdutos:

    def __init__(self, parent, banco):

        self.parent = parent
        self.banco = banco
        self.colecao = banco["produtos"]
        self.produto_selecionado = None
        self.produto_ativo = True

        self.criar_interface()
        self.listar_produtos()

    def criar_interface(self):

        # Título
        tk.Label(
            self.parent,
            text="Produtos",
            font=("Segoe UI", 22, "bold"),
            fg="#193B65",
            bg="#F3F5F9"
        ).pack(anchor="w", padx=35, pady=(30, 5))

        tk.Label(
            self.parent,
            text="Cadastre e gerencie os produtos do sistema.",
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
            text="Cadastro de produto",
            font=("Segoe UI", 13, "bold"),
            fg="#193B65",
            bg="white"
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        self.campos = {}

        campos = [
            ("Nome", "nome"),
            ("Descrição", "descricao"),
            ("Código de barras", "codigo_barras"),
            ("Preço de venda", "preco_venda"),
            ("Custo", "custo")
        ]

        for indice, (rotulo, chave) in enumerate(campos):

            linha = indice // 2
            coluna = (indice % 2) * 2

            tk.Label(
                formulario,
                text=rotulo,
                font=("Segoe UI", 9),
                bg="white",
                fg="#263445"
            ).grid(
                row=linha + 1,
                column=coluna,
                sticky="w",
                padx=(0, 8),
                pady=6
            )

            entrada = tk.Entry(
                formulario,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1
            )

            entrada.grid(
                row=linha + 1,
                column=coluna + 1,
                sticky="ew",
                padx=(0, 15),
                pady=6,
                ipady=5
            )

            self.campos[chave] = entrada

        formulario.grid_columnconfigure(1, weight=1)
        formulario.grid_columnconfigure(3, weight=1)

        # Botões
        botoes = tk.Frame(formulario, bg="white")
        botoes.grid(
            row=4,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(15, 0)
        )

        self.criar_botao(
            botoes, "Salvar produto",
            self.salvar_produto, "#193B65"
        )

        self.criar_botao(
            botoes, "Novo",
            self.limpar_formulario, "#64748B"
        )

        self.botao_status = tk.Button(
            botoes,
            text="Desativar",
            command=self.alternar_status_produto,
            bg="#B45353",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.botao_status.pack(side="left", padx=(0, 8))

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
            text="Produtos cadastrados",
            font=("Segoe UI", 13, "bold"),
            fg="#193B65",
            bg="white"
        ).pack(anchor="w", pady=(0, 12))

        colunas = (
            "nome",
            "codigo",
            "preco",
            "separador",
            "custo",
            "status"
        )

        estilo = ttk.Style(self.parent)
        estilo.configure(
            "Produtos.Treeview",
            background="white",
            foreground="#263445",
            rowheight=34,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )
        estilo.map(
            "Produtos.Treeview",
            background=[("selected", "#DCE9F7")],
            foreground=[("selected", "#193B65")]
        )
        estilo.configure(
            "Produtos.Treeview.Heading",
            background="#E9EEF5",
            foreground="#193B65",
            font=("Segoe UI", 9, "bold"),
            padding=(10, 9),
            relief="solid"
        )
        estilo.map(
            "Produtos.Treeview.Heading",
            background=[("active", "#DDE6F0")]
        )

        self.tabela = ttk.Treeview(
            area_tabela,
            columns=colunas,
            show="headings",
            style="Produtos.Treeview"
        )

        self.tabela.heading("nome", text="Produto")
        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("preco", text="Preço de venda (R$)", anchor="e")
        self.tabela.heading("separador", text="")
        self.tabela.heading("custo", text="Custo (R$)", anchor="e")
        self.tabela.heading("status", text="Status")

        self.tabela.column("nome", width=220)
        self.tabela.column("codigo", width=150)
        self.tabela.column("preco", width=160, anchor="e")
        self.tabela.column(
            "separador",
            width=14,
            minwidth=14,
            stretch=False
        )
        self.tabela.column("custo", width=140, anchor="e")
        self.tabela.column("status", width=100)

        self.tabela.pack(fill="both", expand=True)

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_produto
        )

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

    def listar_produtos(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for produto in self.colecao.find().sort("nome", 1):

            status = (
                "Ativo" if produto.get("ativo", True)
                else "Inativo"
            )

            self.tabela.insert(
                "",
                "end",
                iid=str(produto["_id"]),
                values=(
                    produto.get("nome", ""),
                    produto.get("codigo_barras", ""),
                    self.formatar_moeda(produto.get("preco_venda", 0)),
                    "",
                    self.formatar_moeda(produto.get("custo", 0)),
                    status
                )
            )

    @staticmethod
    def formatar_moeda(valor):
        texto = f"{float(valor or 0):,.2f}"
        texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {texto}"

    def selecionar_produto(self, evento):

        selecionados = self.tabela.selection()

        if not selecionados:
            return

        self.produto_selecionado = selecionados[0]

        produto = self.colecao.find_one({
            "_id": ObjectId(self.produto_selecionado)
        })

        if produto is None:
            return

        self.produto_ativo = produto.get("ativo", True)
        self.botao_status.configure(
            text="Desativar" if self.produto_ativo else "Reativar",
            bg="#B45353" if self.produto_ativo else "#2F855A"
        )

        self.limpar_campos()

        self.campos["nome"].insert(0, produto.get("nome", ""))
        self.campos["descricao"].insert(0, produto.get("descricao", ""))
        self.campos["codigo_barras"].insert(
            0, produto.get("codigo_barras", "")
        )
        self.campos["preco_venda"].insert(
            0, str(produto.get("preco_venda", 0))
        )
        self.campos["custo"].insert(
            0, str(produto.get("custo", 0))
        )

    def salvar_produto(self):

        try:
            nome = self.campos["nome"].get().strip()
            descricao = self.campos["descricao"].get().strip()
            codigo = self.campos["codigo_barras"].get().strip()

            preco = float(
                self.campos["preco_venda"].get().replace(",", ".")
            )

            custo_texto = self.campos["custo"].get().strip()
            custo = float(custo_texto.replace(",", ".")) if custo_texto else 0

            if not nome or not codigo:
                messagebox.showwarning(
                    "Atenção",
                    "Preencha o nome e o código de barras."
                )
                return

            if preco <= 0 or custo < 0:
                raise ValueError("Informe valores válidos para preço e custo.")

            produto = Produto(
                nome=nome,
                descricao=descricao,
                codigo_barras=codigo,
                preco_venda=preco,
                custo=custo,
                ativo=self.produto_ativo
            )

            if self.produto_selecionado:

                self.colecao.update_one(
                    {"_id": ObjectId(self.produto_selecionado)},
                    {"$set": produto.to_document()}
                )

                mensagem = "Produto atualizado com sucesso!"

            else:

                self.colecao.insert_one(produto.to_document())

                mensagem = "Produto cadastrado com sucesso!"

            messagebox.showinfo("EasyGest PDV", mensagem)

            self.limpar_formulario()
            self.listar_produtos()

        except ValueError as erro:

            messagebox.showerror("Dados inválidos", str(erro))

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar o produto:\n{erro}"
            )

    def alternar_status_produto(self):

        if not self.produto_selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione um produto na tabela."
            )
            return

        novo_status = not self.produto_ativo
        acao = "reativar" if novo_status else "desativar"

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"Deseja realmente {acao} este produto?"
        )

        if not confirmar:
            return

        try:
            resultado = self.colecao.update_one(
                {"_id": ObjectId(self.produto_selecionado)},
                {"$set": {"ativo": novo_status}}
            )

            if resultado.matched_count == 0:
                raise ValueError("O produto selecionado não foi encontrado.")

            self.produto_ativo = novo_status
            self.limpar_formulario()
            self.listar_produtos()

            messagebox.showinfo(
                "EasyGest PDV",
                f"Produto {'reativado' if novo_status else 'desativado'} com sucesso!"
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível {acao} o produto:\n{erro}"
            )

    def limpar_campos(self):

        for entrada in self.campos.values():
            entrada.delete(0, tk.END)

    def limpar_formulario(self):

        self.produto_selecionado = None
        self.produto_ativo = True
        self.botao_status.configure(
            text="Desativar",
            bg="#B45353"
        )
        self.limpar_campos()

        for item in self.tabela.selection():
            self.tabela.selection_remove(item)
