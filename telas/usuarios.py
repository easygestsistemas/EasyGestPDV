
import tkinter as tk
from tkinter import ttk, messagebox

from services.usuario_service import UsuarioService


class TelaUsuarios:
    def __init__(
        self,
        pai,
        banco,
        usuario_logado,
        ao_alterar_perfil=None
    ):
        self.pai = pai
        self.banco = banco
        self.usuario_logado = usuario_logado
        self.ao_alterar_perfil = ao_alterar_perfil
        self.servico = UsuarioService(banco)
        self.usuarios = {}

        self.cor_primaria = "#193B65"
        self.cor_fundo = "#F3F5F9"

        self.criar_interface()
        self.carregar_usuarios()

    def criar_interface(self):
        tk.Label(
            self.pai,
            text="Gerenciamento de Usuários",
            font=("Segoe UI", 22, "bold"),
            fg=self.cor_primaria,
            bg=self.cor_fundo
        ).pack(anchor="w", padx=35, pady=(30, 5))

        tk.Label(
            self.pai,
            text="Cadastre e gerencie os acessos ao EasyGest PDV.",
            font=("Segoe UI", 10),
            fg="#718096",
            bg=self.cor_fundo
        ).pack(anchor="w", padx=35, pady=(0, 20))

        area_botoes = tk.Frame(self.pai, bg=self.cor_fundo)
        area_botoes.pack(fill="x", padx=35, pady=(0, 15))

        tk.Button(
            area_botoes,
            text="+ Novo usuário",
            command=self.abrir_cadastro,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg=self.cor_primaria,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side="left")

        tk.Button(
            area_botoes,
            text="Ativar / Desativar",
            command=self.alternar_status,
            font=("Segoe UI", 10),
            fg=self.cor_primaria,
            bg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side="left", padx=10)

        tk.Button(
            area_botoes,
            text="Promover / Rebaixar",
            command=self.alterar_perfil,
            font=("Segoe UI", 10),
            fg=self.cor_primaria,
            bg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side="left")

        painel = tk.Frame(
            self.pai,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        painel.pack(fill="both", expand=True, padx=35, pady=(0, 25))

        tk.Label(
            painel,
            text="Usuários cadastrados",
            font=("Segoe UI", 14, "bold"),
            fg=self.cor_primaria,
            bg="white"
        ).pack(anchor="w", padx=18, pady=15)

        self.tabela = ttk.Treeview(
            painel,
            columns=("nome", "usuario", "perfil", "status"),
            show="headings"
        )

        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("usuario", text="Usuário")
        self.tabela.heading("perfil", text="Cargo")
        self.tabela.heading("status", text="Status")

        self.tabela.column("nome", width=220)
        self.tabela.column("usuario", width=160)
        self.tabela.column("perfil", width=130)
        self.tabela.column("status", width=120)

        self.tabela.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18)
        )

    def carregar_usuarios(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        self.usuarios = {}

        for usuario in self.servico.listar_usuarios():
            identificador = str(usuario["_id"])
            self.usuarios[identificador] = usuario

            self.tabela.insert(
                "",
                tk.END,
                iid=identificador,
                values=(
                    usuario.get("nome", "-"),
                    usuario.get("usuario", "-"),
                    (
                        "Administrador"
                        if usuario.get("perfil") == "ADMIN"
                        else "Operador"
                    ),
                    "Ativo" if usuario.get("ativo") else "Inativo"
                )
            )

    def abrir_cadastro(self):
        janela = tk.Toplevel(self.pai)
        janela.title("Cadastrar usuário")
        janela.geometry("400x470")
        janela.resizable(False, False)
        janela.configure(bg="white")
        janela.transient(self.pai.winfo_toplevel())
        janela.grab_set()

        tk.Label(
            janela,
            text="Novo usuário",
            font=("Segoe UI", 19, "bold"),
            fg=self.cor_primaria,
            bg="white"
        ).pack(pady=(25, 20))

        campos = {}

        for titulo, chave in [
            ("Nome completo", "nome"),
            ("Nome de usuário", "usuario"),
            ("Senha", "senha")
        ]:
            tk.Label(
                janela,
                text=titulo,
                font=("Segoe UI", 10, "bold"),
                bg="white"
            ).pack(anchor="w", padx=35)

            campo = tk.Entry(
                janela,
                font=("Segoe UI", 11),
                show="*" if chave == "senha" else "",
                relief="solid",
                bd=1
            )
            campo.pack(fill="x", padx=35, pady=(5, 15), ipady=6)
            campos[chave] = campo

        tk.Label(
            janela,
            text="Perfil de acesso",
            font=("Segoe UI", 10, "bold"),
            bg="white"
        ).pack(anchor="w", padx=35)

        perfil = ttk.Combobox(
            janela,
            values=["OPERADOR", "ADMIN"],
            state="readonly"
        )
        perfil.set("OPERADOR")
        perfil.pack(fill="x", padx=35, pady=(5, 20))

        def salvar():
            try:
                self.servico.cadastrar_usuario(
                    nome=campos["nome"].get(),
                    usuario=campos["usuario"].get(),
                    senha=campos["senha"].get(),
                    perfil=perfil.get(),
                    usuario_logado=self.usuario_logado
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Usuário cadastrado com sucesso!",
                    parent=janela
                )

                janela.destroy()
                self.carregar_usuarios()

            except ValueError as erro:
                messagebox.showwarning(
                    "Atenção",
                    str(erro),
                    parent=janela
                )

            except Exception as erro:
                messagebox.showerror(
                    "Erro",
                    f"Não foi possível cadastrar o usuário:\n{erro}",
                    parent=janela
                )

        tk.Button(
            janela,
            text="Cadastrar",
            command=salvar,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg=self.cor_primaria,
            relief="flat",
            cursor="hand2"
        ).pack(fill="x", padx=35, ipady=9)

    def alternar_status(self):
        selecionados = self.tabela.selection()

        if not selecionados:
            messagebox.showwarning(
                "Atenção",
                "Selecione um usuário."
            )
            return

        identificador = selecionados[0]
        usuario = self.usuarios[identificador]

        novo_status = not usuario.get("ativo", True)

        acao = "ativar" if novo_status else "desativar"

        confirmar = messagebox.askyesno(
            "Confirmar operação",
            f"Deseja realmente {acao} o usuário {usuario['usuario']}?"
        )

        if not confirmar:
            return

        try:
            self.servico.alterar_status(
                usuario["_id"],
                novo_status,
                self.usuario_logado
            )

            self.carregar_usuarios()

            messagebox.showinfo(
                "Sucesso",
                f"Usuário {'ativado' if novo_status else 'desativado'} com sucesso."
            )

        except (ValueError, PermissionError) as erro:
            messagebox.showwarning(
                "Operação não permitida",
                str(erro)
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível alterar o usuário:\n{erro}"
            )

    def alterar_perfil(self):
        selecionados = self.tabela.selection()

        if not selecionados:
            messagebox.showwarning(
                "Atenção",
                "Selecione um usuário."
            )
            return

        usuario = self.usuarios[selecionados[0]]
        perfil_atual = usuario.get("perfil", "OPERADOR")
        novo_perfil = "OPERADOR" if perfil_atual == "ADMIN" else "ADMIN"
        cargo_atual = (
            "administrador"
            if perfil_atual == "ADMIN"
            else "operador"
        )
        novo_cargo = (
            "operador"
            if novo_perfil == "OPERADOR"
            else "administrador"
        )

        confirmar = messagebox.askyesno(
            "Confirmar alteração",
            f"Deseja alterar {usuario.get('usuario', 'este usuário')} "
            f"de {cargo_atual} para {novo_cargo}?"
        )

        if not confirmar:
            return

        try:
            self.servico.alterar_perfil(
                usuario["_id"],
                novo_perfil,
                self.usuario_logado
            )

            eh_usuario_logado = (
                str(usuario["_id"]) == str(self.usuario_logado.id)
            )
            if eh_usuario_logado:
                self.usuario_logado.perfil = novo_perfil

            self.carregar_usuarios()

            if eh_usuario_logado and self.ao_alterar_perfil:
                self.ao_alterar_perfil(novo_perfil)

            messagebox.showinfo(
                "Sucesso",
                f"Cargo alterado para {novo_cargo}."
            )

        except (ValueError, PermissionError) as erro:
            messagebox.showwarning(
                "Operação não permitida",
                str(erro)
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível alterar o cargo:\n{erro}"
            )
