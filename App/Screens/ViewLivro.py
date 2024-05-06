import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys

sys.path.append(".")

from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml","caminhoDB")



def buscar_livros():
    # Conexão com o banco de dados
    diretorio_atual = os.path.dirname(__file__)
    diretorio_pai = os.path.dirname(diretorio_atual)
    diretorio_pai = os.path.dirname(diretorio_pai)
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Livro")
    livros = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    return livros

def exibir_livros(frame, largura):
    # Limpar o frame antes de adicionar a tabela
    for widget in frame.winfo_children():
        widget.destroy()

    # Criar a tabela para exibir os livros
    tabela = ttk.Treeview(frame, columns=("ISBN", "Nome", "Autor", "Páginas"), show="headings")

    # Definir as larguras das colunas
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")  # Distribuir a largura igualmente entre as colunas

    # Definir o cabeçalho das colunas
    tabela.heading("ISBN", text="ISBN")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Autor", text="Autor")
    tabela.heading("Páginas", text="Páginas")

    # Buscar os livros do banco de dados
    livros = buscar_livros()

    # Adicionar os livros à tabela
    for livro in livros:
        tabela.insert("", "end", values=livro)

    # Configurar o layout da tabela
    tabela.pack(fill="both", expand=True)

def screenViewLivro(screen):
    # Criar o frame onde a tabela será exibida
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    # Configurar a largura da tabela para 450 pixels
    largura_tabela = 450

    # Chamar a função para exibir a tabela de livros no frame especificado
    exibir_livros(frame, largura_tabela)
    
    return frame

# Exemplo de uso em outra tela
# root = tk.Tk()
# root.geometry("300x450")
# root.title("Lista de Livros")
# screenViewLivro(root)
# root.mainloop()
