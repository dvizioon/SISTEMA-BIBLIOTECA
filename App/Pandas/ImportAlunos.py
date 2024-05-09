import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog
import sys
sys.path.append(".")
from App.Modules.LerYaml import LerYaml

buscaDB = LerYaml(".Yaml", "caminhoDB", index=0)

def extrair_numeros(valor):
    return int(''.join(filter(str.isdigit, valor)))

def exibir_mensagem(mensagem, texto_saida):
    texto_saida.config(state=tk.NORMAL)  # Habilitar edição
    texto_saida.delete('1.0', tk.END)    # Limpar conteúdo
    texto_saida.insert(tk.END, mensagem) # Inserir mensagem
    texto_saida.config(state=tk.DISABLED) # Desabilitar edição

def importar_excel_para_sqlite(screen, texto_saida):
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
                ra = extrair_numeros(row['ra'])
                nome = str(row['nome'])
                email = str(row['e-mail'])
                telefone = str(row['telefone'])

                # Inserindo os dados na tabela Aluno
                comando_sql = "INSERT INTO Aluno (ra, nome, email, telefone) VALUES (?, ?, ?, ?)"
                valores = (ra, nome, email, telefone)
                conexao.execute(comando_sql, valores)
                total_registros += 1

            # Confirmar a transação e fechar a conexão
            conexao.commit()
            conexao.close()

            # Exibir mensagem de sucesso
            exibir_mensagem(f"Dados importados com sucesso para o banco de dados SQLite.\n"
                            f"Registros importados: {total_registros}", texto_saida)
        
        except Exception as e:
            # Exibir mensagem de erro
            exibir_mensagem(f"Erro ao importar dados: {e}", texto_saida)

def importAlunos(screen):
    # Criar a tela
    # screen = tk.Tk()
    # screen.title("Importar Dados do Excel para SQLite")

    # Botão para selecionar o arquivo Excel
    botao_selecionar_arquivo = tk.Button(screen, text="Selecionar Arquivo Excel (Aluno)", command=lambda: importar_excel_para_sqlite(screen, texto_saida))
    botao_selecionar_arquivo.pack(pady=10)

    # Texto de saída para exibir o local do arquivo e a quantidade de registros importados
    texto_saida = tk.Text(screen, height=6, width=50, wrap=tk.WORD)
    texto_saida.pack()

    # screen.mainloop()

# Chamar a função para importar alunos
# importAlunos()