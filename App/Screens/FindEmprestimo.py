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
    try:
        conn = sqlite3.connect(buscaDB)
        cursor = conn.cursor()
        cursor.execute("SELECT livroIsbn, colaboradorCpf, dataEmprestimo, dataDevolucao FROM Emprestimo WHERE livroIsbn=?", (isbn,))
        emprestimos = cursor.fetchall()
        conn.close()
        return emprestimos
    except sqlite3.Error as e:
        print("Erro ao pesquisar empréstimo por ISBN:", e)
        return None
    
def pesquisar_emprestimo_por_cpf(cpf):
    try:
        conn = sqlite3.connect(buscaDB)
        cursor = conn.cursor()
        cursor.execute("SELECT livroIsbn, colaboradorCpf, dataEmprestimo, dataDevolucao FROM Emprestimo WHERE colaboradorCpf=?", (cpf,))
        emprestimos = cursor.fetchall()
        conn.close()
        return emprestimos
    except sqlite3.Error as e:
        print("Erro ao pesquisar empréstimo por CPF do colaborador:", e)
        return None



def exibir_resultado_pesquisa(frame, largura, consulta, valor_consulta):
    print(valor_consulta)
    for widget in frame.winfo_children():
        widget.destroy()

    tabela = ttk.Treeview(frame, columns=("ISBN", "CPF Colaborador", "Data Empréstimo", "Data Devolução"), show="headings")
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")
    tabela.heading("ISBN", text="ISBN")
    tabela.heading("CPF Colaborador", text="CPF Colaborador")
    tabela.heading("Data Empréstimo", text="Data Empréstimo")
    tabela.heading("Data Devolução", text="Data Devolução")

    emprestimos_encontrados = None
    if consulta == "ISBN":
        emprestimos_encontrados = pesquisar_emprestimo_por_isbn(valor_consulta)
    elif consulta == "CPF":
        emprestimos_encontrados = pesquisar_emprestimo_por_cpf(valor_consulta)

    if emprestimos_encontrados:
        for emprestimo in emprestimos_encontrados:
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
