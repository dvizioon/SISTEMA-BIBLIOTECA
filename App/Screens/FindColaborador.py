import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import sys

sys.path.append(".")

from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml", "caminhoDB", index=0)

def buscar_colaboradores():
    try:
        conn = sqlite3.connect(buscaDB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Colaborador")
        colaboradores = cursor.fetchall()
        conn.close()
        return colaboradores
    except sqlite3.Error as e:
        print("Erro ao buscar colaboradores:", e)
        return []

def pesquisar_colaborador_por_cpf(cpf):
    try:
        conn = sqlite3.connect(buscaDB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Colaborador WHERE CPF=?", (cpf,))
        colaborador = cursor.fetchone()
        conn.close()
        return colaborador
    except sqlite3.Error as e:
        print("Erro ao pesquisar colaborador por CPF:", e)
        return None

def pesquisar_colaborador_por_nome(nome):
    try:
        conn = sqlite3.connect(buscaDB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Colaborador WHERE Nome LIKE ?", (f'%{nome}%',))
        colaboradores = cursor.fetchall()
        conn.close()
        return colaboradores
    except sqlite3.Error as e:
        print("Erro ao pesquisar colaborador por nome:", e)
        return None

def exibir_resultado_pesquisa(frame, largura, consulta, valor_consulta):
    print(valor_consulta)
    for widget in frame.winfo_children():
        widget.destroy()

    tabela = ttk.Treeview(frame, columns=("CPF", "Nome", "Email", "Cargo"), show="headings")
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")
    tabela.heading("CPF", text="CPF")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Email", text="Email")
    tabela.heading("Cargo", text="Cargo")

    colaboradores_encontrados = None
    if consulta == "CPF":
        colaboradores_encontrados = pesquisar_colaborador_por_cpf(valor_consulta)
    elif consulta == "Nome":
        colaboradores_encontrados = pesquisar_colaborador_por_nome(valor_consulta)

    if colaboradores_encontrados:
        for colaborador in colaboradores_encontrados:
            tabela.insert("", "end", values=colaborador)

    tabela.pack(fill="both", expand=True)

def FindColaborador(screen):
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    largura_tabela = 450

    # Adicione um widget Entry para que o usuário possa digitar o CPF ou Nome
    entrada_valor = tk.Entry(frame)
    entrada_valor.pack(pady=5)

    # Função para pesquisar e exibir resultados
    def pesquisar_e_exibir_resultados():
        tipo_pesquisa = var.get()
        valor_pesquisa = entrada_valor.get()

        # Verificar se o campo de entrada está vazio
        if not valor_pesquisa:
            messagebox.showwarning("Campo Vazio", "Por favor, insira um valor para pesquisa.")
            return

        # Realizar a pesquisa
        exibir_resultado_pesquisa(frame, largura_tabela, tipo_pesquisa, valor_pesquisa)

    # Adicione um checkbox para selecionar a opção de pesquisa por CPF ou Nome
    var = tk.StringVar(value="CPF")  # Definindo o valor inicial como "CPF"
    opcao_cpf = tk.Radiobutton(frame, text="CPF", variable=var, value="CPF", command=lambda: var.set("CPF"))
    opcao_cpf.pack(anchor="w")
    opcao_nome = tk.Radiobutton(frame, text="Nome", variable=var, value="Nome", command=lambda: var.set("Nome"))
    opcao_nome.pack(anchor="w")

    # Adicione um botão para iniciar a pesquisa
    botao_pesquisar = tk.Button(frame, text="Pesquisar", command=pesquisar_e_exibir_resultados)
    botao_pesquisar.pack(pady=5)

    return frame


# Criar a janela
# root = tk.Tk()
# root.geometry("300x450")
# root.title("Consulta de Colaboradores")
# FindColaborador(root)
# root.mainloop()
