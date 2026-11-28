
import bcrypt


class Usuario:
    def __init__(self, nome, usuario, senha, perfil="OPERADOR", ativo=True, id=None):
        self.id = id
        self.nome = nome
        self.usuario = usuario
        self.perfil = perfil
        self.ativo = ativo
        self.senha_hash = self.gerar_hash(senha)

    def gerar_hash(self, senha):
        senha_bytes = senha.encode("utf-8")
        return bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode("utf-8")

    def validar_senha(self, senha):
        senha_bytes = senha.encode("utf-8")
        hash_bytes = self.senha_hash.encode("utf-8")

        return bcrypt.checkpw(senha_bytes, hash_bytes)

    def alterar_senha(self, nova_senha):
        if len(nova_senha) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")

        self.senha_hash = self.gerar_hash(nova_senha)

    def alterar_perfil(self, novo_perfil):
        if novo_perfil not in ["ADMIN", "OPERADOR"]:
            raise ValueError("Perfil inválido.")

        self.perfil = novo_perfil

    def ativar(self):
        self.ativo = True

    def desativar(self):
        self.ativo = False

    def to_document(self):
        return {
            "nome": self.nome,
            "usuario": self.usuario,
            "senha_hash": self.senha_hash,
            "perfil": self.perfil,
            "ativo": self.ativo
        }

    def __str__(self):
        return (
            f"Usuário: {self.usuario} | "
            f"Nome: {self.nome} | "
            f"Perfil: {self.perfil} | "
            f"Ativo: {self.ativo}"
        )
