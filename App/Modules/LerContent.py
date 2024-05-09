import os
import sys
sys.path.append(".")

def ler_arquivo(caminho_arquivo):
    # Verificar se o arquivo existe
    if os.path.exists(caminho_arquivo):
        # Se o arquivo existir, abra-o em modo de leitura
        with open(caminho_arquivo, "r") as arquivo:
            # Ler todo o conteúdo do arquivo
            conteudo = arquivo.read()
            
        # Retorna o conteúdo lido do arquivo
        return conteudo
    else:
        # Se o arquivo não existir, retorna None
        return None

# # Caminho para o arquivo
# caminho_arquivo = "C:\\Users\\Daniel\\Desktop\\AngueraBook\\App\\Email\\archive\\msgPadrao.txt"

# # Chama a função para ler o arquivo e obter seu conteúdo
# conteudo_arquivo = ler_arquivo(caminho_arquivo)

# # Verifica se o conteúdo do arquivo é None (arquivo não existe)
# if conteudo_arquivo is not None:
#     # Se o conteúdo não for None, imprime-o
#     print(conteudo_arquivo)
# else:
#     print("O arquivo não existe.")
