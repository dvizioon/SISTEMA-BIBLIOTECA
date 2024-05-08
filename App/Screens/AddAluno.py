import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
import yaml
sys.path.append(".")
from App.Modules.LerYaml import LerYaml

# Definir as variáveis globais para os campos de entrada
entry_ra = None
entry_nome = None
entry_email = None
entry_telefone = None

buscaDB = LerYaml(".Yaml","caminhoDB",index=0)

def adicionar_aluno():
    global entry_ra, entry_nome, entry_email, entry_telefone  # Acessar as variáveis globais

    ra = entry_ra.get()
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()

    if not ra or not nome:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:
        conexao = sqlite3.connect(f"{buscaDB}")
        cursor = conexao.cursor()

        comando_sql = "INSERT INTO Aluno (ra, nome, email, telefone) VALUES (?, ?, ?, ?)"
        valores = (ra, nome, email, telefone)
        cursor.execute(comando_sql, valores)

        conexao.commit()

        messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")

        entry_ra.delete(0, ctk.END)
        entry_nome.delete(0, ctk.END)
        entry_email.delete(0, ctk.END)
        entry_telefone.delete(0, ctk.END)

    except sqlite3.Error as erro:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o aluno: {erro}")

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

root = ctk.CTk()
root.title("Formulário de Adição de Aluno")

def screenAddAluno(frame):
    global entry_ra, entry_nome, entry_email, entry_telefone  # Acessar as variáveis globais

    # Criando um frame principal para conter todos os widgets
    frame_principal = ctk.CTkFrame(frame)
    frame_principal.pack(expand=True, fill="both")

    # Criando e posicionando os widgets dentro do frame principal
    label_ra = ctk.CTkLabel(frame_principal, text="RA:")
    label_ra.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_ra = ctk.CTkEntry(frame_principal)
    entry_ra.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    label_nome = ctk.CTkLabel(frame_principal, text="Nome:")
    label_nome.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nome = ctk.CTkEntry(frame_principal)
    entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    label_email = ctk.CTkLabel(frame_principal, text="Email:")
    label_email.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_email = ctk.CTkEntry(frame_principal)
    entry_email.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    label_telefone = ctk.CTkLabel(frame_principal, text="Telefone:")
    label_telefone.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_telefone = ctk.CTkEntry(frame_principal)
    entry_telefone.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    button_adicionar = ctk.CTkButton(frame_principal, text="Adicionar Aluno", command=adicionar_aluno)
    button_adicionar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    frame_principal.grid_columnconfigure(1, weight=1)
    # root.grid_columnconfigure(0, weight=1) 
    
    return frame_principal

# screenAddAluno(root)

# root.mainloop()
