
import tkinter as tk
from tkinter import ttk, messagebox


class TelaVendas:

    def __init__(self, parent, banco):
        self.parent = parent
        self.vendas = banco["vendas"]
        self.pagamentos = banco["pagamentos"]

        self.criar_interface()
        self.carregar_vendas()

    def criar_interface(self):

        titulo = tk.Label(
            self.parent,
            text="Histórico de Vendas",
            font=("Arial", 20, "bold"),
            bg="#F3F5F9",
            fg="#193B65"
        )
        titulo.pack(anchor="w", pady=(0, 20))

        area = tk.Frame(
            self.parent,
            bg="#F3F5F9"
        )
        area.pack(fill="both", expand=True)

        colunas = (
            "data",
            "valor",
            "pagamento",
            "status"
        )

        self.tabela = ttk.Treeview(
            area,
            columns=colunas,
            show="headings",
            height=15
        )

        self.tabela.heading("data", text="Data")
        self.tabela.heading("valor", text="Valor total")
        self.tabela.heading("pagamento", text="Pagamento")
        self.tabela.heading("status", text="Status")

        self.tabela.column("data", width=180)
        self.tabela.column("valor", width=130, anchor="center")
        self.tabela.column("pagamento", width=150, anchor="center")
        self.tabela.column("status", width=130, anchor="center")

        self.tabela.pack(
            fill="both",
            expand=True,
            pady=5
        )

        botoes = tk.Frame(
            self.parent,
            bg="#F3F5F9"
        )
        botoes.pack(fill="x", pady=10)

        tk.Button(
            botoes,
            text="Atualizar histórico",
            bg="#193B65",
            fg="white",
            relief="flat",
            padx=15,
            command=self.carregar_vendas
        ).pack(side="left")

        tk.Button(
            botoes,
            text="Ver detalhes",
            bg="#27864A",
            fg="white",
            relief="flat",
            padx=15,
            command=self.ver_detalhes
        ).pack(side="left", padx=10)

    def carregar_vendas(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        try:
            lista = self.vendas.find().sort(
                "data", -1
            )

            for venda in lista:

                pagamento = self.pagamentos.find_one({
                    "venda_id": venda["_id"]
                })

                forma_pagamento = (
                    pagamento["tipo"]
                    if pagamento else "Não informado"
                )

                data = venda["data"].strftime(
                    "%d/%m/%Y %H:%M"
                )

                self.tabela.insert(
                    "",
                    "end",
                    iid=str(venda["_id"]),
                    values=(
                        data,
                        f"R$ {venda['valor_total']:.2f}",
                        forma_pagamento,
                        venda["status"]
                    )
                )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível carregar as vendas:\n{erro}",
                parent=self.parent
            )

    def ver_detalhes(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione uma venda para consultar.",
                parent=self.parent
            )
            return

        try:
            from bson import ObjectId

            venda_id = ObjectId(selecionado[0])

            venda = self.vendas.find_one({
                "_id": venda_id
            })

            pagamento = self.pagamentos.find_one({
                "venda_id": venda_id
            })

            detalhes = (
                f"Data: {venda['data'].strftime('%d/%m/%Y %H:%M')}\n"
                f"Status: {venda['status']}\n\n"
                "PRODUTOS:\n"
            )

            for item in venda["itens"]:
                detalhes += (
                    f"\n{item['nome_produto']}\n"
                    f"Quantidade: {item['quantidade']}\n"
                    f"Valor unitário: R$ {item['valor_unitario']:.2f}\n"
                    f"Subtotal: R$ {item['subtotal']:.2f}\n"
                )

            detalhes += (
                f"\nTOTAL: R$ {venda['valor_total']:.2f}\n"
            )

            if pagamento:
                detalhes += (
                    f"\nPagamento: {pagamento['tipo']}\n"
                    f"Valor: R$ {pagamento['valor']:.2f}\n"
                    f"Status: {pagamento['status']}\n"
                )

                if "troco" in pagamento:
                    detalhes += (
                        f"Troco: R$ {pagamento['troco']:.2f}\n"
                    )

                if "parcelas" in pagamento:
                    detalhes += (
                        f"Parcelas: {pagamento['parcelas']}x\n"
                    )

            messagebox.showinfo(
                "Detalhes da venda",
                detalhes,
                parent=self.parent
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível consultar a venda:\n{erro}",
                parent=self.parent
            )
