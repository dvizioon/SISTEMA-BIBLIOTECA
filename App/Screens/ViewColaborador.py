import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys

sys.path.append(".")
from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml","caminhoDB",index=0)


def buscar_colaboradores():

    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Colaborador")
    colaboradores = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    return colaboradores

def exibir_colaboradores(frame, largura):
    # Limpar o frame antes de adicionar a tabela
    for widget in frame.winfo_children():
        widget.destroy()

    # Criar a tabela para exibir os colaboradores
    tabela = ttk.Treeview(frame, columns=("CPF", "Nome", "Email", "Cargo"), show="headings")

    # Definir as larguras das colunas
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")  # Distribuir a largura igualmente entre as colunas

    # Definir o cabeçalho das colunas
    tabela.heading("CPF", text="CPF")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Email", text="Email")
    tabela.heading("Cargo", text="Cargo")

    # Buscar os colaboradores do banco de dados
    colaboradores = buscar_colaboradores()

    # Adicionar os colaboradores à tabela
    for colaborador in colaboradores:
        tabela.insert("", "end", values=colaborador)

    # Configurar o layout da tabela
    tabela.pack(fill="both", expand=True)

def screenViewColaborador(screen):
    # Criar o frame onde a tabela será exibida
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    # Configurar a largura da tabela para 450 pixels
    largura_tabela = 450

    # Chamar a função para exibir a tabela de colaboradores no frame especificado
    exibir_colaboradores(frame, largura_tabela)
    
    return frame

# # Criar a janela
# root = tk.Tk()
# root.geometry("300x450")
# root.title("Lista de Alunos")
# screenViewAluno(root)
# root.mainloop()
