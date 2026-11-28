
from secrets import token_urlsafe

from models.usuario import Usuario

senha_teste = token_urlsafe(16)

usuario = Usuario(
    nome="Usuário de teste",
    usuario="usuario_teste",
    senha=senha_teste,
    perfil="ADMIN"
)

print(usuario)
print("Senha correta:", usuario.validar_senha(senha_teste))
print("Senha incorreta:", usuario.validar_senha("senhaerrada"))
