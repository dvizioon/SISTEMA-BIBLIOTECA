import tkinter as tk
from tkinter import ttk
import sqlite3
import customtkinter as ctk
import sys
sys.path.append(".")

from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml","caminhoDB",index=0)

def buscar_livros():
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Livro")
    livros = cursor.fetchall()
    conn.close()
    return livros

def pesquisar_livro_por_isbn(isbn):
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Livro WHERE ISBN=?", (isbn,))
    livro = cursor.fetchone()
    conn.close()
    return livro

def pesquisar_livro_por_autor(autor):
    conn = sqlite3.connect(f"{buscaDB}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Livro WHERE Autor=?", (autor,))
    livro = cursor.fetchone()
    conn.close()
    return livro

def exibir_livros(frame, largura):
    for widget in frame.winfo_children():
        widget.destroy()

    tabela = ttk.Treeview(frame, columns=("ISBN", "Título", "Autor", "Páginas"), show="headings")
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")
    tabela.heading("ISBN", text="ISBN")
    tabela.heading("Título", text="Título")
    tabela.heading("Autor", text="Autor")
    tabela.heading("Páginas", text="Páginas")

    livros = buscar_livros()

    for livro in livros:
        tabela.insert("", "end", values=livro)

    tabela.pack(fill="both", expand=True)

def FindLivro(screen):
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    largura_tabela = 450

    entrada_valor = tk.Entry(frame)
    entrada_valor.pack(pady=5)

    var = tk.StringVar(value="ISBN")  # Definindo o valor inicial como "ISBN"
    opcao_isbn = tk.Radiobutton(frame, text="ISBN", variable=var, value="ISBN")
    opcao_isbn.pack(anchor="w")
    opcao_autor = tk.Radiobutton(frame, text="Autor", variable=var, value="Autor")
    opcao_autor.pack(anchor="w")

    botao_pesquisar = ctk.CTkButton(frame, text="Pesquisar", command=lambda: exibir_resultado_pesquisa(frame, largura_tabela, var.get(), entrada_valor.get()))
    botao_pesquisar.pack(pady=5)

    botao_imprimir = ctk.CTkButton(frame, text="Imprimir Livro", command=lambda: imprimir_livro(frame, var.get(), entrada_valor.get()))
    botao_imprimir.pack()

    return frame

def exibir_resultado_pesquisa(frame, largura, consulta, valor_consulta):
    for widget in frame.winfo_children():
        widget.destroy()

    tabela = ttk.Treeview(frame, columns=("ISBN", "Título", "Autor", "Páginas"), show="headings")
    for coluna in tabela["columns"]:
        tabela.column(coluna, width=largura // 4, anchor="center")
    tabela.heading("ISBN", text="ISBN")
    tabela.heading("Título", text="Título")
    tabela.heading("Autor", text="Autor")
    tabela.heading("Páginas", text="Páginas")

    livro_encontrado = None
    if consulta == "ISBN":
        livro_encontrado = pesquisar_livro_por_isbn(valor_consulta)
    elif consulta == "Autor":
        livro_encontrado = pesquisar_livro_por_autor(valor_consulta)

    if livro_encontrado:
        tabela.insert("", "end", values=livro_encontrado)

    tabela.pack(fill="both", expand=True)

def imprimir_livro(frame, consulta, valor_consulta):
    livro = None
    if consulta == "ISBN":
        livro = pesquisar_livro_por_isbn(valor_consulta)
    elif consulta == "Autor":
        livro = pesquisar_livro_por_autor(valor_consulta)

    if livro:
        # Implemente a função de impressão do livro
        print("Livro encontrado:", livro)
    else:
        print("Livro não encontrado.")

# Criar a janela
# root = tk.Tk()
# root.geometry("300x450")
# root.title("Consulta de Livros")
# FindLivro(root)
# root.mainloop()
