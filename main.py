
import tkinter as tk
import sys
from pathlib import Path

from conexao import conectar, fechar_conexao
from telas.principal import EasyGestPDV
from telas.login import TelaLogin


def caminho_recurso(caminho):
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent

    return base / caminho


def iniciar_sistema():
    banco = conectar()

    if banco is None:
        print("Não foi possível iniciar o sistema.")
        return

    root = tk.Tk()

    icone = caminho_recurso("assets/easygest.ico")
    root.iconbitmap(str(icone))

    def ao_fechar():
        fechar_conexao()
        root.destroy()

    def abrir_sistema(usuario_logado):
        EasyGestPDV(root, banco, usuario_logado)

    root.protocol("WM_DELETE_WINDOW", ao_fechar)

    TelaLogin(root, banco, abrir_sistema)

    root.mainloop()


if __name__ == "__main__":
    iniciar_sistema()
