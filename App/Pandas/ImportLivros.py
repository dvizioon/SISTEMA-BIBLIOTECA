import sqlite3
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import sys
sys.path.append(".")
from App.Modules.LerYaml import LerYaml

# Função para remover caracteres não numéricos e converter para inteiro
def extrair_numeros(valor):
    return int(''.join(filter(str.isdigit, valor)))

# Função para limpar e exibir uma mensagem na Text widget
def exibir_mensagem(mensagem, texto_saida):
    texto_saida.config(state=tk.NORMAL)  # Habilitar edição
    texto_saida.delete('1.0', tk.END)    # Limpar conteúdo
    texto_saida.insert(tk.END, mensagem) # Inserir mensagem
    texto_saida.config(state=tk.DISABLED) # Desabilitar edição

# Função para ler o arquivo Excel e importar os dados para o SQLite (Livro)
def importar_excel_livro_para_sqlite(screen, texto_saida):
    # Abrir a janela de seleção de arquivo
    filename = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])

    if filename:
        try:
            # Ler o arquivo Excel
            df = pd.read_excel(filename)

            # Conectar ao banco de dados SQLite
            buscaDB = LerYaml(".Yaml", "caminhoDB", index=0)
            conexao = sqlite3.connect(buscaDB)

            # Iterar sobre as linhas do DataFrame e inserir os dados na tabela
            total_registros = 0
            for index, row in df.iterrows():
                # Convertendo os tipos de dados conforme necessário
                isbn = str(row['isbn'])
                nome = str(row['nome'])
                autor = str(row['autor'])
                paginas = int(row['paginas'])

                # Inserindo os dados na tabela Livro
                comando_sql = "INSERT INTO Livro (isbn, nome, autor, paginas) VALUES (?, ?, ?, ?)"
                valores = (isbn, nome, autor, paginas)
                conexao.execute(comando_sql, valores)
                total_registros += 1

            # Confirmar a transação e fechar a conexão
            conexao.commit()
            conexao.close()

            # Exibir mensagem de sucesso
            exibir_mensagem(f"Dados importados com sucesso para a tabela Livro.\n"
                            f"Registros importados: {total_registros}", texto_saida)
        
        except Exception as e:
            # Exibir mensagem de erro
            exibir_mensagem(f"Erro ao importar dados: {e}", texto_saida)


# Criar a tela de importação de livros
def importLivros(screen):
    # Criar a tela de importação de livros
    # screen = tk.Frame(screen)
    # screen.pack()

    # Botão para selecionar o arquivo Excel (Livros)
    botao_selecionar_arquivo_livro = tk.Button(screen, text="Selecionar Arquivo Excel (Livros)", command=lambda: importar_excel_livro_para_sqlite(screen, texto_saida))
    botao_selecionar_arquivo_livro.pack(pady=10)

    # Texto de saída para exibir mensagens (Livros)
    texto_saida = tk.Text(screen, height=6, width=50, wrap=tk.WORD)
    texto_saida.pack()




# root.mainloop()
