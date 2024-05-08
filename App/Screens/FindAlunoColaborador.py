import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
import customtkinter as ctk

sys.path.append(".")

from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml","caminhoDB",index=0)

def buscar_colaboradores():
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Colaborador")
    colaboradores = cursor.fetchall()
    conn.close()
    return colaboradores

def pesquisar_colaborador_por_cpf(cpf):
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Colaborador WHERE CPF=?", (cpf,))
    colaborador = cursor.fetchone()
    conn.close()
    return colaborador

def pesquisar_colaborador_por_nome(nome):
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Colaborador WHERE Nome=?", (nome,))
    colaborador = cursor.fetchone()
    conn.close()
    return colaborador

def exibir_colaboradores(frame, largura):
    for widget in frame.winfo_children():
        widget.destroy()

    tabela = ttk.Treeview(frame, columns=("CPF", "Nome", "Email", "Cargo"), show="headings")
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")
    tabela.heading("CPF", text="CPF")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Email", text="Email")
    tabela.heading("Cargo", text="Cargo")

    colaboradores = buscar_colaboradores()

    for colaborador in colaboradores:
        tabela.insert("", "end", values=colaborador)

    tabela.pack(fill="both", expand=True)

def FindColaborador(screen):
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    largura_tabela = 450

    entrada_valor = tk.Entry(frame)
    entrada_valor.pack(pady=5)

    var = tk.StringVar(value="CPF")  # Definindo o valor inicial como "CPF"
    opcao_cpf = tk.Radiobutton(frame, text="CPF", variable=var, value="CPF")
    opcao_cpf.pack(anchor="w")
    opcao_nome = tk.Radiobutton(frame, text="Nome", variable=var, value="Nome")
    opcao_nome.pack(anchor="w")

    botao_pesquisar = ctk.CTkButton(frame, text="Pesquisar", command=lambda: exibir_resultado_pesquisa(frame, largura_tabela, var.get(), entrada_valor.get()))
    botao_pesquisar.pack(pady=5)

    botao_imprimir = ctk.CTkButton(frame, text="Imprimir Colaborador", command=lambda: imprimir_colaborador(frame, var.get(), entrada_valor.get()))
    botao_imprimir.pack()

    return frame

def exibir_resultado_pesquisa(frame, largura, consulta, valor_consulta):
    for widget in frame.winfo_children():
        widget.destroy()

    tabela = ttk.Treeview(frame, columns=("CPF", "Nome", "Email", "Cargo"), show="headings")
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")
    tabela.heading("CPF", text="CPF")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Email", text="Email")
    tabela.heading("Cargo", text="Cargo")

    colaborador_encontrado = None
    if consulta == "CPF":
        colaborador_encontrado = pesquisar_colaborador_por_cpf(valor_consulta)
    elif consulta == "Nome":
        colaborador_encontrado = pesquisar_colaborador_por_nome(valor_consulta)

    if colaborador_encontrado:
        tabela.insert("", "end", values=colaborador_encontrado)

    tabela.pack(fill="both", expand=True)

def imprimir_colaborador(frame, consulta, valor_consulta):
    colaborador = None
    if consulta == "CPF":
        colaborador = pesquisar_colaborador_por_cpf(valor_consulta)
    elif consulta == "Nome":
        colaborador = pesquisar_colaborador_por_nome(valor_consulta)

    if colaborador:
        # Implemente a função de impressão do colaborador
        print("Colaborador encontrado:", colaborador)
    else:
        print("Colaborador não encontrado.")

# Criar a janela
# root = tk.Tk()
# root.geometry("300x450")
# root.title("Consulta de Colaboradores")
# FindColaborador(root)
# root.mainloop()
