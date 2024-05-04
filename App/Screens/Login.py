import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
import subprocess
sys.path.append(".")
from App.Modules.criarSecret import verificar_e_criar_users_json
from App.Components.autenticador import autenticar
import time
import webbrowser
import yaml


root = ctk.CTk()
root.title("Login")

tamanho = 440
root.geometry(f"350x{tamanho}+{500}+{50}")
root.resizable(False, False)


def criarMsg(tipo, msg, position, icon_path):
    entry_frame = ctk.CTkFrame(root, corner_radius=5, width=200, height=20)
    entry_frame.grid(row=position, column=0, padx=10, pady=0, columnspan=2, sticky="ew")
    
    # Carregar e redimensionar o ícone
    icon = Image.open(icon_path)
    icon = icon.resize((50, 50))
    icon = ImageTk.PhotoImage(icon)
    
    # Criar o rótulo para o ícone
    icon_label = ctk.CTkLabel(entry_frame, image=icon, text="")
    icon_label.grid(row=2, column=0, padx=10, pady=20, sticky="w")  # Coloque o ícone na segunda coluna

    
    if tipo == "success":
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 20), 
                                   corner_radius=5, 
                                  fg_color=("#2dd55b", "white"), 
                                  text_color=("white"), pady=(5))
        label_msg.grid(row=2, column=1, padx=10, pady=20, columnspan=2, sticky="ew")
    elif tipo == "error":
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 20), 
                                  width=20, corner_radius=5, 
                                  fg_color=("#cb1a27", "white"), 
                                  text_color=("white"), pady=(5))
        label_msg.grid(row=2, column=1, padx=10, pady=20, columnspan=2, sticky="ew")
    elif tipo == "warning":
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 20), 
                                  width=20, corner_radius=5, 
                                  fg_color=("#ffca22", "white"), 
                                  text_color=("white"), pady=(5))
        label_msg.grid(row=2, column=1, padx=10, pady=20, columnspan=2, sticky="ew")
    elif tipo == "validation":
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 20), 
                                  width=20, corner_radius=5, 
                                  fg_color=("#1a65eb", "white"), 
                                  text_color=("white"), pady=(5))
        label_msg.grid(row=2, column=1, padx=10, pady=20, columnspan=2, sticky="ew")

    entry_frame.grid_columnconfigure(1, weight=1)

def login():
    global tamanho
    tamanho = 550
    root.geometry(f"350x{tamanho}")
    
    # Obter os valores dos campos de entrada
    username = usuario.get()
    password = senha.get()
    

    # Verificar se os campos estão vazios
    if not username or not password:
        criarMsg("error", "Campo Vazio!", 6, "Assets\Icons\close.png")
        return
    else:
        def verificar_arquivo(caminho_arquivo):
            if os.path.exists(caminho_arquivo):
                criarMsg("validation", "Validando Dados", 6, r"Assets\Icons\validation.png")
                # print(f"O arquivo '{caminho_arquivo}' existe.")
                if autenticar(username , password):
                    criarMsg("success", "Login bem-sucedido!", 6, "Assets\Icons\check.png")
                else:
                    criarMsg("error", "Usuário Não Encontrado!", 6, "Assets\Icons\close.png")
            else:
                verificar_e_criar_users_json()
                criarMsg("warning", "Criar Usuário", 6, "Assets\Icons\crisis.png")
                
                def ler_url_do_yaml(caminho_arquivo):
                    with open(caminho_arquivo, 'r') as arquivo:
                        conteudo_yaml = yaml.safe_load(arquivo)
                    if 'url' in conteudo_yaml:
                        return conteudo_yaml['url']
                    else:
                        return None

                caminho_arquivo_yaml = ".Yaml"
                url = ler_url_do_yaml(caminho_arquivo_yaml)

                if url:
                    comando_php = ["php_5.exe", "-S", url[0], "-t", r".\App\PHP"]
                    processo_php = subprocess.Popen(comando_php, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    time.sleep(2)  # Aguarda um pouco para garantir que o servidor PHP seja iniciado
                    webbrowser.open(url[1])  # Abre a URL em um navegador da web
                    print("Servidor PHP iniciado.")
                else:
                    print("URL não encontrada no arquivo YAML.")
                    

        caminho_arquivo = "./secret/users.json"
        verificar_arquivo(caminho_arquivo)

Logo = Image.open(r"Assets\Logo.png")
Logo = Logo.resize((150, 150))
Logo = ImageTk.PhotoImage(Logo)
icon_label = ctk.CTkLabel(root, image=Logo, text="")
icon_label.grid(row=0, column=0, padx=(20, 20),pady=20)

# # Label do Usuario
# label_username = ctk.CTkLabel(root, text="Usuário:", font=("Roboto", 30), 
#                               width=20, corner_radius=5, 
#                               bg_color="#f0f0f0", fg_color=("#42adfe", "white"), 
#                               text_color=("white"),pady=(5))
# label_username.grid(row=0, column=0, padx=10, pady=20, columnspan=2, sticky="ew")

def criarInput(icon_path, placeholder_text, position_row, input_type="text"):
    icon = Image.open(icon_path)
    icon = icon.resize((50, 50))
    icon = ImageTk.PhotoImage(icon)

    # Criar o frame que conterá o ícone e o entry
    entry_frame = ctk.CTkFrame(root, corner_radius=5, bg_color="#f0f0f0", width=200, height=40)
    entry_frame.grid(row=position_row, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

    # Criar o label com o ícone
    icon_label = ctk.CTkLabel(entry_frame, image=icon, text="")
    icon_label.grid(row=0, column=0, padx=(20, 20), pady=10)

    # Criar o entry
    if input_type == "password":
        input_entry = ctk.CTkEntry(entry_frame, placeholder_text=placeholder_text, font=("Roboto", 20),height=50, show="*")
    else:
        input_entry = ctk.CTkEntry(entry_frame, placeholder_text=placeholder_text, height=50, font=("Roboto",  20))

    input_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

    # Configurar a coluna para expansão do entry
    entry_frame.grid_columnconfigure(1, weight=1)
    
    return input_entry

#Input Usuário
usuario = criarInput(
    r"Assets\Icons\usuario-conectado.png", 
    "Usuário",
    1, 
    input_type="text"
)


# Label do Password
# label_password = ctk.CTkLabel(root, text="Senha:", font=("Roboto", 30), 
#                               width=20, corner_radius=5, 
#                               bg_color="#f0f0f0", fg_color=("#42adfe", "white"), 
#                               text_color=("white"),pady=(5))
# label_password.grid(row=2, column=0, padx=10, pady=20, columnspan=2, sticky="ew")

#Input Senha
senha = criarInput(
    r"Assets\Icons\senha.png", 
    "Senha",
    3, 
    input_type="password"
)

EntrarImg = Image.open(r"Assets\Icons\entrar.png")
EntrarImg  = EntrarImg.resize((30, 30))
EntrarImg  = ImageTk.PhotoImage(EntrarImg)

buttonEntrar = ctk.CTkButton(root, text="Entrar",
                             fg_color=("#ffb92c"),
                             height=50,text_color=("black"),
                             font=("Roboto", 20),hover_color=("#ffb04d"),
                             image=EntrarImg,
                              command=login)
buttonEntrar.grid(row=5, column=0, padx=10, pady=10, columnspan=2,sticky="ew")

root.grid_columnconfigure(0, weight=1) 
root.mainloop()
