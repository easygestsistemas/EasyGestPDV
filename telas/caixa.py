import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, simpledialog

from services.usuario_service import UsuarioService

from models.caixa import Caixa

class TelaCaixa:

    def __init__(self, parent, banco, usuario_logado):

        self.parent = parent

        self.banco = banco

        self.caixas = banco["caixas"]

        self.usuario_logado = usuario_logado

        self.usuario_service = UsuarioService(banco)

        self.caixa_atual = None

        self.criar_interface()

        self.carregar_caixa()

    def criar_interface(self):

        self._configurar_estilos()

        self.canvas_principal = tk.Canvas(
            self.parent,
            bg="#F3F5F9",
            highlightthickness=0
        )
        barra_principal = ttk.Scrollbar(
            self.parent,
            orient="vertical",
            command=self.canvas_principal.yview
        )
        self.canvas_principal.configure(yscrollcommand=barra_principal.set)
        self.canvas_principal.pack(side="left", fill="both", expand=True)
        barra_principal.pack(side="right", fill="y")

        self.area_conteudo = tk.Frame(
            self.canvas_principal,
            bg="#F3F5F9"
        )
        janela_conteudo = self.canvas_principal.create_window(
            (0, 0),
            window=self.area_conteudo,
            anchor="nw"
        )
        self.area_conteudo.bind(
            "<Configure>",
            lambda evento: self.canvas_principal.configure(
                scrollregion=self.canvas_principal.bbox("all")
            )
        )
        self.canvas_principal.bind(
            "<Configure>",
            lambda evento: self.canvas_principal.itemconfigure(
                janela_conteudo,
                width=evento.width
            )
        )

        titulo = tk.Label(

            self.area_conteudo,

            text="Gerenciamento de Caixa",

            font=("Segoe UI", 22, "bold"),

            bg="#F3F5F9",

            fg="#193B65"

        )

        titulo.pack(anchor="w", padx=24, pady=(22, 4))

        tk.Label(
            self.area_conteudo,
            text="Acompanhe o movimento e os valores do caixa atual.",
            font=("Segoe UI", 10),
            bg="#F3F5F9",
            fg="#718096"
        ).pack(anchor="w", padx=24, pady=(0, 18))

        # Área de abertura*

        area_abertura = tk.LabelFrame(

            self.area_conteudo,

            text="Abertura de caixa",

            bg="white",

            padx=15,

            pady=15

        )

        area_abertura.pack(fill="x", padx=24, pady=6)

        tk.Label(

            area_abertura,

            text="Saldo inicial (R$):",

            bg="white",
            font=("Segoe UI", 10, "bold"),
            fg="#263445"

        ).pack(anchor="w")

        self.campo_saldo = ttk.Entry(

            area_abertura,

            width=25,
            style="Caixa.TEntry"

        )

        self.campo_saldo.pack(anchor="w", pady=5)

        self.botao_abrir = tk.Button(

            area_abertura,

            text="Abrir caixa",

            bg="#193B65",

            fg="white",

            relief="flat",

            padx=15,

            command=self.abrir_caixa

        )

        self.botao_abrir.pack(anchor="w", pady=5)

        # Área de consulta*

        area_consulta = tk.LabelFrame(

            self.area_conteudo,

            text="Situação do caixa",

            bg="white",

            padx=15,

            pady=15

        )

        area_consulta.pack(fill="x", padx=24, pady=(12, 24))

        self.label_status = tk.Label(

            area_consulta,

            text="Verificando caixa...",

            font=("Segoe UI", 13, "bold"),
            bg="white",

            fg="#193B65"

        )

        self.label_status.pack(anchor="w", pady=5)

        self.label_abertura = tk.Label(

            area_consulta,

            text="",

            bg="white",
            font=("Segoe UI", 9),
            fg="#718096"

        )

        self.label_abertura.pack(anchor="w", pady=5)

        area_metricas = tk.Frame(area_consulta, bg="white")
        area_metricas.pack(fill="x", pady=(8, 10))
        for coluna in range(3):
            area_metricas.grid_columnconfigure(coluna, weight=1)

        self.label_saldo_inicial = tk.Label(

            area_metricas,

            text="Saldo inicial: R$ 0,00",

            bg="white",
            font=("Segoe UI", 10),
            fg="#263445"

        )

        self.label_saldo_inicial.grid(
            row=0, column=0, sticky="w", padx=8, pady=7
        )

        self.label_total_vendas = tk.Label(

            area_metricas,

            text="Faturamento total: R$ 0,00",

            bg="white",
            font=("Segoe UI", 10),
            fg="#263445"

        )

        self.label_total_vendas.grid(
            row=0, column=1, sticky="w", padx=8, pady=7
        )

        self.label_dinheiro = tk.Label(

            area_metricas,

            text="Total em dinheiro: R$ 0,00",

            bg="white",
            font=("Segoe UI", 10),
            fg="#263445"

        )

        self.label_dinheiro.grid(
            row=0, column=2, sticky="w", padx=8, pady=7
        )

        self.label_cartao = tk.Label(

            area_metricas,

            text="Total em cartão: R$ 0,00",

            bg="white",
            font=("Segoe UI", 10),
            fg="#263445"

        )

        self.label_cartao.grid(
            row=1, column=0, sticky="w", padx=8, pady=7
        )

        self.label_pix = tk.Label(

            area_metricas,

            text="Total em PIX: R$ 0,00",

            bg="white",
            font=("Segoe UI", 10),
            fg="#263445"

        )

        self.label_pix.grid(
            row=1, column=1, sticky="w", padx=8, pady=7
        )

        self.label_saldo_atual = tk.Label(

            area_metricas,

            text="Saldo físico: R$ 0,00",

            font=("Segoe UI", 15, "bold"),

            fg="#193B65",

            bg="white"

        )

        self.label_saldo_atual.grid(
            row=1, column=2, sticky="w", padx=8, pady=7
        )

        self.label_sangrias = tk.Label(

            area_metricas,

            text="Total de sangrias: R$ 0,00",

            bg="white",
            font=("Segoe UI", 10),
            fg="#263445"

        )

        self.label_sangrias.grid(
            row=2, column=0, sticky="w", padx=8, pady=7
        )

        area_acoes = tk.Frame(area_consulta, bg="white")
        area_acoes.pack(fill="x", pady=(6, 0))
        for coluna in range(2):
            area_acoes.grid_columnconfigure(coluna, weight=1)

        tk.Button(

            area_acoes,

            text="Registrar sangria",

            bg="#D68910",

            fg="white",

            relief="flat",

            padx=15,

            command=self.abrir_tela_sangria

        ).grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=4)

        tk.Button(

            area_acoes,

            text="Histórico de sangrias",

            bg="#7F8C8D",

            fg="white",

            relief="flat",

            padx=15,

            command=self.consultar_sangrias

        ).grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=4)

        tk.Button(

            area_acoes,

            text="Histórico de caixas",

            bg="#193B65",

            fg="white",

            relief="flat",

            padx=15,

            command=self.consultar_historico_caixas

        ).grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=4)

        tk.Button(

            area_acoes,

            text="Atualizar informações",

            bg="#7F8C8D",

            fg="white",

            relief="flat",

            padx=15,

            command=self.carregar_caixa

        ).grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=4)

        self.botao_fechar = tk.Button(

            area_acoes,

            text="Fechar caixa",

            bg="#C0392B",

            fg="white",

            relief="flat",

            padx=15,

            command=self.fechar_caixa

        )

        self.botao_fechar.grid(
            row=2, column=0, sticky="ew", padx=(0, 6), pady=(4, 0)
        )

        self._estilizar_botoes(area_abertura)
        self._estilizar_botoes(area_acoes)

    def _configurar_estilos(self):

        estilo = ttk.Style(self.parent)
        estilo.configure(
            "Caixa.TEntry",
            padding=(9, 7),
            fieldbackground="white",
            foreground="#263445"
        )
        estilo.configure(
            "Caixa.Treeview",
            background="white",
            fieldbackground="white",
            foreground="#263445",
            rowheight=30,
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "Caixa.Treeview.Heading",
            background="#E9EEF5",
            foreground="#193B65",
            font=("Segoe UI", 10, "bold"),
            padding=(8, 8)
        )
        estilo.map(
            "Caixa.Treeview",
            background=[("selected", "#D8E6F5")],
            foreground=[("selected", "#193B65")]
        )

    def _estilizar_botoes(self, container):

        for widget in container.winfo_children():
            if isinstance(widget, tk.Button):
                cor_base = widget.cget("bg")
                cores_hover = {
                    "#193B65": "#244F80",
                    "#D68910": "#B8740C",
                    "#7F8C8D": "#697879",
                    "#C0392B": "#A93226",
                    "#27864A": "#1E6B3A"
                }
                cor_hover = cores_hover.get(cor_base, cor_base)
                widget.configure(
                    font=("Segoe UI", 9, "bold"),
                    cursor="hand2",
                    padx=16,
                    pady=8,
                    bd=0,
                    activebackground=cor_hover,
                    activeforeground="white"
                )
                def aplicar_cor(evento, botao=widget, cor=cor_hover):
                    if botao.cget("state") != "disabled":
                        botao.configure(bg=cor)

                def restaurar_cor(evento, botao=widget, cor=cor_base):
                    if botao.cget("state") != "disabled":
                        botao.configure(bg=cor)

                widget.bind("<Enter>", aplicar_cor)
                widget.bind("<Leave>", restaurar_cor)

    def _preparar_janela(self, janela, titulo, geometria, minimo):

        janela.title(titulo)
        janela.geometry(geometria)
        janela.minsize(*minimo)
        janela.configure(bg="#F3F5F9")
        janela.transient(self.parent.winfo_toplevel())

    def _criar_tabela_rolavel(self, parent, colunas, altura=10):

        area = tk.Frame(parent, bg="white")
        area.pack(fill="both", expand=True, padx=15, pady=10)

        tabela = ttk.Treeview(
            area,
            columns=colunas,
            show="headings",
            height=altura,
            style="Caixa.Treeview"
        )
        barra_vertical = ttk.Scrollbar(
            area,
            orient="vertical",
            command=tabela.yview
        )
        barra_horizontal = ttk.Scrollbar(
            area,
            orient="horizontal",
            command=tabela.xview
        )
        tabela.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )
        tabela.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")
        area.grid_rowconfigure(0, weight=1)
        area.grid_columnconfigure(0, weight=1)
        return tabela

    def carregar_caixa(self):

        self.caixa_atual = self.caixas.find_one({

            "status": "ABERTO"

        })

        if self.caixa_atual:

            caixa = self.caixa_atual

            saldo_inicial = caixa.get("saldo_inicial", 0)

            total_vendas = caixa.get("total_vendas", 0)

            total_dinheiro = caixa.get("total_dinheiro", 0)

            total_cartao = caixa.get("total_cartao", 0)

            total_pix = caixa.get("total_pix", 0)

            total_sangrias = caixa.get("total_sangrias", 0)

            saldo_atual = round(

                saldo_inicial + total_dinheiro - total_sangrias,

                2

            )

            self.label_status.config(

                text="Caixa aberto",

                fg="#27864A"

            )

            self.label_abertura.config(

                text=(

                    "Data de abertura: "

                    f"{caixa['data_abertura'].strftime('%d/%m/%Y %H:%M')}"

                )

            )

            self.label_saldo_inicial.config(

                text=f"Saldo inicial: R$ {saldo_inicial:.2f}"

            )

            self.label_total_vendas.config(

                text=f"Faturamento total: R$ {total_vendas:.2f}"

            )

            self.label_dinheiro.config(

                text=f"Total em dinheiro: R$ {total_dinheiro:.2f}"

            )

            self.label_cartao.config(

                text=f"Total em cartão: R$ {total_cartao:.2f}"

            )

            self.label_pix.config(

                text=f"Total em PIX: R$ {total_pix:.2f}"

            )

            self.label_sangrias.config(

                text=f"Total de sangrias: R$ {total_sangrias:.2f}"

            )

            self.label_saldo_atual.config(

                text=f"Saldo físico: R$ {saldo_atual:.2f}"

            )

            self.botao_abrir.config(state="disabled")

            self.campo_saldo.config(state="disabled")

            self.botao_fechar.config(state="normal")

        else:

            self.label_status.config(

                text="Nenhum caixa aberto",

                fg="#C0392B"

            )

            self.label_abertura.config(text="")

            self.label_saldo_inicial.config(

                text="Saldo inicial: R$ 0,00"

            )

            self.label_total_vendas.config(

                text="Faturamento total: R$ 0,00"

            )

            self.label_dinheiro.config(

                text="Total em dinheiro: R$ 0,00"

            )

            self.label_cartao.config(

                text="Total em cartão: R$ 0,00"

            )

            self.label_pix.config(

                text="Total em PIX: R$ 0,00"

            )

            self.label_sangrias.config(

                text="Total de sangrias: R$ 0,00"

            )

            self.label_saldo_atual.config(

                text="Saldo físico: R$ 0,00"

            )

            self.botao_abrir.config(state="normal")

            self.campo_saldo.config(state="normal")

            self.botao_fechar.config(state="disabled")

    def abrir_caixa(self):

        valor_digitado = self.campo_saldo.get().strip()

        # Verifica se o campo está vazio*

        if not valor_digitado:

            messagebox.showwarning(

                "Campo obrigatório",

                "Informe o saldo inicial para abrir o caixa.",

                parent=self.parent

            )

            self.campo_saldo.focus_set()

            return

        try:

            valor = float(

                valor_digitado.replace(",", ".")

            )

            if valor < 0:

                messagebox.showwarning(

                    "Valor inválido",

                    "O saldo inicial não pode ser negativo.",

                    parent=self.parent

                )

                self.campo_saldo.focus_set()

                return

            # Verifica se já existe um caixa aberto*

            caixa_aberto = self.caixas.find_one({

                "status": "ABERTO"

            })

            if caixa_aberto:

                messagebox.showwarning(

                    "Caixa já aberto",

                    "Já existe um caixa aberto no sistema.",

                    parent=self.parent

                )

                self.carregar_caixa()

                return

            caixa = Caixa(valor)

            self.caixas.insert_one(

                caixa.to_document()

            )

            messagebox.showinfo(

                "Caixa aberto",

                "O caixa foi aberto com sucesso!\n\n"

                f"Saldo inicial: R$ {valor:.2f}",

                parent=self.parent

            )

            self.campo_saldo.delete(0, tk.END)

            self.carregar_caixa()

        except ValueError:

            messagebox.showwarning(

                "Valor inválido",

                "Digite um valor numérico válido.\n\n"

                "Exemplo: 100,00",

                parent=self.parent

            )

            self.campo_saldo.focus_set()

        except Exception as erro:

            messagebox.showerror(

                "Erro ao abrir caixa",

                f"Não foi possível abrir o caixa.\n\n{erro}",

                parent=self.parent

            )

    def fechar_caixa(self):

        if not self.caixa_atual:

            messagebox.showwarning(

                "Atenção",

                "Não existe um caixa aberto.",

                parent=self.parent

            )

            return

        confirmar = messagebox.askyesno(

            "Fechar caixa",

            "Deseja realmente fechar o caixa?",

            parent=self.parent

        )

        if not confirmar:

            return

        senha = simpledialog.askstring(
            "Confirmar fechamento",
            f"Digite sua senha, {self.usuario_logado.nome}, para fechar o caixa:",
            show="*",
            parent=self.parent.winfo_toplevel()
        )

        if senha is None:
            return

        usuario_validado = self.usuario_service.autenticar(
            self.usuario_logado.usuario,
            senha
        )

        if usuario_validado is None:
            messagebox.showerror(
                "Senha incorreta",
                "A senha informada está incorreta. O fechamento foi cancelado.",
                parent=self.parent
            )
            return

        try:

            from datetime import datetime

            saldo_inicial = self.caixa_atual.get(

                "saldo_inicial", 0

            )

            total_dinheiro = self.caixa_atual.get(

                "total_dinheiro", 0

            )

            total_vendas = self.caixa_atual.get(

                "total_vendas", 0

            )

            total_sangrias = self.caixa_atual.get(

                "total_sangrias", 0

            )

            saldo_final = round(

                saldo_inicial

                + total_dinheiro

                - total_sangrias,

                2

            )

            resultado = self.caixas.update_one(

                {

                    "_id": self.caixa_atual["_id"],

                    "status": "ABERTO"

                },

                {

                    "$set": {

                        "data_fechamento": datetime.now(),

                        "saldo_final": saldo_final,

                        "status": "FECHADO",

                        "usuario_fechamento_id": str(self.usuario_logado.id),

                        "usuario_fechamento": self.usuario_logado.usuario,

                        "nome_usuario_fechamento": self.usuario_logado.nome

                    }

                }

            )

            if resultado.modified_count == 0:

                raise ValueError(

                    "O caixa não pôde ser fechado. "

                    "Verifique se ainda está aberto."

                )

            messagebox.showinfo(

                "Caixa fechado",

                "Caixa fechado com sucesso!\n\n"

                f"Faturamento total: R$ {total_vendas:.2f}\n"

                f"Total em dinheiro: R$ {total_dinheiro:.2f}\n"

                f"Total de sangrias: R$ {total_sangrias:.2f}\n"

                f"Saldo físico final: R$ {saldo_final:.2f}",

                parent=self.parent

            )

            self.carregar_caixa()

        except Exception as erro:

            messagebox.showerror(

                "Erro",

                f"Não foi possível fechar o caixa:\n{erro}",

                parent=self.parent

            )

    def abrir_tela_sangria(self):

        if not self.caixa_atual:

            messagebox.showwarning(

                "Atenção",

                "Não existe um caixa aberto.",

                parent=self.parent

            )

            return

        janela = tk.Toplevel(self.parent)

        self._preparar_janela(
            janela,
            "Registrar Sangria",
            "480x400",
            (400, 340)
        )

        janela.grab_set()

        janela.configure(bg="#F3F5F9")

        tk.Label(

            janela,

            text="Registrar Sangria",

            font=("Segoe UI", 18, "bold"),

            bg="#F3F5F9",

            fg="#193B65"

        ).pack(padx=24, pady=(20, 16))

        tk.Label(

            janela,

            text="Valor da retirada (R$):",

            bg="#F3F5F9"

        ).pack(anchor="w", padx=25)

        campo_valor = ttk.Entry(
            janela,
            width=35,
            style="Caixa.TEntry"
        )

        campo_valor.pack(fill="x", padx=25, pady=5)

        tk.Label(

            janela,

            text="Justificativa:",

            bg="#F3F5F9"

        ).pack(anchor="w", padx=25, pady=(10, 0))

        campo_justificativa = tk.Text(

            janela,

            width=35,

            height=5,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            wrap="word"

        )

        campo_justificativa.pack(fill="both", expand=True, padx=25, pady=5)

        def confirmar():

            valor_digitado = campo_valor.get().strip()

            justificativa = campo_justificativa.get(

                "1.0",

                tk.END

            ).strip()

            if not valor_digitado:

                messagebox.showwarning(

                    "Campo obrigatório",

                    "Informe o valor da sangria.",

                    parent=janela

                )

                campo_valor.focus_set()

                return

            if not justificativa:

                messagebox.showwarning(

                    "Campo obrigatório",

                    "Informe a justificativa da sangria.",

                    parent=janela

                )

                campo_justificativa.focus_set()

                return

            try:

                valor = float(

                    valor_digitado.replace(",", ".")

                )

                if valor <= 0:

                    raise ValueError(

                        "O valor deve ser maior que zero."

                    )

                saldo_inicial = self.caixa_atual.get(

                    "saldo_inicial", 0

                )

                total_dinheiro = self.caixa_atual.get(

                    "total_dinheiro", 0

                )

                total_sangrias = self.caixa_atual.get(

                    "total_sangrias", 0

                )

                saldo_atual = round(

                    saldo_inicial

                    + total_dinheiro

                    - total_sangrias,

                    2

                )

                if valor > saldo_atual:

                    raise ValueError(

                        "O valor da sangria é maior que "

                        "o saldo físico disponível."

                    )

                senha = simpledialog.askstring(
                    "Confirmar sangria",
                    f"Digite sua senha, {self.usuario_logado.nome}:",
                    show="*",
                    parent=janela
                )

                if senha is None:
                    return

                usuario_validado = self.usuario_service.autenticar(
                    self.usuario_logado.usuario,
                    senha
                )

                if usuario_validado is None:
                    messagebox.showerror(
                        "Senha incorreta",
                        "A senha informada está incorreta. Sangria cancelada.",
                        parent=janela
                    )
                    return

                from datetime import datetime

                registro = {

                    "valor": round(valor, 2),

                    "justificativa": justificativa,

                    "data": datetime.now(),
                    "usuario_id": str(self.usuario_logado.id),
                    "usuario": self.usuario_logado.usuario,
                    "nome_usuario": self.usuario_logado.nome
                }

                resultado = self.caixas.update_one(

                    {

                        "_id": self.caixa_atual["_id"],

                        "status": "ABERTO"

                    },

                    {

                        "$inc": {

                            "total_sangrias": round(valor, 2)

                        },

                        "$push": {

                            "sangrias": registro

                        }

                    }

                )

                if resultado.modified_count == 0:

                    raise ValueError(

                        "Não foi possível registrar a sangria."

                    )

                messagebox.showinfo(

                    "Sangria registrada",

                    "Sangria registrada com sucesso!\n\n"

                    f"Valor: R$ {valor:.2f}\n"

                    f"Justificativa: {justificativa}",

                    parent=janela

                )

                janela.destroy()

                self.carregar_caixa()

            except ValueError as erro:

                messagebox.showwarning(

                    "Sangria inválida",

                    str(erro),

                    parent=janela

                )

            except Exception as erro:

                messagebox.showerror(

                    "Erro",

                    f"Não foi possível registrar a sangria:\n{erro}",

                    parent=janela

                )

        tk.Button(

            janela,

            text="Confirmar sangria",

            bg="#D68910",

            fg="white",

            relief="flat",

            padx=15,

            pady=5,

            command=confirmar

        ).pack(anchor="e", padx=25, pady=15)

        self._estilizar_botoes(janela)

    def consultar_sangrias(self):

        # Primeiro, tenta localizar o caixa aberto*

        caixa_historico = self.caixa_atual

        # Se não houver caixa aberto, busca o último fechado*

        if not caixa_historico:

            caixa_historico = self.caixas.find_one(

                {"status": "FECHADO"},

                sort=[("data_fechamento", -1)]

            )

        if not caixa_historico:

            messagebox.showwarning(

                "Atenção",

                "Não existe caixa com histórico disponível.",

                parent=self.parent

            )

            return

        janela = tk.Toplevel(self.parent)

        self._preparar_janela(
            janela,
            "Histórico de Sangrias",
            "900x500",
            (600, 350)
        )

        tk.Label(

            janela,

            text="Histórico de Sangrias",

            font=("Segoe UI", 18, "bold"),

            bg="#F3F5F9",

            fg="#193B65"

        ).pack(anchor="w", padx=20, pady=(20, 10))

        # Identificação do caixa consultado*

        data_abertura = caixa_historico.get("data_abertura")

        if data_abertura:

            identificacao = (

                "Caixa aberto em: "

                f"{data_abertura.strftime('%d/%m/%Y %H:%M')}"

            )

        else:

            identificacao = "Data de abertura indisponível"

        tk.Label(

            janela,

            text=identificacao,

            bg="#F3F5F9",

            fg="#7F8C8D"

        ).pack(anchor="w", padx=20, pady=(0, 5))

        tabela = self._criar_tabela_rolavel(
            janela,
            ("data", "valor", "justificativa", "responsavel")
        )

        tabela.heading("data", text="Data")

        tabela.heading("valor", text="Valor")

        tabela.heading("justificativa", text="Justificativa")
        tabela.heading("responsavel", text="Responsável")

        tabela.column("data", width=160, anchor="center")

        tabela.column("valor", width=130, anchor="e")

        tabela.column("justificativa", width=400)
        tabela.column("responsavel", width=190)

        sangrias = caixa_historico.get("sangrias", [])

        for sangria in reversed(sangrias):

            data = sangria.get("data")

            if data:

                data_formatada = data.strftime(

                    "%d/%m/%Y %H:%M"

                )

            else:

                data_formatada = "-"

            tabela.insert(

                "",

                tk.END,

                values=(

                    data_formatada,

                    f"R$ {sangria.get('valor', 0):.2f}",

                    sangria.get("justificativa", ""),
                    sangria.get("nome_usuario", "Não identificado")

                )

            )

        if not sangrias:

            tk.Label(

                janela,

                text="Nenhuma sangria registrada neste caixa.",

                bg="#F3F5F9",

                fg="#7F8C8D"

            ).pack(pady=5)

    def consultar_historico_caixas(self):

        janela = tk.Toplevel(self.parent)

        self._preparar_janela(
            janela,
            "Histórico de Caixas",
            "1200x560",
            (800, 400)
        )

        tk.Label(

            janela,

            text="Histórico de Caixas",

            font=("Segoe UI", 20, "bold"),

            bg="#F3F5F9",

            fg="#193B65"

        ).pack(anchor="w", padx=20, pady=(20, 5))

        tk.Label(

            janela,

            text="Consulte as movimentações financeiras dos caixas.",

            bg="#F3F5F9",

            fg="#7F8C8D"

        ).pack(anchor="w", padx=20, pady=(0, 8))

        # Área da tabela*

        area_tabela = tk.Frame(janela, bg="white")

        area_tabela.pack(

            fill="both",

            expand=True,

            padx=15,

            pady=10

        )

        colunas = (

            "abertura",

            "fechamento",

            "status",

            "saldo_inicial",

            "vendas",

            "dinheiro",

            "cartao",

            "pix",

            "sangrias",

            "saldo_final",

            "responsavel_fechamento"

        )

        tabela = ttk.Treeview(

            area_tabela,

            columns=colunas,

            show="headings",
            style="Caixa.Treeview"

        )

        # Cabeçalhos*

        tabela.heading("abertura", text="Abertura")

        tabela.heading("fechamento", text="Fechamento")

        tabela.heading("status", text="Status")

        tabela.heading("saldo_inicial", text="Saldo inicial")

        tabela.heading("vendas", text="Faturamento")

        tabela.heading("dinheiro", text="Dinheiro")

        tabela.heading("cartao", text="Cartão")

        tabela.heading("pix", text="PIX")

        tabela.heading("sangrias", text="Sangrias")

        tabela.heading("saldo_final", text="Saldo final")

        tabela.heading("responsavel_fechamento", text="Responsável pelo fechamento")

        # Largura das colunas*

        tabela.column("abertura", width=140)

        tabela.column("fechamento", width=140)

        tabela.column("status", width=90)

        tabela.column("saldo_inicial", width=110, anchor="e")

        tabela.column("vendas", width=110, anchor="e")

        tabela.column("dinheiro", width=100, anchor="e")

        tabela.column("cartao", width=100, anchor="e")

        tabela.column("pix", width=100, anchor="e")

        tabela.column("sangrias", width=100, anchor="e")

        tabela.column("saldo_final", width=110, anchor="e")

        tabela.column("responsavel_fechamento", width=190)

        # Barras de rolagem*

        barra_vertical = ttk.Scrollbar(

            area_tabela,

            orient="vertical",

            command=tabela.yview

        )

        barra_horizontal = ttk.Scrollbar(

            area_tabela,

            orient="horizontal",

            command=tabela.xview

        )

        tabela.configure(

            yscrollcommand=barra_vertical.set,

            xscrollcommand=barra_horizontal.set

        )

        tabela.grid(row=0, column=0, sticky="nsew")

        barra_vertical.grid(row=0, column=1, sticky="ns")

        barra_horizontal.grid(row=1, column=0, sticky="ew")

        area_tabela.grid_rowconfigure(0, weight=1)

        area_tabela.grid_columnconfigure(0, weight=1)

        # Busca todos os caixas, do mais recente ao mais antigo*

        caixas = self.caixas.find().sort(

            "data_abertura",

            -1

        )

        self.caixas_por_id = {}

        for caixa in caixas:

            abertura = caixa.get("data_abertura")

            fechamento = caixa.get("data_fechamento")

            if abertura:

                abertura = abertura.strftime(

                    "%d/%m/%Y %H:%M"

                )

            else:

                abertura = "-"

            if fechamento:

                fechamento = fechamento.strftime(

                    "%d/%m/%Y %H:%M"

                )

            else:

                fechamento = "-"

            self.caixas_por_id[str(caixa["_id"])] = caixa

            tabela.insert(

                "",

                tk.END,

                iid=str(caixa["_id"]),

                values=(

                    abertura,

                    fechamento,

                    caixa.get("status", "-"),

                    f"R$ {caixa.get('saldo_inicial', 0):.2f}",

                    f"R$ {caixa.get('total_vendas', 0):.2f}",

                    f"R$ {caixa.get('total_dinheiro', 0):.2f}",

                    f"R$ {caixa.get('total_cartao', 0):.2f}",

                    f"R$ {caixa.get('total_pix', 0):.2f}",

                    f"R$ {caixa.get('total_sangrias', 0):.2f}",

                    (

                        f"R$ {caixa.get('saldo_final'):.2f}"

                        if caixa.get("saldo_final") is not None

                        else "Em aberto"

                    ),

                    caixa.get("nome_usuario_fechamento", "Não identificado")

                )

            )

        tabela.bind(

            "<Double-1>",

            lambda evento: self.abrir_detalhes_caixa(tabela)

        )

        if tabela.get_children() == ():

            tk.Label(

                janela,

                text="Nenhum caixa registrado.",

                bg="#F3F5F9",

                fg="#7F8C8D"

            ).pack(pady=10)

    def abrir_detalhes_caixa(self, tabela):

        selecionados = tabela.selection()

        if not selecionados:

            return

        identificador = selecionados[0]

        caixa = self.caixas_por_id.get(identificador)

        if not caixa:

            messagebox.showerror(

                "Erro",

                "Não foi possível localizar os dados do caixa.",

                parent=self.parent

            )

            return

        janela = tk.Toplevel(self.parent)

        self._preparar_janela(
            janela,
            "Detalhes do Caixa",
            "1050x720",
            (800, 500)
        )

        # Cabeçalho*

        tk.Label(

            janela,

            text="Detalhes do Caixa",

            font=("Segoe UI", 20, "bold"),

            bg="#F3F5F9",

            fg="#193B65"

        ).pack(anchor="w", padx=20, pady=(20, 10))

        data_abertura = caixa.get("data_abertura")

        data_fechamento = caixa.get("data_fechamento")

        if data_abertura:

            abertura = data_abertura.strftime(

                "%d/%m/%Y %H:%M"

            )

        else:

            abertura = "-"

        if data_fechamento:

            fechamento = data_fechamento.strftime(

                "%d/%m/%Y %H:%M"

            )

        else:

            fechamento = "Em aberto"

        # Resumo financeiro*

        resumo = tk.LabelFrame(

            janela,

            text="Resumo financeiro",

            bg="white",

            fg="#193B65",

            font=("Segoe UI", 10, "bold"),

            padx=15,

            pady=10

        )

        resumo.pack(fill="x", padx=15, pady=5)

        informacoes = [

            ("Status", caixa.get("status", "-")),

            ("Abertura", abertura),

            ("Fechamento", fechamento),

            ("Responsável pelo fechamento", caixa.get("nome_usuario_fechamento", "Não identificado")),

            (

                "Saldo inicial",

                f"R$ {caixa.get('saldo_inicial', 0):.2f}"

            ),

            (

                "Faturamento",

                f"R$ {caixa.get('total_vendas', 0):.2f}"

            ),

            (

                "Dinheiro",

                f"R$ {caixa.get('total_dinheiro', 0):.2f}"

            ),

            (

                "Cartão",

                f"R$ {caixa.get('total_cartao', 0):.2f}"

            ),

            (

                "PIX",

                f"R$ {caixa.get('total_pix', 0):.2f}"

            ),

            (

                "Sangrias",

                f"R$ {caixa.get('total_sangrias', 0):.2f}"

            )

        ]

        for indice, (nome, valor) in enumerate(informacoes):

            tk.Label(

                resumo,

                text=f"{nome}: {valor}",

                font=("Segoe UI", 10, "bold"),

                bg="white",

                fg="#263445"

            ).grid(

                row=indice // 3,

                column=indice % 3,

                sticky="w",

                padx=10,

                pady=5

            )

        # Área de vendas*

        tk.Label(

            janela,

            text="Vendas realizadas",

            font=("Segoe UI", 14, "bold"),

            bg="#F3F5F9",

            fg="#193B65"

        ).pack(anchor="w", padx=15, pady=(15, 5))

        tabela_vendas = self._criar_tabela_rolavel(
            janela,
            ("data", "total", "status", "pagamento"),
            altura=8
        )

        tabela_vendas.heading("data", text="Data")

        tabela_vendas.heading("total", text="Valor total")

        tabela_vendas.heading("status", text="Status")

        tabela_vendas.heading("pagamento", text="Pagamento")

        tabela_vendas.column("data", width=180)

        tabela_vendas.column("total", width=130, anchor="e")

        tabela_vendas.column("status", width=130)

        tabela_vendas.column("pagamento", width=180)

        # Busca as vendas vinculadas ao caixa*

        vendas = self.banco["vendas"].find({

            "caixa_id": caixa["_id"]

        }).sort("data", -1)

        for venda in vendas:

            pagamento = self.banco["pagamentos"].find_one({

                "venda_id": venda["_id"]

            })

            if pagamento:

                forma_pagamento = pagamento.get(

                    "tipo", "-"

                )

            else:

                forma_pagamento = "-"

            data_venda = venda.get("data")

            if data_venda:

                data_formatada = data_venda.strftime(

                    "%d/%m/%Y %H:%M"

                )

            else:

                data_formatada = "-"

            tabela_vendas.insert(

                "",

                tk.END,

                values=(

                    data_formatada,

                    f"R$ {venda.get('valor_total', 0):.2f}",

                    venda.get("status", "-"),

                    forma_pagamento

                )

            )

        # Área de sangrias*

        tk.Label(

            janela,

            text="Sangrias realizadas",

            font=("Segoe UI", 14, "bold"),

            bg="#F3F5F9",

            fg="#193B65"

        ).pack(anchor="w", padx=15, pady=(15, 5))

        tabela_sangrias = self._criar_tabela_rolavel(
            janela,
            ("data", "valor", "justificativa", "responsavel"),
            altura=5
        )

        tabela_sangrias.heading("data", text="Data")

        tabela_sangrias.heading("valor", text="Valor")

        tabela_sangrias.heading(

            "justificativa",

            text="Justificativa"

        )
        tabela_sangrias.heading("responsavel", text="Responsável")

        tabela_sangrias.column("data", width=180)

        tabela_sangrias.column("valor", width=130, anchor="e")

        tabela_sangrias.column(

            "justificativa",

            width=500

        )
        tabela_sangrias.column("responsavel", width=190)

        sangrias = caixa.get("sangrias", [])

        for sangria in reversed(sangrias):

            data = sangria.get("data")

            if data:

                data_formatada = data.strftime(

                    "%d/%m/%Y %H:%M"

                )

            else:

                data_formatada = "-"

            tabela_sangrias.insert(

                "",

                tk.END,

                values=(

                    data_formatada,

                    f"R$ {sangria.get('valor', 0):.2f}",

                    sangria.get("justificativa", ""),
                    sangria.get("nome_usuario", "Não identificado")

                )

            )
