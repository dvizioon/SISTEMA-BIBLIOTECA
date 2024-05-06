import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import sys
import os

sys.path.append(".")
from App.Modules.LerYaml import LerYaml

# Definir as variáveis globais para os campos de entrada
entry_cpf = None
entry_nome = None
entry_email = None
entry_cargo = None

buscaDB = LerYaml(".Yaml","caminhoDB")


# root = ctk.CTk()
# root.title("Formulário de Adição de Colaborador")

def adicionar_colaborador():
    global entry_cpf, entry_nome, entry_email, entry_cargo  # Acessar as variáveis globais

    cpf = entry_cpf.get()
    nome = entry_nome.get()
    email = entry_email.get()
    cargo = entry_cargo.get()

    if not cpf or not nome:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:

        conexao = sqlite3.connect(f"{buscaDB}")
        cursor = conexao.cursor()

        comando_sql = "INSERT INTO Colaborador (cpf, nome, email, cargo) VALUES (?, ?, ?, ?)"
        valores = (cpf, nome, email, cargo)
        cursor.execute(comando_sql, valores)

        conexao.commit()

        messagebox.showinfo("Sucesso", "Colaborador adicionado com sucesso!")

        entry_cpf.delete(0, ctk.END)
        entry_nome.delete(0, ctk.END)
        entry_email.delete(0, ctk.END)
        entry_cargo.delete(0, ctk.END)

    except sqlite3.Error as erro:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o colaborador: {erro}")

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def screenAddColaborador(frame):
    global entry_cpf, entry_nome, entry_email, entry_cargo  # Acessar as variáveis globais

    # Criando um frame principal para conter todos os widgets
    frame_principal = ctk.CTkFrame(frame)
    frame_principal.pack(expand=True, fill="both")

    # Criando e posicionando os widgets dentro do frame principal
    label_cpf = ctk.CTkLabel(frame_principal, text="CPF:")
    label_cpf.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_cpf = ctk.CTkEntry(frame_principal)
    entry_cpf.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    label_nome = ctk.CTkLabel(frame_principal, text="Nome:")
    label_nome.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nome = ctk.CTkEntry(frame_principal)
    entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    label_email = ctk.CTkLabel(frame_principal, text="Email:")
    label_email.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_email = ctk.CTkEntry(frame_principal)
    entry_email.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    label_cargo = ctk.CTkLabel(frame_principal, text="Cargo:")
    label_cargo.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_cargo = ctk.CTkEntry(frame_principal)
    entry_cargo.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    button_adicionar = ctk.CTkButton(frame_principal, text="Adicionar Colaborador", command=adicionar_colaborador)
    button_adicionar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    frame_principal.grid_columnconfigure(1, weight=1)
    
    return frame_principal

# screenAddColaborador(root)

# root.mainloop()
