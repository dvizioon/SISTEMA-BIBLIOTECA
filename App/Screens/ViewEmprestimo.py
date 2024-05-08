import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys

sys.path.append(".")
from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml","caminhoDB",index=0)


def buscar_emprestimos():

    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Emprestimo")
    emprestimos = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    return emprestimos

def exibir_emprestimos(frame, largura):
    # Limpar o frame antes de adicionar a tabela
    for widget in frame.winfo_children():
        widget.destroy()

    # Criar a tabela para exibir os empréstimos
    tabela = ttk.Treeview(frame, columns=("ID", "Data Empréstimo", "Data Devolução", "ISBN Livro", "CPF Colaborador"), show="headings")

    # Definir as larguras das colunas
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 5, anchor="center")  # Distribuir a largura igualmente entre as colunas

    # Definir o cabeçalho das colunas
    tabela.heading("ID", text="ID")
    tabela.heading("Data Empréstimo", text="Data Empréstimo")
    tabela.heading("Data Devolução", text="Data Devolução")
    tabela.heading("ISBN Livro", text="ISBN Livro")
    tabela.heading("CPF Colaborador", text="CPF Colaborador")

    # Buscar os empréstimos do banco de dados
    emprestimos = buscar_emprestimos()

    # Adicionar os empréstimos à tabela
    for emprestimo in emprestimos:
        tabela.insert("", "end", values=emprestimo)

    # Configurar o layout da tabela
    tabela.pack(fill="both", expand=True)

def screenViewEmprestimo(screen):
    # Criar o frame onde a tabela será exibida
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    # Configurar a largura da tabela para 450 pixels
    largura_tabela = 600

    # Chamar a função para exibir a tabela de empréstimos no frame especificado
    exibir_emprestimos(frame, largura_tabela)
    
    return frame

# # Criar a janela
# root = tk.Tk()
# root.geometry("600x450")
# root.title("Lista de Empréstimos")
# screenViewEmprestimo(root)
# root.mainloop()
