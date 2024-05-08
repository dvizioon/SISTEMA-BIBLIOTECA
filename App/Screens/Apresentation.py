
import customtkinter as ctk
import os
import sqlite3
import sys
sys.path.append(".")
from App.Screens.Login import login_loop
from App.Modules.LerYaml import LerYaml

caminhoDB = LerYaml(".Yaml","caminhoDB",index=1)
app = ctk.CTk()
app.title("AngueraBook - Sistema de Biblioteca")

# print(caminhoDB)
def criarBanco(caminho, nomeDB):
    db_directory = f"./{caminho}"
    db_filename = nomeDB
    db_path = os.path.join(db_directory, db_filename)

    # Verifica se o diretório existe, se não, cria-o
    if not os.path.exists(db_directory):
        print(f"Ditorio {db_path} ")

    # Verifica se o banco de dados já existe
    if os.path.exists(db_path):
        print(f"O banco de dados '{nomeDB}' já existe.")
        return

    # Comandos SQL para criar tabelas
    sql_commands = [
        """
        CREATE TABLE IF NOT EXISTS Aluno (
            ra INTEGER PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            telefone VARCHAR(20)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Livro (
            isbn VARCHAR(13) PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            autor VARCHAR(100),
            paginas INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Colaborador (
            cpf VARCHAR(11) PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            cargo VARCHAR(100)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Emprestimo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataEmprestimo DATE NOT NULL,
            dataDevolucao DATE,
            livroIsbn VARCHAR(13),
            colaboradorCpf VARCHAR(11),
            FOREIGN KEY (livroIsbn) REFERENCES Livro(isbn),
            FOREIGN KEY (colaboradorCpf) REFERENCES Colaborador(cpf)
        )
        """
    ]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for command in sql_commands:
        cursor.execute(command)
    conn.commit()
    conn.close()

    print("Banco de dados e tabelas criados com sucesso!")
    
    app.destroy()
    login_loop()



def apresentation():
    def exibir_texto():
        tab_name = tabview.get()
        texto = textos.get(tab_name, "Texto não encontrado para esta aba.")
        for widget in tabview.tab(tab_name).winfo_children():
            widget.destroy()
        texto_label = ctk.CTkLabel(tabview.tab(tab_name), text=texto, font=("Arial", 16), wraplength=tabview.winfo_width() - 40)
        texto_label.pack(pady=20)

    def iniciar():
        criarBanco(caminhoDB,"angueraBook.sqlite")
        exibir_texto()
        
   
    tabview = ctk.CTkTabview(master=app)
    tabview.pack(padx=20, pady=20)
    abas = ["Início", "Sobre"]
    for aba in abas:
        tabview.add(aba)
    textos = {
        "Início": "Bem-vindo ao AngueraBook! , \nPercebir que você é novo Por aqui!!!,\nVamos inicar 📦",
        "Sobre": "AngueraBook é um sistema de biblioteca para gerenciamento de livros, alunos e empréstimos.",
    }
    exibir_texto()
    tabview._command = exibir_texto
    btn_iniciar = ctk.CTkButton(master=app, text="Iniciar", command=iniciar,
                                fg_color=("#ffb92c"),
                                height=50,text_color=("black"),
                                font=("Roboto", 20),hover_color=("#ffb04d"))
    btn_iniciar.pack(pady=10)
    app.mainloop()
    
# apresentation()
