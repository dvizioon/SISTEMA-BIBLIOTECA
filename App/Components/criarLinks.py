import customtkinter as ctk
import sys

sys.path.append(".")

class LinkButton(ctk.CTkButton):
    def __init__(self, parent, text, command=None, **kwargs):
        super().__init__(parent, text=text, fg_color="transparent", text_color="blue", hover_color="lightblue", command=command, **kwargs)
        self.configure(compound="left")

        # Adicionando uma seta Unicode
        self.arrow = "\u2192"  # Seta apontando para a direita
        self.configure(text=f"{self.arrow} {text}")

# Exemplo de uso:
# def adicionar_aluno():
#     print("Abrindo tela de adicionar aluno...")

# def visualizar_alunos():
#     print("Abrindo tela de visualizar alunos...")

def criar_links(frame, links):
    for link in links:
        text, command = link
        link_button = LinkButton(frame, text=text, command=command)
        link_button.pack(pady=5)

def initLinkScreen(screen, links):
    frame_principal = ctk.CTkFrame(screen)
    frame_principal.pack(expand=True, fill="both")
    
    criar_links(frame_principal, links)

# # Exemplo de uso:
# root = ctk.CTk()
# root.title("Exemplo de Links com Ícones")

# # Defina os links desejados como uma lista de tuplas
# links = [
#     ("Adicionar Aluno", adicionar_aluno),
#     ("Visualizar Alunos", visualizar_alunos)
# ]

# initLinkScreen(root, links)

# root.mainloop()
