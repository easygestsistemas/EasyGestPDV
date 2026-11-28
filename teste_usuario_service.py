
from getpass import getpass

from conexao import conectar, fechar_conexao
from services.usuario_service import UsuarioService


banco = conectar()

if banco is None:
    print("Não foi possível conectar ao MongoDB.")
    exit()

try:
    servico = UsuarioService(banco)

    if not servico.existe_administrador():
        print("\n=== CONFIGURAÇÃO DO PRIMEIRO ADMINISTRADOR ===")

        nome = input("Nome completo: ")
        usuario = input("Nome de usuário: ")
        senha = getpass("Crie uma senha: ")
        confirmar = getpass("Confirme a senha: ")

        if senha != confirmar:
            print("As senhas não coincidem.")
            exit()

        identificador = servico.cadastrar_usuario(
            nome=nome,
            usuario=usuario,
            senha=senha,
            perfil="ADMIN"
        )

        print("\nAdministrador cadastrado com sucesso!")
        print("ID:", identificador)

    else:
        print("\nJá existe um administrador cadastrado.")

    print("\n=== TESTE DE AUTENTICAÇÃO ===")

    usuario_login = input("Usuário: ")
    senha_login = getpass("Senha: ")

    usuario_logado = servico.autenticar(
        usuario_login,
        senha_login
    )

    if usuario_logado:
        print("\nLogin realizado com sucesso!")
        print("Nome:", usuario_logado.nome)
        print("Perfil:", usuario_logado.perfil)
    else:
        print("\nUsuário ou senha inválidos.")

    print("\n=== TESTE DE LISTAGEM ===")

    usuarios = servico.listar_usuarios()

    for usuario in usuarios:
        print(
            usuario["nome"],
            "|",
            usuario["usuario"],
            "|",
            usuario["perfil"]
        )

finally:
    fechar_conexao()
