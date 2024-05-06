import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
from datetime import datetime, timedelta

sys.path.append(".")

from App.Modules.LerYaml import LerYaml

# Definir as variáveis globais para os campos de entrada
entry_data_emprestimo = None
combobox_isbn_livro = None
combobox_colaborador  = None

buscaDB = LerYaml(".Yaml","caminhoDB")

# root = ctk.CTk()
# root.title("Formulário de Criação de Empréstimo")

def adicionar_emprestimo():
    global entry_data_emprestimo, combobox_isbn_livro, combobox_colaborador  # Acessar as variáveis globais

    data_emprestimo = entry_data_emprestimo.get()
    isbn_livro = combobox_isbn_livro.get()
    colaborador_selecionado = combobox_colaborador.get()  # Obter o colaborador selecionado no combobox

    # Obter a data de devolução (7 dias após a data de empréstimo)
    data_devolucao = (datetime.strptime(data_emprestimo, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")

    if not data_emprestimo or not isbn_livro:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:
        conexao = sqlite3.connect(f"{buscaDB}")
        cursor = conexao.cursor()

        # Obter o CPF do colaborador selecionado
        cursor.execute("SELECT cpf FROM Colaborador WHERE nome = ?", (colaborador_selecionado,))
        cpf_colaborador = cursor.fetchone()[0]

        comando_sql = "INSERT INTO Emprestimo (dataEmprestimo, dataDevolucao, livroIsbn, colaboradorCpf) VALUES (?, ?, ?, ?)"
        valores = (data_emprestimo, data_devolucao, isbn_livro, cpf_colaborador)
        cursor.execute(comando_sql, valores)

        conexao.commit()

        messagebox.showinfo("Sucesso", "Empréstimo adicionado com sucesso!")

        entry_data_emprestimo.delete(0, ctk.END)

    except sqlite3.Error as erro:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o empréstimo: {erro}")

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def screenAddEmprestimo(frame):
    global entry_data_emprestimo, combobox_isbn_livro, combobox_colaborador  # Acessar as variáveis globais

    def buscar_colaboradores():
        try:
            diretorio_atual = os.path.dirname(__file__)
            diretorio_pai = os.path.dirname(diretorio_atual)
            diretorio_pai = os.path.dirname(diretorio_pai)

            conexao = sqlite3.connect(f"{diretorio_pai}/Packages/phpLiteAdmin/angueraBook.sqlite")
            cursor = conexao.cursor()

            cursor.execute("SELECT nome FROM Colaborador")
            colaboradores = cursor.fetchall()

            return [colaborador[0] for colaborador in colaboradores]

        except sqlite3.Error as erro:
            print(f"Ocorreu um erro ao buscar os colaboradores: {erro}")
            return []

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()
                
    def buscar_livros():
        try:
            diretorio_atual = os.path.dirname(__file__)
            diretorio_pai = os.path.dirname(diretorio_atual)
            diretorio_pai = os.path.dirname(diretorio_pai)

            conexao = sqlite3.connect(f"{diretorio_pai}/Packages/phpLiteAdmin/angueraBook.sqlite")
            cursor = conexao.cursor()

            cursor.execute("SELECT isbn FROM Livro")
            livros = cursor.fetchall()

            return [livro[0] for livro in livros]

        except sqlite3.Error as erro:
            print(f"Ocorreu um erro ao buscar os livros: {erro}")
            return []

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()


    frame_principal = ctk.CTkFrame(frame)
    frame_principal.pack(expand=True, fill="both")

    label_data_emprestimo = ctk.CTkLabel(frame_principal, text="Data de Empréstimo:")
    label_data_emprestimo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_data_emprestimo = ctk.CTkEntry(frame_principal)
    entry_data_emprestimo.insert(0, datetime.now().strftime("%Y-%m-%d"))  
    entry_data_emprestimo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    label_isbn_livro = ctk.CTkLabel(frame_principal, text="ISBN do Livro:")
    label_isbn_livro.grid(row=1, column=0, padx=10, pady=5, sticky="w")
   
    combobox_isbn_livro = ctk.CTkComboBox(frame_principal, values=buscar_livros(), state="readonly")
    combobox_isbn_livro.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    label_colaborador = ctk.CTkLabel(frame_principal, text="Colaborador:")
    label_colaborador.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    
    combobox_colaborador = ctk.CTkComboBox(frame_principal, values=buscar_colaboradores(), state="readonly")
    combobox_colaborador.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    button_adicionar = ctk.CTkButton(frame_principal, text="Adicionar Empréstimo", command=adicionar_emprestimo)
    button_adicionar.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    frame_principal.grid_columnconfigure(1, weight=1)

    return frame_principal

# screenAddEmprestimo(root)

# root.mainloop()
