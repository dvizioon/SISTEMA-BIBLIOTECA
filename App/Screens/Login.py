import customtkinter as ctk
from PIL import Image, ImageTk


# def login():
#     username = entry_username.get()
#     password = entry_password.get()

#     # Verificação do nome de usuário e senha (substitua com sua lógica de autenticação)
#     if username == "usuario" and password == "senha":
#         messagebox.showinfo("Login", "Login bem-sucedido!")
#         # Aqui você pode adicionar a lógica para abrir a próxima janela após o login bem-sucedido
#         return True
#     else:
#         messagebox.showerror("Login", "Nome de usuário ou senha incorretos")
#         return False

root = ctk.CTk()
root.title("Login")
root.geometry("350x500")


def criarMsg(tipo,msg,postion):
    
    entry_frame = ctk.CTkFrame(root, corner_radius=5, width=200, height=40)
    entry_frame.grid(row=postion, column=0, padx=10, pady=10, columnspan=2, sticky="ew")
    
    if tipo == "success":
        # Label da Msg
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 30), 
                                    width=20, corner_radius=5, 
                                    fg_color=("#2dd55b", "white"), 
                                    text_color=("white"),pady=(5))
        label_msg.grid(row=2, column=0, padx=10, pady=20, columnspan=2, sticky="ew")
    elif  tipo == "error" :
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 15), 
                                    width=20, corner_radius=5, 
                                     fg_color=("#cb1a27", "white"), 
                                    text_color=("white"),pady=(5))
        label_msg.grid(row=2, column=0, padx=10, pady=20, columnspan=2, sticky="ew")
    elif  tipo == "warning" :
        label_msg = ctk.CTkLabel(entry_frame, text=msg, font=("Roboto", 30), 
                                    width=20, corner_radius=5, 
                                    fg_color=("#ffca22", "white"), 
                                    text_color=("white"),pady=(5))
        label_msg.grid(row=2, column=0, padx=10, pady=20, columnspan=2, sticky="ew")

    entry_frame.grid_columnconfigure(1, weight=1)


criarMsg("error","Senha Incorreta",6)

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
                             image=EntrarImg)
buttonEntrar.grid(row=5, column=0, padx=10, pady=10, columnspan=2,sticky="ew")

root.grid_columnconfigure(0, weight=1) 
root.mainloop()
