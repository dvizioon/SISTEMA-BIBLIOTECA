import sys
import configparser
import tkinter as tk
import tkinter.ttk as ttk
import configparser
sys.path.append(".")
from App.Modules.LerIni import LerINI
from App.Commands.Proccess.initProcess import process

import configparser

# process("Script/Config/angueraConfig.ps1","Script/Processamento_Form/pid.txt")

def openProcess():
    process("Script/Config/angueraConfig.ps1","Script/Processamento_Form/pid.txt")
# Função para formatar o INI
def formatarINI(dicionario, secao):
    formatted_ini = f"[{secao}]\n"
    for chave, valor in dicionario.items():
        formatted_ini += f"{chave} = {valor}\n"
    return formatted_ini

# Função para ler do INI
def LerINI(nome_arquivo_ini, secao):
    config = configparser.ConfigParser()
    config.read(nome_arquivo_ini)
    if secao in config:
        return dict(config[secao])
    else:
        return None

# Função para configurar o host
def configHost(frame):
    host_frame = tk.Frame(frame)
    label_host = tk.Label(host_frame, text="Configuração de Host", font=("Arial", 16))
    label_host.pack()
    text_area_host = tk.Text(host_frame, height=10, width=50)
    text_area_host.pack()

    _Host = LerINI("config.ini", "Panel")
    if _Host:
        formatted_ini = formatarINI(_Host, "Panel")
        text_area_host.insert(tk.END, formatted_ini)
    else:
        text_area_host.insert(tk.END, "A seção 'Panel' não foi encontrada no arquivo INI.")

    return host_frame

# Função para configurar o navegador
def configNavegador(frame):
    browser_frame = tk.Frame(frame)
    label_browser = tk.Label(browser_frame, text="Configuração do Navegador", font=("Arial", 16))
    label_browser.pack()
    text_area_browser = tk.Text(browser_frame, height=10, width=50)
    text_area_browser.pack()

    _browser = LerINI("App/Tools/Browser.ini", "Navegador")
    if _browser:
        formatted_ini = formatarINI(_browser, "Navegador")
        text_area_browser.insert(tk.END, formatted_ini)
    else:
        text_area_browser.insert(tk.END, "A seção 'Navegador' não foi encontrada no arquivo INI.")

    return browser_frame

# Função para configurar a janela principal
def configDB(frame):
    db_window = frame
    tab_control = ttk.Notebook(master=db_window)
    tab_control.pack(padx=20, pady=20)

    tab_host = tk.Frame(tab_control)
    tab_control.add(tab_host, text="Host")
    config_host_frame = configHost(tab_host)
    config_host_frame.pack()

    tab_browser = tk.Frame(tab_control)
    tab_control.add(tab_browser, text="Navegador")
    config_browser_frame = configNavegador(tab_browser)
    config_browser_frame.pack()
    btn_salvar_browser = tk.Button(db_window, text="Abrir Configuração",command=openProcess)
    btn_salvar_browser.pack(padx=30,pady=20)

    return db_window

# Configuração inicial da aplicação
# root = tk.Tk()
# Janela = configDB(root)
# root.title("Configurações")
# root.mainloop()