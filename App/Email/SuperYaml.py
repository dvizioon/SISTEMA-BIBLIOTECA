import tkinter as tk
from tkinter import messagebox
import sys
import os
import yaml

sys.path.append(".")

def LerYaml(nome_arquivo_yaml, variavel, index=None):
    if not os.path.exists(nome_arquivo_yaml):
        messagebox.showerror("Erro", "Arquivo YAML não encontrado")
        return None
    
    with open(nome_arquivo_yaml, 'r') as arquivo:
        conteudo = yaml.safe_load(arquivo)
        valor = conteudo.get(variavel)
        
        if valor is None:
            messagebox.showerror("Erro", f"A variável '{variavel}' não foi encontrada no arquivo YAML")
            return None
        
        if isinstance(valor, list):
            if index is not None:
                return valor[index] if 0 <= index < len(valor) else None
            else:
                return valor[0] if len(valor) == 1 else valor
        else:
            return valor

def ModificarYaml(nome_arquivo_yaml, variavel, index, novo_valor):
    if not os.path.exists(nome_arquivo_yaml):
        messagebox.showerror("Erro", "Arquivo YAML não encontrado")
        return False
    
    with open(nome_arquivo_yaml, 'r') as arquivo:
        conteudo = yaml.safe_load(arquivo)
        
        valor = conteudo.get(variavel)
        if valor is None:
            messagebox.showerror("Erro", f"A variável '{variavel}' não foi encontrada no arquivo YAML")
            return False
        
        if isinstance(valor, list):
            if 0 <= index < len(valor):
                conteudo[variavel][index] = novo_valor
            else:
                messagebox.showerror("Erro", "Índice fora do intervalo")
                return False
        else:
            messagebox.showerror("Erro", f"A variável '{variavel}' não é uma lista")
            return False
    
    with open(nome_arquivo_yaml, 'w') as arquivo:
        yaml.dump(conteudo, arquivo, default_flow_style=False)
    
    return True

# Exemplo de uso:
# url = LerYaml("arquivo.yaml", "url")
# print(url)

# url2 = LerYaml("arquivo.yaml", "url", index=1)  # Retorna o segundo elemento da lista na seção "url"
# print(url2)

# Modificar o valor do segundo item da lista associada à chave "url" para "http://exemplo.com"
# ModificarYaml("arquivo.yaml", "url", 1, "http://exemplo.com")
