
import tkinter as tk
from tkinter import ttk, messagebox
from uuid import uuid4
from models.dinheiro import Dinheiro
from models.cartao import Cartao
from models.pix import PIX


class TelaPagamento:

    def __init__(self, parent, valor_total, callback):
        self.valor_total = valor_total
        self.callback = callback

        self.janela = tk.Toplevel(parent)
        self.janela.title("Pagamento - EasyGest PDV")
        self.janela.geometry("420x430")
        self.janela.resizable(False, False)
        self.janela.configure(bg="#F3F5F9")
        self.janela.transient(parent)
        self.janela.grab_set()

        self.criar_interface()

    def criar_interface(self):

        tk.Label(
            self.janela,
            text="Finalizar pagamento",
            font=("Arial", 18, "bold"),
            bg="#F3F5F9",
            fg="#193B65"
        ).pack(pady=(20, 10))

        tk.Label(
            self.janela,
            text=f"Total da venda: R$ {self.valor_total:.2f}",
            font=("Arial", 15, "bold"),
            bg="#F3F5F9",
            fg="#193B65"
        ).pack(pady=10)

        area = tk.Frame(self.janela, bg="#F3F5F9")
        area.pack(fill="both", expand=True, padx=30, pady=10)

        tk.Label(
            area,
            text="Forma de pagamento:",
            bg="#F3F5F9"
        ).pack(anchor="w")

        self.combo_pagamento = ttk.Combobox(
            area,
            values=["Dinheiro", "Cartão", "PIX"],
            state="readonly"
        )
        self.combo_pagamento.pack(fill="x", pady=5)
        self.combo_pagamento.current(0)
        self.combo_pagamento.bind(
            "<<ComboboxSelected>>",
            self.alterar_campos
        )

        self.area_campos = tk.Frame(
            area,
            bg="#F3F5F9"
        )
        self.area_campos.pack(fill="x", pady=15)

        self.alterar_campos()

        tk.Button(
            self.janela,
            text="Processar pagamento",
            bg="#193B65",
            fg="white",
            relief="flat",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            command=self.processar_pagamento
        ).pack(pady=15)

    def alterar_campos(self, evento=None):

        for widget in self.area_campos.winfo_children():
            widget.destroy()

        forma = self.combo_pagamento.get()

        if forma == "Dinheiro":

            tk.Label(
                self.area_campos,
                text="Valor recebido (R$):",
                bg="#F3F5F9"
            ).pack(anchor="w")

            self.campo_valor = ttk.Entry(self.area_campos)
            self.campo_valor.pack(fill="x", pady=5)

        elif forma == "Cartão":

            tk.Label(
                self.area_campos,
                text="Quantidade de parcelas:",
                bg="#F3F5F9"
            ).pack(anchor="w")

            self.combo_parcelas = ttk.Combobox(
                self.area_campos,
                values=[str(i) for i in range(1, 13)],
                state="readonly"
            )
            self.combo_parcelas.pack(fill="x", pady=5)
            self.combo_parcelas.current(0)

        elif forma == "PIX":

            tk.Label(
                self.area_campos,
                text="Pagamento via PIX",
                font=("Arial", 11, "bold"),
                bg="#F3F5F9",
                fg="#193B65"
            ).pack(anchor="w")

            tk.Label(
                self.area_campos,
                text="A confirmação será simulada nesta etapa.",
                bg="#F3F5F9"
            ).pack(anchor="w", pady=5)

    
    def processar_pagamento(self):

        forma = self.combo_pagamento.get()

        try:

            if forma == "Dinheiro":

                valor_digitado = self.campo_valor.get().strip()

                if not valor_digitado:
                    messagebox.showwarning(
                        "Campo obrigatório",
                        "Informe o valor recebido pelo cliente.",
                        parent=self.janela
                    )
                    self.campo_valor.focus_set()
                    return

                valor_recebido = float(
                    valor_digitado.replace(",", ".")
                )

                pagamento = Dinheiro(
                    self.valor_total,
                    valor_recebido
                )

            elif forma == "Cartão":

                parcelas = int(self.combo_parcelas.get())

                pagamento = Cartao(
                    self.valor_total,
                    parcelas
                )

            else:

                identificador = str(uuid4())

                pagamento = PIX(
                    self.valor_total,
                    identificador
                )

            pagamento.processar()

            self.callback(pagamento)
            self.janela.destroy()

        except ValueError as erro:

            messagebox.showerror(
                "Pagamento inválido",
                str(erro),
                parent=self.janela
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro no pagamento",
                f"Não foi possível processar o pagamento:\n{erro}",
                parent=self.janela
            )
