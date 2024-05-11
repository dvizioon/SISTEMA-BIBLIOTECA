import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import customtkinter as ctk
import sys
import os
import datetime
sys.path.append(".")
from App.Modules.LerYaml import LerYaml
from App.Email.Chat.EnviarEmail import enviarEmail

data_hora_atual = datetime.datetime.now()
data_hora_formatada = data_hora_atual.strftime("%Y-%m-%d %H:%M:%S")

def conectar_banco_dados():
    # Carregar o caminho do banco de dados do arquivo YAML
    buscaDB = LerYaml(".Yaml", "caminhoDB", index=0)

    # Verificar se o arquivo do banco de dados existe
    if not os.path.exists(buscaDB):
        messagebox.showerror("Erro", "Banco de dados não encontrado.")
        return None, None

    # Conectar ao banco de dados SQLite
    conexao = sqlite3.connect(buscaDB)
    cursor = conexao.cursor()
    return conexao, cursor

def buscar_alunos(conexao, cursor):
    cursor.execute("SELECT * FROM Aluno")
    alunos = cursor.fetchall()
    return alunos

def pesquisar_aluno_por_ra(conexao, cursor, ra):
    cursor.execute("SELECT * FROM Aluno WHERE RA=?", (ra,))
    aluno = cursor.fetchone()
    return aluno

def pesquisar_aluno_por_nome(conexao, cursor, nome):
    cursor.execute("SELECT * FROM Aluno WHERE Nome LIKE ?", (f'%{nome}%',))
    alunos = cursor.fetchall()
    return alunos

def enviar_email(aluno):
    # aluno = {"nome": aluno[1], "Email": aluno[2], "data": data_hora_formatada}
    print(aluno)
    ssl = LerYaml("App/Email/conf.Yaml", "Aluno", index=0)  
    email = LerYaml("App/Email/conf.Yaml", "Aluno", index=1)  
    senha = LerYaml("App/Email/conf.Yaml", "Aluno", index=2)  
    tipo_email = LerYaml("App/Email/conf.Yaml", "Aluno", index=3)  
    smtp =  LerYaml("App/Email/conf.Yaml", "Aluno", index=4)  
    port =  LerYaml("App/Email/conf.Yaml", "Aluno", index=5)  
    
    if tipo_email == "Padrao":
        template = "App/Email/archive/msgPadrao_a.txt"
    else:
        template = "App/Email/archive/msgCustom_a.txt"
    
    destinatario = aluno[2]
    # print(destinatario)
    enviarEmail(
        "Aluno",
        template,
        destinatario,
        "AngueraBook Informa ✅🔎",
        None,
        email,
        senha,
        smtp,
        port,
        ssl,
        {"Nome": aluno[1], "Email": aluno[2], "data": data_hora_formatada,"Ra":aluno[0],"Telefone":aluno[3]}
    )
    # # Implemente aqui a lógica para enviar e-mail para o aluno
    # messagebox.showinfo("E-mail Enviado", f"E-mail enviado para o aluno {aluno[1]}")

def limpar_lista():
    for widget in frame_alunos.winfo_children():
        widget.destroy()

def exibir_alunos(lista_alunos):
    scrollable_frame = ctk.CTkScrollableFrame(frame_alunos, width=400, height=300)
    scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

    frame_interior = scrollable_frame
    
    for aluno in lista_alunos:
        # Frame do aluno (card)
        aluno_frame = ttk.Frame(frame_interior, width=scrollable_frame.winfo_width())
        aluno_frame.pack(fill="x", padx=5, pady=5)

        # Labels com as informações do aluno
        label_ra = ttk.Label(aluno_frame, text=f"RA: {aluno[0]}")
        label_ra.pack(anchor="w", padx=10, pady=(10, 0))

        label_nome = ttk.Label(aluno_frame, text=f"Nome: {aluno[1]}")
        label_nome.pack(anchor="w", padx=10, pady=(0, 5))

        label_email = ttk.Label(aluno_frame, text=f"E-mail: {aluno[2]}")
        label_email.pack(anchor="w", padx=10)

        label_telefone = ttk.Label(aluno_frame, text=f"Telefone: {aluno[3]}")
        label_telefone.pack(anchor="w", padx=10, pady=(0, 10))

        # Botão para enviar e-mail
        button_email = ctk.CTkButton(aluno_frame, text="Enviar E-mail", command=lambda a=aluno: enviar_email(a))
        button_email.pack(anchor="e", padx=10, pady=(0, 10))

def pesquisar_alunos():
    limpar_lista()
    valor_pesquisa = entry_pesquisa.get()
    tipo_pesquisa = combo_tipo_pesquisa.get()
    if tipo_pesquisa == "RA":
        aluno = pesquisar_aluno_por_ra(conexao, cursor, valor_pesquisa)
        if aluno:
            exibir_alunos([aluno])
        else:
            messagebox.showinfo("Aluno não encontrado", "Nenhum aluno encontrado com o RA fornecido.")
    elif tipo_pesquisa == "Nome":
        alunos = pesquisar_aluno_por_nome(conexao, cursor, valor_pesquisa)
        if alunos:
            exibir_alunos(alunos)
        else:
            messagebox.showinfo("Alunos não encontrados", "Nenhum aluno encontrado com o nome fornecido.")

# Criar a janela principal
# root = tk.Tk()
# root.title("Envio de E-mail para Alunos")
# root.geometry("600x400")

def CardAluno(root):
    global entry_pesquisa, combo_tipo_pesquisa, frame_alunos, conexao, cursor
    
    # Conectar ao banco de dados
    conexao, cursor = conectar_banco_dados()
    if conexao is None:
        root.destroy()
        return

    # Frame para entrada de pesquisa
    frame_pesquisa = ttk.Frame(root)
    frame_pesquisa.pack(fill="x", padx=10, pady=10)

    label_pesquisa = ttk.Label(frame_pesquisa, text="Pesquisar por:")
    label_pesquisa.grid(row=0, column=0, padx=5, pady=5)

    combo_tipo_pesquisa = ttk.Combobox(frame_pesquisa, values=["RA", "Nome"])
    combo_tipo_pesquisa.grid(row=0, column=1, padx=5, pady=5)
    combo_tipo_pesquisa.current(0)

    entry_pesquisa = ttk.Entry(frame_pesquisa)
    entry_pesquisa.grid(row=0, column=2, padx=5, pady=5)

    button_pesquisar = ttk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar_alunos)
    button_pesquisar.grid(row=0, column=3, padx=5, pady=5)

    # Frame para exibir alunos
    frame_alunos = ttk.Frame(root)
    frame_alunos.pack(fill="both", expand=True, padx=10, pady=10)

    # Exibir todos os alunos inicialmente
    exibir_alunos(buscar_alunos(conexao, cursor))

# CardAluno(root)

# root.mainloop()
