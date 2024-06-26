import customtkinter as ctk
import sys
import tkinter as tk
from PIL import Image
from PIL import ImageTk

sys.path.append(".")
from App.Screens.AddAluno import screenAddAluno
from App.Screens.AddLivro import screenAddLivro
from App.Screens.AddColaborador import screenAddColaborador
from App.Screens.AddEmprestimo import screenAddEmprestimo

from App.Screens.ViewAluno import screenViewAluno
from App.Screens.ViewLivro import screenViewLivro
from App.Screens.ViewColaborador import screenViewColaborador
from App.Screens.ViewEmprestimo import screenViewEmprestimo


from App.Components.criarLinks import initLinkScreen
from App.Components.Graficos import exibir_cards

root = ctk.CTk()
root.title("Painel angueraBook")
root.geometry("840x450")
# # root.iconbitmap("Assets\Logo.ico")

# root.iconpath = ImageTk.PhotoImage(file="Assets\Logo.png")
# root.wm_iconbitmap()
# root.iconphoto(False, root.iconpath)

def Painel():
    
    def criarNavLinks(frame, nome, position):
        # Criando botões de navegação
        link = ctk.CTkButton(frame, corner_radius=0, height=40, border_spacing=10, text=nome, font=("Roboto", 20),
                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                             anchor="w", command=lambda: selecionarScreen(nome))
        link.grid(row=position, column=0, sticky="ew")
        
    # Configurando o layout da grade para 1 linha e 2 colunas
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Criando o frame de navegação
    navigation_frame = ctk.CTkFrame(root, corner_radius=0)
    navigation_frame.grid(row=0, column=0, sticky="nsew")
    navigation_frame.grid_rowconfigure(10, weight=1) # Configuração da coluna quantidade de links

    # Criando o rótulo do frame de navegação
    navigation_frame_label = ctk.CTkLabel(navigation_frame, text="angueraBook", font=ctk.CTkFont(size=20, weight="bold"))
    navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

    # Criando o frame_home
    global frame_home
    frame_home = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")
    frame_home.grid(row=0, column=1, sticky="nsew")
    
    link_Home = criarNavLinks(navigation_frame, "Home", 1)
    link_Aluno = criarNavLinks(navigation_frame, "Aluno", 2)
    link_Livros = criarNavLinks(navigation_frame, "Livros", 3)
    link_Colaborador = criarNavLinks(navigation_frame, "Colaborador", 4)
    link_Emprestimo = criarNavLinks(navigation_frame, "Emprestimo", 5)

    # Chama a função para criar e exibir a tela "Home" quando o Painel é carregado
    criar_tela_home_frame()

    root.mainloop()

def criar_tela_home_frame():
       # Limpar o frame anterior antes de adicionar novos widgets
    for widget in frame_home.winfo_children():
        widget.destroy()

     
    frame_atual = ctk.CTkFrame(frame_home, height=30)  # Defina a altura desejada aqui
    frame_atual.pack(padx=20, pady=20)
    
    # frame_render = ctk.CTkFrame(frame_home)  # Defina a altura desejada aqui
    # frame_render.pack(fill="both", expand=True, padx=20, pady=20)
    
    exibir_cards(frame_atual)
    
def criar_tela_Aluno_frame():
    # Limpar o frame anterior antes de adicionar novos widgets
    for widget in frame_home.winfo_children():
        widget.destroy()

     
    frame_atual = ctk.CTkFrame(frame_home, height=30)  # Defina a altura desejada aqui
    frame_atual.pack(padx=20, pady=20)
    
    frame_render = ctk.CTkFrame(frame_home)  # Defina a altura desejada aqui
    frame_render.pack(fill="both", expand=True, padx=20, pady=20)
    
    def voltar():
        for widget in frame_render.winfo_children():
            widget.destroy()
        initLinkScreen(frame_render, links)
        
    def adicionar_aluno():
        for widget in frame_render.winfo_children():
            widget.destroy()
        screenAddAluno(frame_render)
        print("Adicionando Aluno...")

    def visualizar_alunos():
        for widget in frame_render.winfo_children():
            widget.destroy()
        screenViewAluno(frame_render)
        print("Vizualizando Alunos...")

    botao_voltar = ctk.CTkButton(frame_atual, text="Voltar",command=voltar)
    botao_voltar.pack()
    
    links = [
        ("Adicionar Aluno", "Assets/Icons/arrow.png", adicionar_aluno),
        ("Visualizar Alunos", "Assets/Icons/arrow.png", visualizar_alunos)
    ]
    initLinkScreen(frame_render, links)


