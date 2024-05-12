import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
import subprocess
import psutil
sys.path.append(".")
from App.Modules.criarSecret import verificar_e_criar_users_json
from App.Screens.Painel import Painel
from App.Components.autenticador import autenticar
from App.Modules.LerYaml import LerYaml
from App.Modules.LerIni import LerINI
from App.Components.Processamento import prefix_process
from App.Sys.ProcessPid import pidProcess

import time
import webbrowser
import yaml
import configparser


pid = os.getpid()
arquivo_pid = "App\Sys\pid.txt"
pidProcess("cPID", pid, arquivo_pid)
# Lendo todos os PIDs do arquivo
pids = pidProcess("lPID", None, arquivo_pid)


root = ctk.CTk()
root.title("Login")

root.geometry(f"350x520+{500}+{50}")
root.resizable(False, False)

def encerrar_processos(pids):
    for pid in pids:
        try:
            print(f"Processo com PID {pid} encerrado.")
            psutil.Process(int(pid)).terminate()
            root.destroy()
        except psutil.NoSuchProcess:
            print(f"Processo com PID {pid} não encontrado.")
            
def confirmar_encerramento():
    encerrar_processos(pids)
    # Encerrar a janela
    root.destroy()
    root.quit()

phpCp = prefix_process("_pfx.json","_prf_")
def runPHP(_pre):
     url = LerYaml(".Yaml","url",index=_pre)
     return url
 

def entrarLink():
    if phpCp:
            comando_php = [phpCp, "-S",runPHP(0) , "-t", r".\App\PHP"]
            subprocess.Popen(comando_php, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(2)  # Aguarda um pouco para garantir que o servidor PHP seja iniciado
            webbrowser.open(runPHP(1))  # Abre a URL em um navegador da web
            print("Servidor PHP iniciado.")
    else:
            print("URL não encontrada no arquivo YAML.")
    encerrar_processos(pids)
    time.sleep(2)
    root.destroy()

def criar_msg(tipo, msg, position):
    entry_frame = ctk.CTkFrame(root, corner_radius=5, width=200, height=20,fg_color="transparent")
    entry_frame.grid(row=position, column=0, padx=10, pady=0, columnspan=2, sticky="ew")
    if tipo == "success":
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 20),
                                  corner_radius=5,
                                  fg_color=("#2dd55b", "white"),
                                  text_color=("white"), pady=(5))
    elif tipo == "error":
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 20),
                                  width=20, corner_radius=5,
                                  fg_color=("#cb1a27", "white"),
                                  text_color=("white"), pady=(5))
    elif tipo == "warning":
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 20),
                                  width=20, corner_radius=5,
                                  fg_color=("#ffca22", "white"),
                                  text_color=("white"), pady=(5))
    elif tipo == "validation":
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 20),
                                  width=20, corner_radius=5,
                                  fg_color=("#1a65eb", "white"),
                                  text_color=("white"), pady=(5))
    elif tipo == "Link":
        label_msg = ctk.CTkButton(entry_frame, text=msg, font=("Roboto", 20),
                          width=20, corner_radius=5,
                          fg_color=("#ffca22", "white"),
                          text_color=("blue"),command=entrarLink)


    label_msg.grid(row=2, column=1, padx=10, pady=20, columnspan=2, sticky="ew")
    entry_frame.grid_columnconfigure(1, weight=1)


def verificar_arquivo(caminho_arquivo):
            if os.path.exists(caminho_arquivo):
                    pass
            else:

                def criarUsuario():
                    
                    if phpCp:
                        comando_php = [phpCp, "-S",runPHP(0) , "-t", r".\App\PHP"]
                        subprocess.Popen(comando_php, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        time.sleep(2)  # Aguarda um pouco para garantir que o servidor PHP seja iniciado
                        webbrowser.open(runPHP(1))  # Abre a URL em um navegador da web
                        print("Servidor PHP iniciado.")
                    else:
                        print("URL não encontrada no arquivo YAML.")

                Button = ctk.CTkButton(root, text="Criar Usuário", width=20,height=50,font=("Roboto", 20),command=criarUsuario) 
                Button.grid(row=7, column=0, padx=10, pady=20, columnspan=2, sticky="ew")
  

              

caminho_arquivo = "./secret/users.json"
verificar_arquivo(caminho_arquivo)

def login():
    # Obter os valores dos campos de entrada
    username = usuario.get()
    password = senha.get()

    # Verificar se os campos estão vazios
    if not username or not password:
        criar_msg("error", "Campo Vazio!",  8)
        return
    else:
        def verificar_arquivo(caminho_arquivo):
            if os.path.exists(caminho_arquivo):
                criar_msg("validation", "Validando Dados",  8)
                if autenticar(username, password):
                    criar_msg("success", "Login bem-sucedido!",  8)
                    resultado_login = True  # Se o login for bem-sucedido
                    root.destroy()
                    root.quit()
                    Painel()
                    return True
                else:
                    criar_msg("error", "Usuário Não Encontrado!",  8)
                    resultado_login = False  # Se o login falhar
                    return False
            else:
                # verificar_e_criar_users_json()
                criar_msg("warning", "Criar Usuário", 8)

                if phpCp:
                    comando_php = [phpCp, "-S", runPHP(0), "-t", r".\App\PHP"]
                    subprocess.Popen(comando_php, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    time.sleep(2)  # Aguarda um pouco para garantir que o servidor PHP seja iniciado
                    webbrowser.open(runPHP(1))  # Abre a URL em um navegador da web
                    print("Servidor PHP iniciado.")
                else:
                    print("URL não encontrada no arquivo YAML.")

        caminho_arquivo = "./secret/users.json"
        verificar_arquivo(caminho_arquivo)

icon_label = ctk.CTkLabel(root,corner_radius=4,fg_color=("#1a65eb"),padx=10,pady=10, text_color=("#fff"),text="angueraBook", font=("Roboto", 40))
icon_label.grid(row=0, column=0, padx=(20, 20), pady=20)

def criar_input(placeholder_text, position_row, input_type="text"):
    entry_frame = ctk.CTkFrame(root, corner_radius=5, bg_color="#f0f0f0", width=200, height=40)
    entry_frame.grid(row=position_row, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

    if input_type == "password":
        input_entry = ctk.CTkEntry(entry_frame, placeholder_text=placeholder_text, font=("Roboto", 20), height=50,show="*")
    else:
        input_entry = ctk.CTkEntry(entry_frame, placeholder_text=placeholder_text, height=50, font=("Roboto", 20))
    input_entry.grid(row=0, column=1, padx=(10), pady=10, sticky="ew")
    entry_frame.grid_columnconfigure(1, weight=1)

    return input_entry
# Input Usuário
usuario = criar_input("Usuário", 1)

# Input Senha
senha = criar_input("Senha", 3, input_type="password")

criar_msg("Link", "Recuperar Senha", 6)

button_entrar = ctk.CTkButton(root, text="Entrar",
                             fg_color=("#ffb92c"),
                             height=50,text_color=("black"),
                             font=("Roboto", 20),hover_color=("#ffb04d"),
                              command=login)
button_entrar.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

root.grid_columnconfigure(0, weight=1)

# Defina a função de confirmação de encerramento ao fechar a janela
root.protocol("WM_DELETE_WINDOW", confirmar_encerramento)

def login_loop():
    root.mainloop()
    return root
#login_loop()
