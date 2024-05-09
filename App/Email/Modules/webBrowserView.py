import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import webview
import sys
sys.path.append(".")
from App.Email.SuperYaml import LerYaml


def visualizar_email():
    if methodoTo == "Aluno":
        indePath = LerYaml("App/Email/conf.Yaml", "Aluno", index=3)  
        if indePath == "Custom":
                template = "App/Email/archive/msgCustom_a.txt" 
        else:
                template = "App/Email/archive/msgPadrao_a.txt"
              
                # Ler o conteúdo do arquivo
        with open(template, "r") as file:
            html_content = file.read()

            # Exibir o conteúdo HTML em uma janela do navegador
        webview.create_window("Visualização de Email", html=html_content)
        webview.start()
        
    elif methodoTo == "Colaborador":
        indePath = LerYaml("App/Email/conf.Yaml", "Colaborador", index=3)  
        if indePath == "Custom":
                template = "App/Email/archive/msgCustom_c.txt" 
        else:
                template = "App/Email/archive/msgPadrao_c.txt"
              
                # Ler o conteúdo do arquivo
        with open(template, "r") as file:
            html_content = file.read()

            # Exibir o conteúdo HTML em uma janela do navegador
        webview.create_window("Visualização de Email", html=html_content)
        webview.start()


def exibir_ajuda(texto_ajuda,msg):
    texto_ajuda.delete('1.0', tk.END)  
    texto_ajuda.insert(tk.END, msg)


# root = tk.Tk()
# root.title("Visualizador de E-mail")

def vizualizarTemplate(janela,tipo,msg):
    global methodoTo
    methodoTo = tipo
    _mgs = msg
    
    # Criar um botão para abrir a visualização do e-mail
    botao_visualizar = ttk.Button(janela, text="Abrir Visualização", command=visualizar_email)
    botao_visualizar.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    # Criar uma área de texto para exibir o texto de ajuda
    texto_ajuda = scrolledtext.ScrolledText(janela, width=60, height=5)
    texto_ajuda.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

    # Exibir o texto de ajuda padrão
    exibir_ajuda(texto_ajuda,_mgs)



# vizualizarTemplate(root,"Aluno","Insira aqui o texto de ajuda ou instruções para visualizar o e-mail.")

# root.mainloop()