def criar_tela_Livros_frame():
      # Limpar o frame anterior antes de adicionar novos widgets
    for widget in frame_home.winfo_children():
        widget.destroy()

     
    frame_atual = ctk.CTkFrame(frame_home, height=30)  # Defina a altura desejada aqui
    frame_atual.pack(padx=20, pady=20)
    
    frame_render = ctk.CTkFrame(frame_home)  # Defina a altura desejada aqui
    frame_render.pack(fill="both", expand=True, padx=20, pady=20)
    
    def voltar():
        for widget in frame_render.winfo_children():
            widget.destroy()
        initLinkScreen(frame_render, links)
        
    def adicionar_livro():
        for widget in frame_render.winfo_children():
            widget.destroy()
        screenAddLivro(frame_render)
        print("Adicionando Livro...")

    def visualizar_livros():
        for widget in frame_render.winfo_children():
            widget.destroy()
        screenViewLivro(frame_render)
        print("Vizualizando Alunos...")

    botao_voltar = ctk.CTkButton(frame_atual, text="Voltar",command=voltar)
    botao_voltar.pack()
    
    links = [
        ("Adicionar Livro", "Assets/Icons/arrow.png", adicionar_livro),
        ("Visualizar Livros", "Assets/Icons/arrow.png", visualizar_livros)
    ]
    initLinkScreen(frame_render, links)


    
def criar_tela_Colaborador_frame():
    # Limpar o frame anterior antes de adicionar novos widgets
    for widget in frame_home.winfo_children():
        widget.destroy()

     
    frame_atual = ctk.CTkFrame(frame_home, height=30)  # Defina a altura desejada aqui
    frame_atual.pack(padx=20, pady=20)
    
    frame_render = ctk.CTkFrame(frame_home)  # Defina a altura desejada aqui
    frame_render.pack(fill="both", expand=True, padx=20, pady=20)
    
    def voltar():
        for widget in frame_render.winfo_children():
            widget.destroy()
        initLinkScreen(frame_render, links)
        
    def adicionar_colaborador():
        for widget in frame_render.winfo_children():
            widget.destroy()
        screenAddColaborador(frame_render)
        print("Adicionando Colaborador...")

    def visualizar_colaborador():
        for widget in frame_render.winfo_children():
            widget.destroy()
        screenViewColaborador(frame_render)
        print("Vizualizando Colaborador...")

    botao_voltar = ctk.CTkButton(frame_atual, text="Voltar",command=voltar)
    botao_voltar.pack()
    
    links = [
        ("Adicionar  Colaborador", "Assets/Icons/arrow.png", adicionar_colaborador),
        ("Visualizar Colaborador", "Assets/Icons/arrow.png", visualizar_colaborador)
    ]
    initLinkScreen(frame_render, links)


def criar_tela_Emprestimos_frame():
    # Limpar o frame anterior antes de adicionar novos widgets
    for widget in frame_home.winfo_children():
        widget.destroy()

     
    frame_atual = ctk.CTkFrame(frame_home, height=30)  # Defina a altura desejada aqui
    frame_atual.pack(padx=20, pady=20)
    
    frame_render = ctk.CTkFrame(frame_home)  # Defina a altura desejada aqui
    frame_render.pack(fill="both", expand=True, padx=20, pady=20)
    
    def voltar():
        for widget in frame_render.winfo_children():
            widget.destroy()
        initLinkScreen(frame_render, links)
        
    def adicionar_Emprestimo():
        for widget in frame_render.winfo_children():
            widget.destroy()
        screenAddEmprestimo(frame_render)
        print("Adicionando Emprestimo...")

    def visualizar_emprestimo():
        for widget in frame_render.winfo_children():
            widget.destroy()
        screenViewEmprestimo(frame_render)
        print("Vizualizando Emprestimo...")

    botao_voltar = ctk.CTkButton(frame_atual, text="Voltar",command=voltar)
    botao_voltar.pack()
    
    links = [
        ("Adicionar Emprestimo", "Assets/Icons/arrow.png", adicionar_Emprestimo),
        ("Visualizar Emprestimo", "Assets/Icons/arrow.png", visualizar_emprestimo)
    ]
    initLinkScreen(frame_render, links)


def selecionarScreen(nome):
    if nome == "Home":
        criar_tela_home_frame()
    elif nome == "Aluno":
        criar_tela_Aluno_frame()
    elif nome == "Livros":
        criar_tela_Livros_frame()
    elif nome == "Colaborador":
        criar_tela_Colaborador_frame()
    elif nome == "Emprestimo":
        criar_tela_Emprestimos_frame()

# Verifica se este script é o principal
# if __name__ == "__main__":
#     Painel()
