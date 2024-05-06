import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys

sys.path.append(".")

from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml","caminhoDB")

# Função para buscar todos os alunos no banco de dados
def buscar_alunos():

    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Aluno")
    alunos = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    return alunos

# Função para criar e exibir a tabela de alunos em um frame especificado
def exibir_alunos(frame, largura):
    # Limpar o frame antes de adicionar a tabela
    for widget in frame.winfo_children():
        widget.destroy()

    # Criar a tabela para exibir os alunos
    tabela = ttk.Treeview(frame, columns=("RA", "Nome", "Email", "Telefone"), show="headings")

    # Definir as larguras das colunas
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")  # Distribuir a largura igualmente entre as colunas

    # Definir o cabeçalho das colunas
    tabela.heading("RA", text="RA")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Email", text="Email")
    tabela.heading("Telefone", text="Telefone")

    # Buscar os alunos do banco de dados
    alunos = buscar_alunos()

    # Adicionar os alunos à tabela
    for aluno in alunos:
        tabela.insert("", "end", values=aluno)

    # Configurar o layout da tabela
    tabela.pack(fill="both", expand=True)

# Exemplo de uso em outra tela
def screenViewAluno(screen):
    # Criar o frame onde a tabela será exibida
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    # Configurar a largura da tabela para 450 pixels
    largura_tabela = 450

    # Chamar a função para exibir a tabela de alunos no frame especificado
    exibir_alunos(frame, largura_tabela)
    
    return frame

# # Criar a janela
# root = tk.Tk()
# root.geometry("300x450")
# root.title("Lista de Alunos")
# screenViewAluno(root)
# root.mainloop()
