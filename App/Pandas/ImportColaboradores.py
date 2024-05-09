import sqlite3
import tkinter as tk
from tkinter import filedialog
import pandas as pd
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

def importar_excel_colaborador_para_sqlite(screen, texto_saida):
    # Abrir a janela de seleção de arquivo
    filename = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])

    if filename:
        try:
            # Ler o arquivo Excel
            df = pd.read_excel(filename)

            # Conectar ao banco de dados SQLite
            conexao = sqlite3.connect(buscaDB)

            # Iterar sobre as linhas do DataFrame e inserir os dados na tabela
            total_registros = 0
            for index, row in df.iterrows():
                # Convertendo os tipos de dados conforme necessário
                cpf = str(row['cpf'])
                nome = str(row['nome'])
                email = str(row['e-mail'])
                cargo = str(row['cargo'])

                # Inserindo os dados na tabela Colaborador
                comando_sql = "INSERT INTO Colaborador (cpf, nome, email, cargo) VALUES (?, ?, ?, ?)"
                valores = (cpf, nome, email, cargo)
                conexao.execute(comando_sql, valores)
                total_registros += 1

            # Confirmar a transação e fechar a conexão
            conexao.commit()
            conexao.close()

            # Exibir mensagem de sucesso
            exibir_mensagem(f"Dados importados com sucesso para a tabela Colaborador.\n"
                            f"Registros importados: {total_registros}", texto_saida)
        
        except Exception as e:
            # Exibir mensagem de erro
            exibir_mensagem(f"Erro ao importar dados: {e}", texto_saida)

def importColaboradores(screen):
    # Criar a tela de importação de colaboradores
    # screen = tk.Frame(screen)
    # screen.pack()

    # Botão para selecionar o arquivo Excel (Colaboradores)
    botao_selecionar_arquivo_colaborador = tk.Button(screen, text="Selecionar Arquivo Excel (Colaboradores)", command=lambda: importar_excel_colaborador_para_sqlite(screen, texto_saida))
    botao_selecionar_arquivo_colaborador.pack(pady=10)

    # Texto de saída para exibir mensagens
    texto_saida = tk.Text(screen, height=6, width=50, wrap=tk.WORD)
    texto_saida.pack()

# Criar a janela principal
# root = tk.Tk()
# root.title("Importar Dados do Excel para SQLite")

# # Criar a tela de importação de colaboradores
# importColaboradores(root)

# root.mainloop()
