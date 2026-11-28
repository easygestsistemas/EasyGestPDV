
import tkinter as tk
from tkinter import messagebox

from services.usuario_service import UsuarioService


class TelaLogin:
    def __init__(self, root, banco, ao_autenticar):
        self.root = root
        self.banco = banco
        self.ao_autenticar = ao_autenticar
        self.servico = UsuarioService(banco)

        self.cor_primaria = "#193B65"
        self.cor_fundo = "#F3F5F9"

        self.criar_interface()

    def criar_interface(self):
        self.root.title("EasyGest PDV - Login")
        self.root.geometry("420x500")
        self.root.minsize(420, 500)
        self.root.configure(bg=self.cor_fundo)

        self.frame = tk.Frame(
            self.root,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        self.frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=340,
            height=390
        )

        tk.Label(
            self.frame,
            text="EasyGest",
            font=("Segoe UI", 28, "bold"),
            fg=self.cor_primaria,
            bg="white"
        ).pack(pady=(30, 0))

        tk.Label(
            self.frame,
            text="PONTO DE VENDA",
            font=("Segoe UI", 9),
            fg="#718096",
            bg="white"
        ).pack(pady=(0, 30))

        tk.Label(
            self.frame,
            text="Usuário",
            font=("Segoe UI", 10, "bold"),
            fg="#263445",
            bg="white"
        ).pack(anchor="w", padx=30)

        self.campo_usuario = tk.Entry(
            self.frame,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )
        self.campo_usuario.pack(fill="x", padx=30, pady=(5, 15), ipady=7)

        tk.Label(
            self.frame,
            text="Senha",
            font=("Segoe UI", 10, "bold"),
            fg="#263445",
            bg="white"
        ).pack(anchor="w", padx=30)

        self.campo_senha = tk.Entry(
            self.frame,
            font=("Segoe UI", 11),
            show="*",
            relief="solid",
            bd=1
        )
        self.campo_senha.pack(fill="x", padx=30, pady=(5, 25), ipady=7)

        tk.Button(
            self.frame,
            text="Entrar",
            command=self.realizar_login,
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg=self.cor_primaria,
            activebackground="#2D5685",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        ).pack(fill="x", padx=30, ipady=9)

        tk.Label(
            self.frame,
            text="EasyGest PDV | 2026",
            font=("Segoe UI", 8),
            fg="#718096",
            bg="white"
        ).pack(side="bottom", pady=15)

        self.campo_usuario.focus_set()

        self.root.bind("<Return>", lambda evento: self.realizar_login())

    def realizar_login(self):
        usuario = self.campo_usuario.get().strip()
        senha = self.campo_senha.get()

        if not usuario or not senha:
            messagebox.showwarning(
                "Atenção",
                "Informe o usuário e a senha."
            )
            return

        try:
            usuario_logado = self.servico.autenticar(usuario, senha)

            if usuario_logado is None:
                messagebox.showerror(
                    "Falha no login",
                    "Usuário ou senha inválidos."
                )
                self.campo_senha.delete(0, tk.END)
                self.campo_senha.focus_set()
                return

            self.root.unbind("<Return>")
            self.frame.destroy()

            self.ao_autenticar(usuario_logado)

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível realizar o login:\n{erro}"
            )
