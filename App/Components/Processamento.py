import sys
import json
sys.path.append(".")

def ler_json(caminho_arquivo, nome_chave):
    try:
        with open(caminho_arquivo) as arquivo_json:
            conteudo_json = json.load(arquivo_json)
            if nome_chave in conteudo_json[0]:
                return conteudo_json[0][nome_chave]
            else:
                print(f"A chave '{nome_chave}' não foi encontrada no arquivo JSON.")
                return None
    except FileNotFoundError:
        print(f"O arquivo {caminho_arquivo} não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo JSON: {e}")
        return None

# Exemplo de uso
def prefix_process(_c_,_p_):
    caminho_arquivo = _c_
    nome_chave = _p_
    valor_chave = ler_json(caminho_arquivo, nome_chave)
    return valor_chave

# # Exemplo de uso
# caminho_arquivo = "_pfx.json"
# nome_chave = "_prf_"
# valor_chave = ler_json(caminho_arquivo, nome_chave)

# if valor_chave is not None:
#     print(f"Valor da chave '{nome_chave}': {valor_chave}")
# else:
#     print("Não foi possível ler o valor da chave ou a chave especificada não foi encontrada.")
