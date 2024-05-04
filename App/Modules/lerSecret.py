import json

def carregar_usuarios(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            dados = json.load(arquivo)
        return dados
    except FileNotFoundError:
        print(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON '{caminho_arquivo}'. Verifique a formatação.")
        return {}
    except Exception as e:
        print(f"Ocorreu um erro ao carregar os usuários: {e}")
        return {}

# Exemplo de uso:
# caminho_usuarios = "./secret/users.json"
# usuarios = carregar_usuarios(caminho_usuarios)
# print(usuarios)
