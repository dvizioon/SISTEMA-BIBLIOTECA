import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
import customtkinter as ctk

sys.path.append(".")

from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml","caminhoDB",index=0)

def buscar_alunos():
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Aluno")
    alunos = cursor.fetchall()
    conn.close()
    return alunos

def pesquisar_aluno_por_ra(ra):
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Aluno WHERE RA=?", (ra,))
    aluno = cursor.fetchone()
    conn.close()
    return aluno

def pesquisar_aluno_por_Nome(Nome):
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Aluno WHERE Nome=?", (Nome,))
    aluno = cursor.fetchone()
    conn.close()
    return aluno

def exibir_resultado_pesquisa(frame, largura, consulta, valor_consulta):
    for widget in frame.winfo_children():
        widget.destroy()

    tabela = ttk.Treeview(frame, columns=("RA", "Nome", "Email", "Telefone"), show="headings")
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")
    tabela.heading("RA", text="RA")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Email", text="Email")
    tabela.heading("Telefone", text="Telefone")

    aluno_encontrado = None
    if consulta == "RA":
        aluno_encontrado = pesquisar_aluno_por_ra(valor_consulta)
    elif consulta == "Nome":
        aluno_encontrado = pesquisar_aluno_por_Nome(valor_consulta)

    if aluno_encontrado:
        tabela.insert("", "end", values=aluno_encontrado)

    tabela.pack(fill="both", expand=True)

def imprimir_aluno(frame, consulta, valor_consulta):
    aluno = None
    if consulta == "RA":
        aluno = pesquisar_aluno_por_ra(valor_consulta)
    elif consulta == "Nome":
        aluno = pesquisar_aluno_por_Nome(valor_consulta)

    if aluno:
        # Aqui você implementaria a função para imprimir o aluno
        print("Aluno encontrado:", aluno)
    else:
        print("Aluno não encontrado.")

def FindAluno(screen):
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    largura_tabela = 450

    # Adicione um widget Entry para que o usuário possa digitar o RA ou Nome
    entrada_valor = tk.Entry(frame)
    entrada_valor.pack(pady=5)

    # Adicione um checkbox para selecionar a opção de pesquisa por RA ou Nome
    var = tk.StringVar(value="RA")  # Definindo o valor inicial como "RA"
    opcao_ra = tk.Radiobutton(frame, text="RA", variable=var, value="RA")
    opcao_ra.pack(anchor="w")
    opcao_nome = tk.Radiobutton(frame, text="Nome", variable=var, value="Nome")
    opcao_nome.pack(anchor="w")

    # Adicione um botão para iniciar a pesquisa
    botao_pesquisar = ctk.CTkButton(frame, text="Pesquisar", command=lambda: exibir_resultado_pesquisa(frame, largura_tabela, var.get(), entrada_valor.get()))
    botao_pesquisar.pack(pady=5)

    # Adicione um botão para imprimir o aluno
    botao_imprimir = ctk.CTkButton(frame, text="Imprimir Aluno", command=lambda: imprimir_aluno(frame, var.get(), entrada_valor.get()))
    botao_imprimir.pack()

    return frame

# Criar a janela
# root = tk.Tk()
# root.geometry("300x450")
# root.title("Consulta de Alunos")
# FindAluno(root)
# root.mainloop()
