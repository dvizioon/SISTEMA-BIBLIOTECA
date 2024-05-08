import sqlite3
import os
import sys
import customtkinter as ctk
from tkinter import messagebox
sys.path.append(".")
# Criar uma nova janela
janela = ctk.CTk()
janela.title("Gráfico de Dados")
from App.Modules.LerYaml import LerYaml
buscaDB = LerYaml(".Yaml","caminhoDB",index=0)


def buscar_dados():
    try:
        diretorio_atual = os.path.dirname(__file__)
        diretorio_pai = os.path.dirname(diretorio_atual)
        diretorio_pai = os.path.dirname(diretorio_pai)
        print(diretorio_pai)
        # Conexão com o banco de dados
        conn = sqlite3.connect(f"{buscaDB}")
        cursor = conn.cursor()
        
        # Buscar o número de alunos
        cursor.execute("SELECT COUNT(*) FROM Aluno")
        numero_alunos = cursor.fetchone()[0] or 0  # Definir como zero se for None

        # Buscar o número de livros
        cursor.execute("SELECT COUNT(*) FROM Livro")
        numero_livros = cursor.fetchone()[0] or 0  # Definir como zero se for None

        # Buscar o número de colaboradores
        cursor.execute("SELECT COUNT(*) FROM Colaborador")
        numero_colaboradores = cursor.fetchone()[0] or 0  # Definir como zero se for None

        # Fechar a conexão com o banco de dados
        conn.close()

        return numero_alunos, numero_livros, numero_colaboradores

    except sqlite3.Error as erro:
        # messagebox.showerror("Erro", f"Ocorreu um erro ao buscar os dados: {erro}")
        return 0, 0, 0  # Retorna zeros em caso de erro

def criar_card(frame, texto, cor, imagem_path, row, column):
    # Criar o cartão
    card = ctk.CTkFrame(master=frame, fg_color=cor, border_color="black")
    card.grid(row=row, column=column, padx=10, pady=10)

    # Adicionar imagem ao cartão
    if imagem_path:
        label_imagem = ctk.CTkLabel(card, text="imagem")
        label_imagem.pack(padx=5, pady=5)

    # Adicionar texto ao cartão
    label_texto = ctk.CTkLabel(card, text=texto, font=("Arial", 20))
    label_texto.pack(fill="both", expand=True, padx=20, pady=20)

    # Adicionar botão "Detalhes" ao cartão
    button_detalhes = ctk.CTkButton(card, text="Detalhes")
    button_detalhes.pack(padx=20, pady=10)

def exibir_cards(screen):
    numero_alunos, numero_livros, numero_colaboradores = buscar_dados()

    diretorio_atual = os.path.dirname(__file__)
    diretorio_pai = os.path.dirname(diretorio_atual)
    diretorio_pai = os.path.dirname(diretorio_pai)
    print(diretorio_pai)

    # Criar uma frame principal
    frame_principal = ctk.CTkFrame(screen)
    frame_principal.pack()

    # Criar e exibir os cartões
    card1 = criar_card(frame_principal, f"Alunos\n{numero_alunos}", ("#ffc107", "white"), None, 0, 0)
    card2 = criar_card(frame_principal, f"Livros\n{numero_livros}", ("#007bff", "white"), None, 0, 1)
    card3 = criar_card(frame_principal, f"Colaboradores\n{numero_colaboradores}", ("#28a745", "white"), None, 0, 2)

    # Exibir a janela
#     janela.mainloop()

# # Exibir os cartões
# exibir_cards(janela)
