
from models.usuario import Usuario


class UsuarioService:
    def __init__(self, banco):
        self.banco = banco
        self.usuarios = banco["usuarios"]

    def existe_administrador(self):
        return self.usuarios.count_documents({
            "perfil": "ADMIN",
            "ativo": True
        }) > 0

    def eh_administrador_ativo(self, usuario_logado):
        identificador = getattr(usuario_logado, "id", None)
        if identificador is None:
            return False

        return self.usuarios.find_one({
            "_id": identificador,
            "perfil": "ADMIN",
            "ativo": True
        }) is not None

    def _exigir_administrador_ativo(self, usuario_logado):
        if not self.eh_administrador_ativo(usuario_logado):
            raise PermissionError(
                "Somente um administrador ativo pode gerenciar acessos."
            )

    def existe_usuario(self, usuario):
        usuario = usuario.strip().lower()

        return self.usuarios.find_one({
        "usuario": usuario
        }) is not None

    def cadastrar_usuario(
        self,
        nome,
        usuario,
        senha,
        perfil="OPERADOR",
        usuario_logado=None
    ):
        if not nome.strip():
            raise ValueError("Informe o nome do usuário.")

        if not usuario.strip():
            raise ValueError("Informe um nome de usuário.")

        if len(senha) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")

        if perfil not in ["ADMIN", "OPERADOR"]:
            raise ValueError("Perfil inválido.")

        if usuario_logado is None:
            if perfil != "ADMIN" or self.existe_administrador():
                raise PermissionError(
                    "Somente um administrador ativo pode cadastrar usuários."
                )
        else:
            self._exigir_administrador_ativo(usuario_logado)

        if self.existe_usuario(usuario):
            raise ValueError("Este nome de usuário já está cadastrado.")

        novo_usuario = Usuario(
            nome=nome.strip(),
            usuario=usuario.strip().lower(),
            senha=senha,
            perfil=perfil
        )

        resultado = self.usuarios.insert_one(novo_usuario.to_document())

        return resultado.inserted_id

    def autenticar(self, usuario, senha):
        usuario_encontrado = self.usuarios.find_one({
            "usuario": usuario.strip().lower(),
            "ativo": True
        })

        if not usuario_encontrado:
            return None

        objeto_usuario = Usuario.__new__(Usuario)
        objeto_usuario.id = usuario_encontrado["_id"]
        objeto_usuario.nome = usuario_encontrado["nome"]
        objeto_usuario.usuario = usuario_encontrado["usuario"]
        objeto_usuario.perfil = usuario_encontrado["perfil"]
        objeto_usuario.ativo = usuario_encontrado["ativo"]
        objeto_usuario.senha_hash = usuario_encontrado["senha_hash"]

        if objeto_usuario.validar_senha(senha):
            return objeto_usuario

        return None

    def listar_usuarios(self):
        return list(self.usuarios.find({}, {"senha_hash": 0}))

    def alterar_status(self, id_usuario, ativo, usuario_logado):
        self._exigir_administrador_ativo(usuario_logado)

        usuario = self.usuarios.find_one({"_id": id_usuario})
        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        if not isinstance(ativo, bool):
            raise ValueError("O status deve ser ativo ou inativo.")

        if (
            not ativo
            and str(id_usuario) == str(usuario_logado.id)
        ):
            raise ValueError("Você não pode desativar sua própria conta.")

        if (
            usuario.get("perfil") == "ADMIN"
            and usuario.get("ativo")
            and not ativo
            and self.usuarios.count_documents({
                "perfil": "ADMIN",
                "ativo": True
            }) <= 1
        ):
            raise ValueError(
                "O sistema precisa manter pelo menos um administrador ativo."
            )

        resultado = self.usuarios.update_one(
            {"_id": id_usuario},
            {"$set": {"ativo": ativo}}
        )

        if resultado.matched_count == 0:
            raise ValueError("Usuário não encontrado.")

        return resultado

    def alterar_perfil(self, id_usuario, novo_perfil, usuario_logado):
        self._exigir_administrador_ativo(usuario_logado)

        if novo_perfil not in ["ADMIN", "OPERADOR"]:
            raise ValueError("Perfil inválido.")

        usuario = self.usuarios.find_one({"_id": id_usuario})
        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        if (
            usuario.get("perfil") == "ADMIN"
            and usuario.get("ativo")
            and novo_perfil != "ADMIN"
            and self.usuarios.count_documents({
                "perfil": "ADMIN",
                "ativo": True
            }) <= 1
        ):
            raise ValueError(
                "O sistema precisa manter pelo menos um administrador ativo."
            )

        resultado = self.usuarios.update_one(
            {"_id": id_usuario},
            {"$set": {"perfil": novo_perfil}}
        )

        if resultado.matched_count == 0:
            raise ValueError("Usuário não encontrado.")

        return resultado

    def alterar_senha(self, id_usuario, nova_senha):
        usuario_encontrado = self.usuarios.find_one({"_id": id_usuario})

        if not usuario_encontrado:
            raise ValueError("Usuário não encontrado.")

        objeto_usuario = Usuario.__new__(Usuario)
        objeto_usuario.senha_hash = usuario_encontrado["senha_hash"]

        objeto_usuario.alterar_senha(nova_senha)

        return self.usuarios.update_one(
            {"_id": id_usuario},
            {"$set": {"senha_hash": objeto_usuario.senha_hash}}
        )
