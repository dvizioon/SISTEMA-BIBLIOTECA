import json
import os
import hashlib
import random
import string
from datetime import datetime

def ler_usuarios(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as file:
            try:
                usuarios = json.load(file)
            except json.decoder.JSONDecodeError:
                usuarios = []
        return usuarios
    else:
        return []

def gerar_id_aleatorio():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def usuario_existe(usuario, usuarios):
    for u in usuarios:
        if u["usuario"] == usuario:
            return True
    return False

def salvar_usuario(usuario, senha, caminho_arquivo):
    usuarios = ler_usuarios(caminho_arquivo)
    
    if usuario_existe(usuario, usuarios):
        print("Usuário já existe!")
        return
    
    id_usuario = gerar_id_aleatorio()
    hash_senha = hashlib.sha256(senha.encode()).hexdigest()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    novo_usuario = {
        "id": id_usuario,
        "usuario": usuario,
        "senha_hash": hash_senha,
        "criacao": timestamp,
        "atualizacao": timestamp,
        "img": ""
    }
    usuarios.append(novo_usuario)
    with open(caminho_arquivo, 'w') as file:
        json.dump(usuarios, file, indent=4)

# Exemplo de uso
# usuario = "usuario1"
# senha = "senha123"

# caminho_arquivo = "./secret/users.json"
# salvar_usuario(usuario, senha, caminho_arquivo)
