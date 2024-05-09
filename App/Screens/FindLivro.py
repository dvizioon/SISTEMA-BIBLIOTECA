import tkinter as tk
from tkinter import ttk
import sqlite3
import customtkinter as ctk
from tkinter import messagebox
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
    try:
        conn = sqlite3.connect(buscaDB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Livro WHERE isbn=?", (isbn,))
        livro = cursor.fetchone()
        conn.close()
        return livro
    except sqlite3.Error as e:
        print("Erro ao pesquisar livro por ISBN:", e)
        return None

def pesquisar_livro_por_autor(autor):
    try:
        conn = sqlite3.connect(buscaDB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Livro WHERE autor=?", (autor,))
        livros = cursor.fetchall()
        conn.close()
        return livros
    except sqlite3.Error as e:
        print("Erro ao pesquisar livro por autor:", e)
        return None


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

    livros_encontrados = None
    if consulta == "ISBN":
        livros_encontrados = pesquisar_livro_por_isbn(valor_consulta)
    elif consulta == "Autor":
        livros_encontrados = pesquisar_livro_por_autor(valor_consulta)

    if livros_encontrados:
        for livro in livros_encontrados:
            tabela.insert("", "end", values=livro)

    tabela.pack(fill="both", expand=True)

def FindLivro(screen):
    frame = tk.Frame(screen)
    frame.pack(fill="both", expand=True)

    largura_tabela = 450

    # Adicione um widget Entry para que o usuário possa digitar o ISBN ou Autor
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

    # Adicione um checkbox para selecionar a opção de pesquisa por ISBN ou Autor
    var = tk.StringVar(value="ISBN")  # Definindo o valor inicial como "ISBN"
    opcao_isbn = tk.Radiobutton(frame, text="ISBN", variable=var, value="ISBN", command=lambda: var.set("ISBN"))
    opcao_isbn.pack(anchor="w")
    opcao_autor = tk.Radiobutton(frame, text="Autor", variable=var, value="Autor", command=lambda: var.set("Autor"))
    opcao_autor.pack(anchor="w")

    # Adicione um botão para iniciar a pesquisa
    botao_pesquisar = ctk.CTkButton(frame, text="Pesquisar", command=pesquisar_e_exibir_resultados)
    botao_pesquisar.pack(pady=5)

    # Adicione um botão para imprimir o livro
    botao_imprimir = ctk.CTkButton(frame, text="Imprimir Livro", command=lambda: imprimir_livro(frame, var.get(), entrada_valor.get()))
    botao_imprimir.pack()

    return frame




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
