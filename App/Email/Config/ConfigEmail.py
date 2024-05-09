import tkinter as tk
from tkinter import ttk
import sys
sys.path.append(".")
from App.Email.SuperYaml import ModificarYaml

import tkinter as tk
from tkinter import ttk

def salvar_configuracoes():
    email = entry_email.get()
    senha = entry_senha.get()
    ssl_ativado = ssl_var.get()
    tipo_email = combo_tipo_email.get()
    smtp = entry_smtp.get()
    porta = entry_porta.get()
    
    ModificarYaml(caminho_yaml, secao_yaml ,0, ssl_ativado)
    ModificarYaml(caminho_yaml, secao_yaml ,1, email)
    ModificarYaml(caminho_yaml, secao_yaml ,2, senha)
    ModificarYaml(caminho_yaml, secao_yaml ,3, tipo_email)
    ModificarYaml(caminho_yaml, secao_yaml ,4, smtp)
    ModificarYaml(caminho_yaml, secao_yaml ,5, porta)
    
    print("Email:", email)
    print("Senha:", senha)
    print("SSL Ativado:", ssl_ativado)
    print("Tipo de Email:", tipo_email)
    print("SMTP:", smtp)
    print("Porta:", porta)
    print("Configurações salvas com sucesso!")

def configuracao_email(root, email, senha, template, smtp, porta,_vP=None,caminho_y=None,secao_y=None):
    global ssl_var, combo_tipo_email, entry_email, entry_senha, entry_smtp, entry_porta,caminho_yaml,secao_yaml

    caminho_yaml = caminho_y
    secao_yaml = secao_y

    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Label e input para configuração de email
    lbl_email = ttk.Label(frame, text="Email:")
    lbl_email.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_email = ttk.Entry(frame)
    entry_email.insert(0, email)
    entry_email.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Label e input para configuração de senha
    lbl_senha = ttk.Label(frame, text="Senha:")
    lbl_senha.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_senha = ttk.Entry(frame, show="*")
    entry_senha.insert(0, senha)
    entry_senha.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Label e input para configuração de SMTP
    lbl_smtp = ttk.Label(frame, text="SMTP:")
    lbl_smtp.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_smtp = ttk.Entry(frame)
    entry_smtp.insert(0, smtp)
    entry_smtp.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Label e input para configuração de porta
    lbl_porta = ttk.Label(frame, text="Porta:")
    lbl_porta.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_porta = ttk.Entry(frame)
    entry_porta.insert(0, porta)
    entry_porta.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Botões de rádio para ativar SSL
    ssl_var = tk.StringVar(value=_vP)
    radio_tls = ttk.Radiobutton(frame, text="TLS", variable=ssl_var, value="tls")
    radio_tls.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    radio_ssl = ttk.Radiobutton(frame, text="SSL", variable=ssl_var, value="ssl")
    radio_ssl.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # Combobox para selecionar entre padrão ou personalizado
    lbl_tipo_email = ttk.Label(frame, text="Tipo de Email:")
    lbl_tipo_email.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    # Definindo os valores para o combobox
    valores_combobox = ["Padrao", "Custom"]

    # Criando o combobox
    combo_tipo_email = ttk.Combobox(frame, values=valores_combobox)
    combo_tipo_email.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    # Definindo o valor padrão
    combo_tipo_email.set(template)

    # Botão para salvar as configurações
    btn_salvar = ttk.Button(frame, text="Salvar", command=salvar_configuracoes)
    btn_salvar.grid(row=6, column=0, columnspan=2, pady=10)

    # Adicionando padding ao frame
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

# root = tk.Tk()
# root.title("Configuração de Email")
# root.geometry("300x320")

# # Configurações padrão
# email = "daniel@gmail.com"
# senha = "hhkd mlxw ussx fdsd"
# template = "Padrao"
# ssl = True
# smtp = "smtp.gmail.com"
# porta = "587"
# caminho_yaml = "App/Email/conf.Yaml"  # Adicione o caminho do arquivo YAML aqui
# secao_yaml = "Aluno"  # Adicione a seção YAML aqui

# configuracao_email(root, email, senha, template, smtp, porta, "ssl",caminho_yaml,secao_yaml)
# root.mainloop()
