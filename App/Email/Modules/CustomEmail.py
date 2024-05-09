import tkinter as tk
from tkinter import ttk
import os
import sys
import re
from bs4 import BeautifulSoup

sys.path.append(".")

from App.Modules.LerContent import ler_arquivo

# Função para salvar a mensagem
def salvar_mensagem():
    global texto_mensagem, arquivo_nome
    
    mensagem = texto_mensagem.get("1.0", "end-1c")      
        
    with open(arquivo_nome, "w", encoding="utf-8") as arquivo:
        arquivo.write(mensagem)  # Correção aqui: use 'mensagem' em vez de 'texto_mensagem'

    print("Mensagem salva com sucesso!")



# Configuração da janela principal
# root = tk.Tk()
# root.title("Editor de Mensagens")
# root.geometry("400x300")

# Função para configurar a tela de mensagem padrão do aluno
def customEmail(root, a_nome):
    global arquivo_nome, texto_mensagem
    
    arquivo_nome = a_nome
    
    # Frame para a entrada de texto
    frame_texto = ttk.Frame(root)
    frame_texto.pack(padx=10, pady=10, fill="both", expand=True)

    # Textarea para inserir a mensagem
    texto_mensagem = tk.Text(frame_texto, height=10, width=50)
    # Textarea para inserir a mensagem
    texto_mensagem = tk.Text(frame_texto, height=10, width=50)
    if os.path.exists(a_nome):
        with open(a_nome, "r", encoding="utf-8") as arquivo:
            texto = arquivo.read()
            texto_mensagem.insert("1.0", texto)
    else:
        print("O arquivo não existe.")
        texto_mensagem.insert("1.0", "")
    texto_mensagem.pack(padx=10, pady=10, fill="both", expand=True)
    texto_mensagem.pack(padx=10, pady=10, fill="both", expand=True)

    # Botão para salvar a mensagem
    botao_salvar = ttk.Button(root, text="Salvar", command=salvar_mensagem)
    botao_salvar.pack(pady=(0, 10))

# customEmail(root, "App/Email/archive/msgCustom_a.txt")
# root.mainloop()
