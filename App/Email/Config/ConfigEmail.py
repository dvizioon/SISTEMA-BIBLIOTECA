import tkinter as tk
from tkinter import ttk
import sys
sys.path.append(".")
from App.Email.SuperYaml import ModificarYaml

def salvar_configuracoes():
    
    email = entry_email.get()
    senha = entry_senha.get()
    ssl_ativado = ssl_var.get()
    tipo_email = combo_tipo_email.get()
    
    ModificarYaml(caminho_yaml, secao_yaml ,0, ssl_ativado)
    ModificarYaml(caminho_yaml, secao_yaml ,1, email)
    ModificarYaml(caminho_yaml, secao_yaml ,2,senha)
    ModificarYaml(caminho_yaml, secao_yaml ,3,tipo_email)
    
    print("Email:", email)
    print("Senha:", senha)
    print("SSL Ativado:", ssl_ativado)
    print("Tipo de Email:", tipo_email)
    print("Configurações salvas com sucesso!")

def configuracao_email(root, email, senha, template, ssl,_yamlc,_yamls):
    global ssl_var, combo_tipo_email, entry_email, entry_senha , caminho_yaml , secao_yaml

    caminho_yaml = _yamlc
    secao_yaml = _yamls
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

    # Checkbox para ativar SSL
    ssl_var = tk.BooleanVar(value=ssl)
    chk_ssl = ttk.Checkbutton(frame, text="Ativar SSL", variable=ssl_var)
    chk_ssl.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    # Combobox para selecionar entre padrão ou personalizado
    lbl_tipo_email = ttk.Label(frame, text="Tipo de Email:")
    lbl_tipo_email.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    # Definindo os valores para o combobox
    valores_combobox = ["Padrao", "Custom"]

    # Criando o combobox
    combo_tipo_email = ttk.Combobox(frame, values=valores_combobox)
    combo_tipo_email.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Definindo o valor padrão
    combo_tipo_email.set(template)

    # Botão para salvar as configurações
    btn_salvar = ttk.Button(frame, text="Salvar", command=salvar_configuracoes)
    btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

    # Adicionando padding ao frame
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

# root = tk.Tk()
# root.title("Configuração de Email")
# root.geometry("300x220")

# Configurações padrão
# email = "daniel@gmail.com"
# senha = "hhkd mlxw ussx fdsd"
# template = "Padrao"
# ssl = True


# configuracao_email(root, email, senha, template, ssl,"App/Email/conf.Yaml","Aluno")

# root.mainloop()