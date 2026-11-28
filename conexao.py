
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

cliente = None
banco = None


def conectar():
    global cliente, banco

    try:
        cliente = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        # Verifica se o MongoDB está acessível
        cliente.admin.command("ping")

        banco = cliente["EasyGest_PDV"]

        print("Conexão com MongoDB realizada!")
        return banco

    except Exception as erro:
        print(f"Erro na conexão: {erro}")
        return None


def fechar_conexao():
    global cliente

    if cliente:
        cliente.close()
        print("Conexão encerrada.")
