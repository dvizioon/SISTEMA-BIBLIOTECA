import tkinter as tk
from tkinter import ttk
import sqlite3
import customtkinter as ctk
import sys

sys.path.append(".")

from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml","caminhoDB",index=0)

def buscar_emprestimos():
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Emprestimo")
    emprestimos = cursor.fetchall()
    conn.close()
    return emprestimos

def pesquisar_emprestimo_por_isbn(isbn):
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Emprestimo WHERE ISBN=?", (isbn,))
    emprestimo = cursor.fetchone()
    conn.close()
    return emprestimo

def pesquisar_emprestimo_por_cpf(cpf):
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Emprestimo WHERE CPF_Colaborador=?", (cpf,))
    emprestimo = cursor.fetchone()
    conn.close()
    return emprestimo

def exibir_emprestimos(frame, largura):
    for widget in frame.winfo_children():
        widget.destroy()

    tabela = ttk.Treeview(frame, columns=("ID", "Data Empréstimo", "Data Devolução", "ISBN Livro", "CPF Colaborador"), show="headings")
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 5, anchor="center")
    tabela.heading("ID", text="ID")
    tabela.heading("Data Empréstimo", text="Data Empréstimo")
    tabela.heading("Data Devolução", text="Data Devolução")
    tabela.heading("ISBN Livro", text="ISBN Livro")
    tabela.heading("CPF Colaborador", text="CPF Colaborador")

    emprestimos = buscar_emprestimos()

    for emprestimo in emprestimos:
        tabela.insert("", "end", values=emprestimo)

    tabela.pack(fill="both", expand=True)

def FindEmprestimo(screen):
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    largura_tabela = 600

    entrada_valor = tk.Entry(frame)
    entrada_valor.pack(pady=5)

    var = tk.StringVar(value="ISBN")  # Definindo o valor inicial como "ISBN"
    opcao_isbn = tk.Radiobutton(frame, text="ISBN", variable=var, value="ISBN")
    opcao_isbn.pack(anchor="w")
    opcao_cpf = tk.Radiobutton(frame, text="CPF Colaborador", variable=var, value="CPF")
    opcao_cpf.pack(anchor="w")

    botao_pesquisar = ctk.CTkButton(frame, text="Pesquisar", command=lambda: exibir_resultado_pesquisa(frame, largura_tabela, var.get(), entrada_valor.get()))
    botao_pesquisar.pack(pady=5)

    botao_imprimir = ctk.CTkButton(frame, text="Imprimir Empréstimo", command=lambda: imprimir_emprestimo(frame, var.get(), entrada_valor.get()))
    botao_imprimir.pack()

    return frame

def exibir_resultado_pesquisa(frame, largura, consulta, valor_consulta):
    for widget in frame.winfo_children():
        widget.destroy()

    tabela = ttk.Treeview(frame, columns=("ID", "Data Empréstimo", "Data Devolução", "ISBN Livro", "CPF Colaborador"), show="headings")
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 5, anchor="center")
    tabela.heading("ID", text="ID")
    tabela.heading("Data Empréstimo", text="Data Empréstimo")
    tabela.heading("Data Devolução", text="Data Devolução")
    tabela.heading("ISBN Livro", text="ISBN Livro")
    tabela.heading("CPF Colaborador", text="CPF Colaborador")

    emprestimo_encontrado = None
    if consulta == "ISBN":
        emprestimo_encontrado = pesquisar_emprestimo_por_isbn(valor_consulta)
    elif consulta == "CPF":
        emprestimo_encontrado = pesquisar_emprestimo_por_cpf(valor_consulta)

    if emprestimo_encontrado:
        tabela.insert("", "end", values=emprestimo_encontrado)

    tabela.pack(fill="both", expand=True)

def imprimir_emprestimo(frame, consulta, valor_consulta):
    emprestimo = None
    if consulta == "ISBN":
        emprestimo = pesquisar_emprestimo_por_isbn(valor_consulta)
    elif consulta == "CPF":
        emprestimo = pesquisar_emprestimo_por_cpf(valor_consulta)

    if emprestimo:
        # Implemente a função de impressão do empréstimo
        print("Empréstimo encontrado:", emprestimo)
    else:
        print("Empréstimo não encontrado.")

# Criar a janela
# root = tk.Tk()
# root.geometry("600x450")
# root.title("Consulta de Empréstimos")
# FindEmprestimo(root)
# root.mainloop()
