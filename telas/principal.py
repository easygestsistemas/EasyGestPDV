from telas.caixa import TelaCaixa

import tkinter as tk

from tkinter import ttk

from telas.produtos import TelaProdutos

from telas.estoque import TelaEstoque

from telas.pdv import TelaPDV

from tkinter import messagebox

from telas.vendas import TelaVendas

from datetime import datetime, timedelta

from telas.usuarios import TelaUsuarios
from services.usuario_service import UsuarioService

class EasyGestPDV:

    def __init__(self, root, banco, usuario_logado):

        self.root = root

        self.banco = banco

        self.usuario_logado = usuario_logado

        self.periodo_dashboard = "Todo o período"
        self.nav_buttons = {}
        self.pagina_ativa = "Dashboard"

        self.root.title("EasyGest PDV")

        self.root.geometry("1100x700")

        self.root.minsize(900, 600)

        self.root.configure(bg="#F3F5F9")

        self.cor_primaria = "#193B65"

        self.cor_fundo = "#F3F5F9"

        self.cor_texto = "#263445"

        self.configurar_estilos()

        self.criar_layout()

        self.mostrar_dashboard()

    def configurar_estilos(self):

        estilo = ttk.Style()

        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background="white",
            foreground=self.cor_texto,
            rowheight=34,
            fieldbackground="white",
            font=("Segoe UI", 10),
            borderwidth=0
        )
        estilo.map(
            "Treeview",
            background=[("selected", "#DCE9F7")],
            foreground=[("selected", self.cor_primaria)]
        )
        estilo.configure(
            "Treeview.Heading",
            background="#E9EEF5",
            foreground=self.cor_primaria,
            font=("Segoe UI", 10, "bold"),
            padding=(10, 9),
            relief="flat"
        )
        estilo.map(
            "Treeview.Heading",
            background=[("active", "#DDE6F0")]
        )
        estilo.configure(
            "TCombobox",
            fieldbackground="white",
            background="white",
            foreground=self.cor_texto,
            arrowcolor=self.cor_primaria,
            padding=6
        )

    def criar_layout(self):

        # Menu lateral

        self.menu = tk.Frame(

            self.root,

            bg=self.cor_primaria,

            width=220

        )

        self.menu.pack(side="left", fill="y")

        self.menu.pack_propagate(False)

        # Identificação

        self.rotulo_perfil = tk.Label(

            self.menu,

            text="EasyGest",

            font=("Segoe UI", 23, "bold"),

            fg="white",

            bg=self.cor_primaria

        ).pack(pady=(30, 0))

        tk.Label(

            self.menu,

            text="PONTO DE VENDA",

            font=("Segoe UI", 9),

            fg="#B9CDE4",

            bg=self.cor_primaria

        ).pack(pady=(0, 35))

        tk.Label(

            self.menu,

            text=f"Olá, {self.usuario_logado.nome}",

            font=("Segoe UI", 10, "bold"),

            fg="white",

            bg=self.cor_primaria

        ).pack(pady=(0, 5))

        self.rotulo_perfil = tk.Label(

            self.menu,

            text=self.usuario_logado.perfil,

            font=("Segoe UI", 8),

            fg="#B9CDE4",

            bg=self.cor_primaria

        )
        self.rotulo_perfil.pack(pady=(0, 25))

        # Opções do menu

        opcoes = [

            ("Dashboard", self.mostrar_dashboard),

            ("Frente de Caixa", self.mostrar_pdv),

            ("Produtos", self.mostrar_produtos),

            ("Estoque", self.mostrar_estoque),

            ("Vendas", self.mostrar_vendas),

            ("Caixa", self.mostrar_caixa)

        ]

        if self.usuario_logado.perfil == "ADMIN":

            opcoes.append(("Usuários", self.mostrar_usuarios))

        for nome, comando in opcoes:
            botao = tk.Button(
                self.menu,
                text=f"  {nome}",
                command=lambda n=nome, c=comando: self.navegar(n, c),
                font=("Segoe UI", 10, "bold"),
                fg="white",
                bg=self.cor_primaria,
                activebackground="#2D5685",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=18,
                pady=12,
                cursor="hand2",
                bd=0,
                highlightthickness=0
            )
            botao.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[nome] = botao
            botao.bind(
                "<Enter>",
                lambda evento, n=nome: self._hover_menu(n, True)
            )
            botao.bind(
                "<Leave>",
                lambda evento, n=nome: self._hover_menu(n, False)
            )

        # Rodapé do menu

        tk.Label(

            self.menu,

            text="EasyGest PDV | 2026",

            font=("Segoe UI", 8),

            fg="#B9CDE4",

            bg=self.cor_primaria

        ).pack(side="bottom", pady=20)

        # Área de conteúdo

        self.conteudo = tk.Frame(

            self.root,

            bg=self.cor_fundo

        )

        self.conteudo.pack(

            side="right",

            fill="both",

            expand=True

        )

    def navegar(self, nome, comando):
        self.marcar_menu_ativo(nome)
        comando()

    def marcar_menu_ativo(self, nome):
        self.pagina_ativa = nome
        for item, botao in self.nav_buttons.items():
            ativo = item == nome
            botao.configure(
                bg="#2D5685" if ativo else self.cor_primaria,
                fg="white",
                font=("Segoe UI", 10, "bold" if ativo else "normal")
            )

    def _hover_menu(self, nome, entrou):
        if nome == self.pagina_ativa:
            return
        botao = self.nav_buttons.get(nome)
        if botao:
            botao.configure(
                bg="#254B77" if entrou else self.cor_primaria
            )

    @staticmethod
    def formatar_moeda(valor):
        try:
            valor = float(valor or 0)
        except (TypeError, ValueError):
            valor = 0.0
        texto = f"{valor:,.2f}"
        texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {texto}"

    def limpar_conteudo(self):

        for widget in self.conteudo.winfo_children():

            widget.destroy()

    def criar_cabecalho(self, titulo, descricao):

        tk.Label(

            self.conteudo,

            text=titulo,

            font=("Segoe UI", 22, "bold"),

            fg=self.cor_primaria,

            bg=self.cor_fundo

        ).pack(anchor="w", padx=35, pady=(30, 5))

        tk.Label(

            self.conteudo,

            text=descricao,

            font=("Segoe UI", 10),

            fg="#718096",

            bg=self.cor_fundo

        ).pack(anchor="w", padx=35, pady=(0, 25))

    def criar_card(self, pai, titulo, valor, coluna, linha=0):
        cores_destaque = {
            "Faturamento acumulado": "#2F80ED",
            "Vendas realizadas": "#16A085",
            "Produtos cadastrados": "#6C63FF",
            "Estoque baixo": "#E67E22",
            "Situação do caixa": "#16A085" if valor == "Aberto" else "#64748B",
            "Saldo físico": "#193B65"
        }
        cor_destaque = cores_destaque.get(titulo, self.cor_primaria)

        card = tk.Frame(
            pai,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1,
            bd=0
        )
        card.grid(
            row=linha,
            column=coluna,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        tk.Frame(card, bg=cor_destaque, width=5).pack(
            side="left",
            fill="y"
        )

        area_texto = tk.Frame(card, bg="white")
        area_texto.pack(side="left", fill="both", expand=True)

        tk.Label(
            area_texto,
            text=titulo,
            font=("Segoe UI", 10),
            fg="#718096",
            bg="white"
        ).pack(anchor="w", padx=16, pady=(16, 7))

        tk.Label(
            area_texto,
            text=valor,
            font=("Segoe UI", 20, "bold"),
            fg=self.cor_primaria,
            bg="white"
        ).pack(anchor="w", padx=16, pady=(0, 16))

    def mostrar_dashboard(self):

        self.marcar_menu_ativo("Dashboard")
        self.limpar_conteudo()

        self.criar_cabecalho(

            "Dashboard",

            "Visão geral do EasyGest PDV"

        )

        # Filtro de período

        area_filtro = tk.Frame(

            self.conteudo,

            bg=self.cor_fundo

        )

        area_filtro.pack(

            fill="x",

            padx=35,

            pady=(0, 15)

        )

        tk.Label(

            area_filtro,

            text="Período das vendas:",

            font=("Segoe UI", 10, "bold"),

            fg=self.cor_texto,

            bg=self.cor_fundo

        ).pack(side="left", padx=(0, 10))

        filtro_periodo = ttk.Combobox(

            area_filtro,

            values=[

                "Hoje",

                "Últimos 7 dias",

                "Este mês",

                "Todo o período"

            ],

            state="readonly",

            width=20

        )

        filtro_periodo.set(self.periodo_dashboard)

        filtro_periodo.pack(side="left")

        def alterar_periodo(event):

            self.periodo_dashboard = filtro_periodo.get()

            self.mostrar_dashboard()

        filtro_periodo.bind(

            "<<ComboboxSelected>>",

            alterar_periodo

        )

        # =====================================

        # CONSULTA DOS DADOS NO MONGODB

        # =====================================

        produtos = self.banco["produtos"]

        estoques = self.banco["estoques"]

        vendas = self.banco["vendas"]

        pagamentos = self.banco["pagamentos"]

        caixas = self.banco["caixas"]

        # Produtos ativos

        total_produtos = produtos.count_documents({

            "ativo": True

        })

        # =====================================

        # FILTRO DE PERÍODO DAS VENDAS

        # =====================================

        agora = datetime.now()

        data_inicio = None

        if self.periodo_dashboard == "Hoje":

            data_inicio = agora.replace(

                hour=0,

                minute=0,

                second=0,

                microsecond=0

            )

        elif self.periodo_dashboard == "Últimos 7 dias":

            data_inicio = agora - timedelta(days=7)

        elif self.periodo_dashboard == "Este mês":

            data_inicio = datetime(

                agora.year,

                agora.month,

                1

            )

        # Monta a consulta

        filtro_vendas = {

            "status": "FINALIZADA"

        }

        if data_inicio:

            filtro_vendas["data"] = {

                "$gte": data_inicio

            }

        # Quantidade de vendas no período

        total_vendas = vendas.count_documents(

            filtro_vendas

        )

        # Faturamento no período

        vendas_finalizadas = vendas.find(

            filtro_vendas

        )

        faturamento = sum(

            venda.get("valor_total", 0)

            for venda in vendas_finalizadas

        )

        # Produtos com estoque baixo

        estoque_baixo = estoques.count_documents({

            "$expr": {

                "$lte": [

                    "$quantidade",

                    "$quantidade_minima"

                ]

            }

        })

        # Situação do caixa

        caixa_aberto = caixas.find_one({

            "status": "ABERTO"

        })

        if caixa_aberto:

            status_caixa = "Aberto"

            saldo_fisico = round(

                caixa_aberto.get("saldo_inicial", 0)

                + caixa_aberto.get("total_dinheiro", 0)

                - caixa_aberto.get("total_sangrias", 0),

                2

            )

        else:

            status_caixa = "Fechado"

            saldo_fisico = 0.0

        # =====================================

        # CARDS DO DASHBOARD

        # =====================================

        cards = tk.Frame(

            self.conteudo,

            bg=self.cor_fundo

        )

        cards.pack(fill="x", padx=27)

        for coluna in range(3):

            cards.grid_columnconfigure(

                coluna,

                weight=1

            )

        # Primeira linha

        self.criar_card(

            cards,

            "Faturamento acumulado",

            self.formatar_moeda(faturamento),

            0,

            0

        )

        self.criar_card(

            cards,

            "Vendas realizadas",

            str(total_vendas),

            1,

            0

        )

        self.criar_card(

            cards,

            "Produtos cadastrados",

            str(total_produtos),

            2,

            0

        )

        # Segunda linha

        self.criar_card(

            cards,

            "Estoque baixo",

            str(estoque_baixo),

            0,

            1

        )

        self.criar_card(

            cards,

            "Situação do caixa",

            status_caixa,

            1,

            1

        )

        self.criar_card(

            cards,

            "Saldo físico",

            self.formatar_moeda(saldo_fisico),

            2,

            1

        )

        # =====================================

        # VENDAS RECENTES

        # =====================================

        painel = tk.Frame(

            self.conteudo,

            bg="white",

            highlightbackground="#E2E8F0",

            highlightthickness=1

        )

        painel.pack(

            fill="both",

            expand=True,

            padx=35,

            pady=20

        )

        tk.Label(

            painel,

            text="Vendas recentes",

            font=("Segoe UI", 16, "bold"),

            fg=self.cor_primaria,

            bg="white"

        ).pack(

            anchor="w",

            padx=18,

            pady=15

        )

        # Área exclusiva da tabela: tabela e scrollbar compartilham o mesmo pai.
        area_tabela = tk.Frame(painel, bg="white")
        area_tabela.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 15)
        )

        tabela = ttk.Treeview(
            area_tabela,
            columns=("data", "valor", "pagamento"),
            show="headings",
            height=5
        )

        tabela.heading("data", text="Data")
        tabela.heading("valor", text="Valor total")
        tabela.heading("pagamento", text="Forma de pagamento")

        tabela.column("data", width=200)
        tabela.column("valor", width=180)
        tabela.column("pagamento", width=200)

        scroll_vendas = ttk.Scrollbar(
            area_tabela,
            orient="vertical",
            command=tabela.yview
        )
        tabela.configure(yscrollcommand=scroll_vendas.set)

        tabela.pack(side="left", fill="both", expand=True)
        scroll_vendas.pack(side="right", fill="y")

        vendas_recentes = vendas.find(

            filtro_vendas

        ).sort(

            "data",

            -1

        ).limit(5)

        quantidade_vendas = 0

        self.vendas_dashboard = {}

        for venda in vendas_recentes:

            quantidade_vendas += 1

            self.vendas_dashboard[str(venda["_id"])] = venda

            data = venda.get("data")

            if data:

                data_formatada = data.strftime(

                    "%d/%m/%Y %H:%M"

                )

            else:

                data_formatada = "-"

            pagamento = pagamentos.find_one({

                "venda_id": venda["_id"]

            })

            if pagamento:

                forma_pagamento = pagamento.get(

                    "tipo",

                    "-"

                )

            else:

                forma_pagamento = "-"

            tabela.insert(

                "",

                tk.END,

                iid=str(venda["_id"]),

                values=(

                    data_formatada,

                    self.formatar_moeda(venda.get("valor_total", 0)),

                    forma_pagamento

                )

            )

        tabela.bind(

            "<Double-1>",

            lambda evento: self.abrir_detalhes_venda(tabela)

        )

        if quantidade_vendas == 0:

            tabela.insert(

                "",

                tk.END,

                values=(

                    "Nenhuma venda realizada",

                    "-",

                    "-"

                )

            )

    def mostrar_pagina(self, titulo, descricao):

        self.limpar_conteudo()

        self.criar_cabecalho(titulo, descricao)

        tk.Label(

            self.conteudo,

            text="Módulo em desenvolvimento.",

            font=("Segoe UI", 13),

            fg="#718096",

            bg=self.cor_fundo

        ).pack(pady=80)

    def abrir_detalhes_venda(self, tabela):

        selecionados = tabela.selection()

        if not selecionados:

            return

        identificador = selecionados[0]

        venda = self.vendas_dashboard.get(identificador)

        if not venda:

            messagebox.showwarning(

                "Venda não encontrada",

                "Não foi possível localizar os dados da venda."

            )

            return

        janela = tk.Toplevel(self.root)

        janela.title("Detalhes da Venda")

        janela.geometry("850x650")
        janela.minsize(700, 500)
        janela.configure(bg=self.cor_fundo)

        # Cabeçalho

        tk.Label(

            janela,

            text="Detalhes da Venda",

            font=("Segoe UI", 20, "bold"),

            fg=self.cor_primaria,

            bg=self.cor_fundo

        ).pack(pady=(20, 5))

        data = venda.get("data")

        if data:

            data_formatada = data.strftime(

                "%d/%m/%Y às %H:%M"

            )

        else:

            data_formatada = "-"

        # Informações gerais

        painel = tk.Frame(

            janela,

            bg="white",

            highlightbackground="#E2E8F0",

            highlightthickness=1

        )

        painel.pack(fill="x", padx=20, pady=15)

        tk.Label(

            painel,

            text=f"Data: {data_formatada}",

            font=("Segoe UI", 10),

            bg="white"

        ).pack(anchor="w", padx=15, pady=5)

        tk.Label(

            painel,

            text=f"Status: {venda.get('status', '-')}",

            font=("Segoe UI", 10),

            bg="white"

        ).pack(anchor="w", padx=15, pady=5)

        tk.Label(

            painel,

            text=f"Total da venda: {self.formatar_moeda(venda.get('valor_total', 0))}",

            font=("Segoe UI", 13, "bold"),

            fg=self.cor_primaria,

            bg="white"

        ).pack(anchor="w", padx=15, pady=8)

        # Tabela de produtos

        tk.Label(

            janela,

            text="Produtos vendidos",

            font=("Segoe UI", 14, "bold"),

            fg=self.cor_primaria,

            bg=self.cor_fundo

        ).pack(anchor="w", padx=20, pady=(5, 8))

        tabela_itens = ttk.Treeview(

            janela,

            columns=(

                "produto",

                "quantidade",

                "unitario",

                "subtotal"

            ),

            show="headings",

            height=8

        )

        tabela_itens.heading("produto", text="Produto")

        tabela_itens.heading("quantidade", text="Quantidade")

        tabela_itens.heading("unitario", text="Valor unitário")

        tabela_itens.heading("subtotal", text="Subtotal")

        tabela_itens.column("produto", width=250)

        tabela_itens.column("quantidade", width=100)

        tabela_itens.column("unitario", width=130)

        tabela_itens.column("subtotal", width=130)

        tabela_itens.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=5

        )

        for item in venda.get("itens", []):

            tabela_itens.insert(

                "",

                tk.END,

                values=(

                    item.get("nome_produto", "-"),

                    item.get("quantidade", 0),

                    self.formatar_moeda(item.get("valor_unitario", 0)),

                    self.formatar_moeda(item.get("subtotal", 0))

                )

            )

        # Informações do pagamento

        pagamento = self.banco["pagamentos"].find_one({

            "venda_id": venda["_id"]

        })

        area_pagamento = tk.Frame(

            janela,

            bg="white",

            highlightbackground="#E2E8F0",

            highlightthickness=1

        )

        area_pagamento.pack(

            fill="x",

            padx=20,

            pady=15

        )

        tk.Label(

            area_pagamento,

            text="Informações do pagamento",

            font=("Segoe UI", 12, "bold"),

            fg=self.cor_primaria,

            bg="white"

        ).pack(anchor="w", padx=15, pady=8)

        if pagamento:

            tk.Label(

                area_pagamento,

                text=f"Forma: {pagamento.get('tipo', '-')}",

                bg="white",

                font=("Segoe UI", 10)

            ).pack(anchor="w", padx=15, pady=3)

            tk.Label(

                area_pagamento,

                text=f"Valor: {self.formatar_moeda(pagamento.get('valor', 0))}",

                bg="white",

                font=("Segoe UI", 10)

            ).pack(anchor="w", padx=15, pady=3)

            tk.Label(

                area_pagamento,

                text=f"Status: {pagamento.get('status', '-')}",

                bg="white",

                font=("Segoe UI", 10)

            ).pack(anchor="w", padx=15, pady=3)

            if pagamento.get("tipo") == "Dinheiro":

                tk.Label(
                    area_pagamento,
                    text=f"Valor recebido: {self.formatar_moeda(pagamento.get('valor_recebido', 0))}",
                    bg="white"
                ).pack(anchor="w", padx=15, pady=3)

                tk.Label(

                    area_pagamento,

                    text=f"Troco: {self.formatar_moeda(pagamento.get('troco', 0))}",

                    bg="white"

                ).pack(anchor="w", padx=15, pady=3)

            elif pagamento.get("tipo") == "Cartao":

                tk.Label(

                    area_pagamento,

                    text=(

                        f"Parcelas: "

                        f"{pagamento.get('parcelas', 1)}x"

                    ),

                    bg="white"

                ).pack(anchor="w", padx=15, pady=3)

            elif pagamento.get("tipo") == "PIX":

                tk.Label(

                    area_pagamento,

                    text=(

                        "Transação: "

                        f"{pagamento.get('identificador_transacao', '-')}"

                    ),

                    bg="white"

                ).pack(anchor="w", padx=15, pady=3)

        else:

            tk.Label(

                area_pagamento,

                text="Informações de pagamento não encontradas.",

                bg="white",

                fg="#C0392B"

            ).pack(anchor="w", padx=15, pady=8)

    def mostrar_pdv(self):

        self.marcar_menu_ativo("Frente de Caixa")

        caixa_aberto = self.banco["caixas"].find_one({

            "status": "ABERTO"

        })

        if not caixa_aberto:

            messagebox.showwarning(

                "Caixa fechado",

                "Não existe um caixa aberto.\n\n"

                "Abra o caixa antes de iniciar uma venda."

            )

            # Direciona para o módulo Caixa

            self.mostrar_caixa()

            return

        self.limpar_conteudo()

        TelaPDV(self.conteudo, self.banco)

    def mostrar_produtos(self):

        self.marcar_menu_ativo("Produtos")

        self.limpar_conteudo()

        TelaProdutos(

            self.conteudo,

            self.banco

        )

    def mostrar_estoque(self):

        self.marcar_menu_ativo("Estoque")

        self.limpar_conteudo()

        TelaEstoque(

            self.conteudo,

            self.banco

        )

    def mostrar_vendas(self):

        self.marcar_menu_ativo("Vendas")

        self.limpar_conteudo()

        TelaVendas(

            self.conteudo,

            self.banco

        )

    def mostrar_caixa(self):

        self.marcar_menu_ativo("Caixa")

        self.limpar_conteudo()

        TelaCaixa(self.conteudo, self.banco, self.usuario_logado)

    def mostrar_usuarios(self):

        self.marcar_menu_ativo("Usuários")

        if not UsuarioService(self.banco).eh_administrador_ativo(
            self.usuario_logado
        ):

            messagebox.showerror(

                "Acesso negado",

                "Você não tem permissão para acessar este módulo."

            )

            return

        self.limpar_conteudo()

        TelaUsuarios(

            self.conteudo,

            self.banco,

            self.usuario_logado,
            self.atualizar_perfil_logado
        )

    def atualizar_perfil_logado(self, perfil):
        self.usuario_logado.perfil = perfil
        self.rotulo_perfil.configure(text=perfil)

        if perfil != "ADMIN":
            botao_usuarios = self.nav_buttons.get("Usuários")
            if botao_usuarios:
                botao_usuarios.pack_forget()
            self.mostrar_dashboard()

