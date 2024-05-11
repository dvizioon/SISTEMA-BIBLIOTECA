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

def buscar_colaboradores(conexao, cursor):
    cursor.execute("SELECT * FROM Colaborador")
    colaboradores = cursor.fetchall()
    return colaboradores

def pesquisar_colaborador_por_cpf(conexao, cursor, cpf):
    cursor.execute("SELECT * FROM Colaborador WHERE cpf=?", (cpf,))
    colaborador = cursor.fetchone()
    return colaborador

def pesquisar_colaborador_por_nome(conexao, cursor, nome):
    cursor.execute("SELECT * FROM Colaborador WHERE nome LIKE ?", (f'%{nome}%',))
    colaboradores = cursor.fetchall()
    return colaboradores

def enviar_email_colaborador(colaborador):
    print(colaborador)
    ssl = LerYaml("App/Email/conf.Yaml", "Colaborador", index=0)  
    email = LerYaml("App/Email/conf.Yaml", "Colaborador", index=1)  
    senha = LerYaml("App/Email/conf.Yaml", "Colaborador", index=2)  
    tipo_email = LerYaml("App/Email/conf.Yaml", "Colaborador", index=3)  
    smtp = LerYaml("App/Email/conf.Yaml", "Colaborador", index=4)  
    port = LerYaml("App/Email/conf.Yaml", "Colaborador", index=5)  
    
    if tipo_email == "Padrao":
        template = "App/Email/archive/msgPadrao_c.txt"
    else:
        template = "App/Email/archive/msgCustom_c.txt"
    
    destinatario = colaborador[2]  # Supondo que o e-mail do colaborador está na segunda coluna da tabela
    
    enviarEmail(
        "Colaborador",
        template,
        destinatario,
        "AngueraBook Informa ✅🔎",
        None,
        email,
        senha,
        smtp,
        port,
        ssl,
        {"Nome": colaborador[1], "Email": colaborador[2], "data": data_hora_formatada, "CPF": colaborador[0], "Cargo": colaborador[3]}
    )

def limpar_lista():
    for widget in frame_colaboradores.winfo_children():
        widget.destroy()

def exibir_colaboradores(lista_colaboradores):
    scrollable_frame = ctk.CTkScrollableFrame(frame_colaboradores, width=400, height=300)
    scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

    frame_interior = scrollable_frame
    
    for colaborador in lista_colaboradores:
        # Frame do colaborador (card)
        colaborador_frame = ttk.Frame(frame_interior, width=scrollable_frame.winfo_width())
        colaborador_frame.pack(fill="x", padx=5, pady=5)

        # Labels com as informações do colaborador
        label_cpf = ttk.Label(colaborador_frame, text=f"CPF: {colaborador[0]}")
        label_cpf.pack(anchor="w", padx=10, pady=(10, 0))

        label_nome = ttk.Label(colaborador_frame, text=f"Nome: {colaborador[1]}")
        label_nome.pack(anchor="w", padx=10, pady=(0, 5))

        label_email = ttk.Label(colaborador_frame, text=f"E-mail: {colaborador[2]}")
        label_email.pack(anchor="w", padx=10)

        label_cargo = ttk.Label(colaborador_frame, text=f"Cargo: {colaborador[3]}")
        label_cargo.pack(anchor="w", padx=10, pady=(0, 10))

        # Botão para enviar e-mail
        button_email = ctk.CTkButton(colaborador_frame, text="Enviar E-mail", command=lambda c=colaborador: enviar_email_colaborador(c))
        button_email.pack(anchor="e", padx=10, pady=(0, 10))

def pesquisar_colaboradores():
    limpar_lista()
    valor_pesquisa = entry_pesquisa.get()
    tipo_pesquisa = combo_tipo_pesquisa.get()
    if tipo_pesquisa == "CPF":
        colaborador = pesquisar_colaborador_por_cpf(conexao, cursor, valor_pesquisa)
        if colaborador:
            exibir_colaboradores([colaborador])
        else:
            messagebox.showinfo("Colaborador não encontrado", "Nenhum colaborador encontrado com o CPF fornecido.")
    elif tipo_pesquisa == "Nome":
        colaboradores = pesquisar_colaborador_por_nome(conexao, cursor, valor_pesquisa)
        if colaboradores:
            exibir_colaboradores(colaboradores)
        else:
            messagebox.showinfo("Colaboradores não encontrados", "Nenhum colaborador encontrado com o nome fornecido.")

# Criar a janela principal
# root = tk.Tk()
# root.title("Envio de E-mail para Colaboradores")
# root.geometry("600x400")

def CardColaborador(root):
    global entry_pesquisa, combo_tipo_pesquisa, frame_colaboradores, conexao, cursor
    
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

    combo_tipo_pesquisa = ttk.Combobox(frame_pesquisa, values=["CPF", "Nome"])
    combo_tipo_pesquisa.grid(row=0, column=1, padx=5, pady=5)
    combo_tipo_pesquisa.current(0)

    entry_pesquisa = ttk.Entry(frame_pesquisa)
    entry_pesquisa.grid(row=0, column=2, padx=5, pady=5)

    button_pesquisar = ttk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar_colaboradores)
    button_pesquisar.grid(row=0, column=3, padx=5, pady=5)

    # Frame para exibir colaboradores
    frame_colaboradores = ttk.Frame(root)
    frame_colaboradores.pack(fill="both", expand=True, padx=10, pady=10)

    # Exibir todos os colaboradores inicialmente
    exibir_colaboradores(buscar_colaboradores(conexao, cursor))

# CardColaborador(root)

# root.mainloop()
