import sys
sys.path.append(".")
import hashlib
from App.Modules.lerSecret import carregar_usuarios
import time

def autenticar(usuario, senha):
    """
    Função para autenticar um usuário.

    Parâmetros:
        usuario (str): Nome de usuário.
        senha (str): Senha do usuário.

    Retorna:
        bool: True se a autenticação for bem-sucedida, False caso contrário.
    """

    usuarios = carregar_usuarios("./secret/users.json")
    
    # Função para verificar se o usuário existe
    def verificar_usuario(user):
        return user['usuario'] == usuario
    
    for user in usuarios:
        if verificar_usuario(user):
            # Criar a hash da senha fornecida
            senha_hash_fornecida = hashlib.sha256(senha.encode()).hexdigest()
            # Comparar a hash da senha fornecida com a senha_hash armazenada no dicionário do usuário
            if user['senha_hash'] == senha_hash_fornecida:
                return True
    return False

# # Exemplo de uso:
# usuario = "usuario1"
# senha = "senha123"

# if autenticar(usuario, senha):
#     print("Autenticação bem-sucedida!")
# else:
#     print("Nome de usuário ou senha incorretos.")
