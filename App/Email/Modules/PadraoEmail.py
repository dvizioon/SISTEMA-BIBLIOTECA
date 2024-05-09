import tkinter as tk
from tkinter import ttk
import os
import sys
import re
from bs4 import BeautifulSoup

sys.path.append(".")

from App.Modules.LerContent import ler_arquivo

# Função para salvar a mensagem
def salvar_mensagem():
    global texto_mensagem, modo_selecionado, arquivo_nome
    
    mensagem = texto_mensagem.get("1.0", "end-1c") 
    modo = modo_selecionado.get()  
    
    if modo == "texto":
        mensagem_limpa = remover_caracteres_html_e_js(mensagem)
    else:
        mensagem_limpa = mensagem  
    
    htmlPadrao = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customizada</title>
</head>
<body>
{mensagem_limpa}
</body>
</html>
    """
        
    with open(arquivo_nome, "w", encoding="utf-8") as arquivo:
        arquivo.write(htmlPadrao)

    print("Mensagem salva com sucesso!")

def remover_caracteres_html_e_js(texto):
    texto_sem_html = re.sub(r'<[^>]*>', '', texto)
    texto_sem_js = re.sub(r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', '', texto_sem_html)
    
    return texto_sem_js

# Configuração da janela principal
# root = tk.Tk()
# root.title("Editor de Mensagens")
# root.geometry("400x300")

# Função para configurar a tela de mensagem padrão do aluno
def padraoEmail(root, a_nome):
    global modo_selecionado, arquivo_nome, texto_mensagem
    
    arquivo_nome = a_nome
    
    # Frame para a entrada de texto
    frame_texto = ttk.Frame(root)
    frame_texto.pack(padx=10, pady=10, fill="both", expand=True)

    # Textarea para inserir a mensagem
    texto_mensagem = tk.Text(frame_texto, height=10, width=50)
    if os.path.exists(a_nome):
        with open(a_nome, "r", encoding="utf-8") as arquivo:
            texto = arquivo.read()
            # Parseia o HTML
            soup = BeautifulSoup(texto, 'html.parser')
            # Extrai o texto dentro do corpo
            texto_body = soup.body.get_text(strip=True)
            # print(texto_body)
            texto_mensagem.insert("1.0", texto_body)
    else:
        print("O arquivo não existe.")
        texto_mensagem.insert("1.0", "")
    texto_mensagem.pack(padx=10, pady=10, fill="both", expand=True)

    # Frame para os radiobuttons
    frame_radios = ttk.Frame(root)
    frame_radios.pack(padx=10, pady=(0, 10), fill="x")

    # Variável para armazenar o modo selecionado
    modo_selecionado = tk.StringVar(value="texto")

    # Radiobuttons para selecionar o modo
    modo_texto = ttk.Radiobutton(frame_radios, text="Modo Texto", variable=modo_selecionado, value="texto")
    modo_texto.grid(row=0, column=0, padx=5)

    modo_codigo = ttk.Radiobutton(frame_radios, text="Modo Código", variable=modo_selecionado, value="codigo")
    modo_codigo.grid(row=0, column=1, padx=5)

    # Botão para salvar a mensagem
    botao_salvar = ttk.Button(root, text="Salvar", command=salvar_mensagem)
    botao_salvar.pack(pady=(0, 10))

# padraoEmail(root, "App/Email/archive/msgPadrao_a.txt")
# root.mainloop()
