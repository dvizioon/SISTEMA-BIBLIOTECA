import tkinter as tk
from tkinter import ttk
import webview
import sys
sys.path.append(".")
from App.Email.Modules.PadraoEmail import padraoEmail
from App.Email.Modules.CustomEmail import customEmail
from App.Email.Config.ConfigEmail import configuracao_email
from App.Email.SuperYaml import LerYaml

def mensagem_padrao(aba_mensagem_padrao):
    print("Mostrando mensagem padrão")
    for widget in aba_mensagem_padrao.winfo_children():
        widget.destroy()

    padraoEmail(aba_mensagem_padrao, "App/Email/archive/msgPadrao_c.txt")

def mensagem_custom(aba_mensagem_personalizada):
    print("Mostrando mensagem customizada")
    for widget in aba_mensagem_personalizada.winfo_children():
        widget.destroy()

    customEmail(aba_mensagem_personalizada, "App/Email/archive/msgCustom_c.txt")
    
def configEmail(aba_mensagem_personalizada):
    print("Mostrando mensagem customizada")
    ssl = LerYaml("App/Email/conf.Yaml", "Colaborador", index=0)  
    email = LerYaml("App/Email/conf.Yaml", "Colaborador", index=1)  
    senha = LerYaml("App/Email/conf.Yaml", "Colaborador", index=2)  
    tipo_email = LerYaml("App/Email/conf.Yaml", "Colaborador", index=3)  
    # print(url2)

    for widget in aba_mensagem_personalizada.winfo_children():
        widget.destroy()
    

    configuracao_email(
        aba_mensagem_personalizada,
        email,
        senha,
        tipo_email,
        ssl ,
        "App/Email/conf.Yaml",
        "Colaborador"           
    )


def on_tab_change(event, notebook):
    current_tab = notebook.tab(notebook.select(), "text")
    print("Aba selecionada:", current_tab)  # Mensagem de depuração
    if current_tab == "Email Padrão":
        mensagem_padrao(notebook.nametowidget(notebook.select()))
    elif current_tab == "Email Personalizado":
        mensagem_custom(notebook.nametowidget(notebook.select()))
    elif current_tab == "Configuração Colaborador":
        configEmail(notebook.nametowidget(notebook.select()))

def configColaborador(root):
    notebook = ttk.Notebook(root)

    aba_mensagem_padrao = ttk.Frame(notebook)
    notebook.add(aba_mensagem_padrao, text='Email Padrão')

    aba_mensagem_personalizada = ttk.Frame(notebook)
    notebook.add(aba_mensagem_personalizada, text='Email Personalizado')

    aba_config_aluno = ttk.Frame(notebook)
    notebook.add(aba_config_aluno, text='Configuração Colaborador')

    notebook.pack(padx=10, pady=10, expand=True, fill="both")

    notebook.bind("<<NotebookTabChanged>>", lambda event: on_tab_change(event, notebook))

# root = tk.Tk()
# root.title("Gerenciador de Mensagens")
# root.geometry("400x400")

# configColaborador(root)

# root.mainloop()
