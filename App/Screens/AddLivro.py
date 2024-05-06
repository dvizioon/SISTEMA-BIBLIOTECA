import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import sys
import os

sys.path.append(".")

from App.Modules.LerYaml import LerYaml

# Definir as variáveis globais para os campos de entrada
entry_isbn = None
entry_nome = None
entry_autor = None
entry_paginas  = None

buscaDB = LerYaml(".Yaml","caminhoDB")

# root = ctk.CTk()
# root.title("Formulário de Adição de Livro")

def adicionar_livro():
    global entry_isbn, entry_nome, entry_autor, entry_paginas  # Acessar as variáveis globais

    isbn = entry_isbn.get()
    nome = entry_nome.get()
    autor = entry_autor.get()
    paginas = entry_paginas.get()

    if not isbn or not nome:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:

        conexao = sqlite3.connect(f"{buscaDB}")
        cursor = conexao.cursor()

        comando_sql = "INSERT INTO Livro (isbn, nome, autor, paginas) VALUES (?, ?, ?, ?)"
        valores = (isbn, nome, autor, paginas)
        cursor.execute(comando_sql, valores)

        conexao.commit()

        messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")

        entry_isbn.delete(0, ctk.END)
        entry_nome.delete(0, ctk.END)
        entry_autor.delete(0, ctk.END)
        entry_paginas.delete(0, ctk.END)

    except sqlite3.Error as erro:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o livro: {erro}")

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def screenAddLivro(frame):
    global entry_isbn, entry_nome, entry_autor, entry_paginas  # Acessar as variáveis globais

    # Criando um frame principal para conter todos os widgets
    frame_principal = ctk.CTkFrame(frame)
    frame_principal.pack(expand=True, fill="both")

    # Criando e posicionando os widgets dentro do frame principal
    label_isbn = ctk.CTkLabel(frame_principal, text="ISBN:")
    label_isbn.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_isbn = ctk.CTkEntry(frame_principal)
    entry_isbn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    label_nome = ctk.CTkLabel(frame_principal, text="Nome:")
    label_nome.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nome = ctk.CTkEntry(frame_principal)
    entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    label_autor = ctk.CTkLabel(frame_principal, text="Autor:")
    label_autor.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_autor = ctk.CTkEntry(frame_principal)
    entry_autor.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    label_paginas = ctk.CTkLabel(frame_principal, text="Páginas:")
    label_paginas.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_paginas = ctk.CTkEntry(frame_principal)
    entry_paginas.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    button_adicionar = ctk.CTkButton(frame_principal, text="Adicionar Livro", command=adicionar_livro)
    button_adicionar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    frame_principal.grid_columnconfigure(1, weight=1)
    
    return frame_principal


# screenAddLivro(root)

# root.mainloop()
