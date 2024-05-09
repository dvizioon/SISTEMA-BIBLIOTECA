import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
import yaml
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
sys.path.append(".")
from App.Modules.LerYaml import LerYaml

buscaDB = LerYaml(".Yaml", "caminhoDB", index=0)

# janela = tk.Tk()
# janela.title("SQL Query Builder")
def commandScreen(janela):
    
    def obter_tabelas():
        try:
            conexao = sqlite3.connect(buscaDB)
            cursor = conexao.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = cursor.fetchall()
            conexao.close()
            return [tabela[0] for tabela in tabelas]
        except sqlite3.Error as error:
            print("Erro ao obter tabelas:", error)
            return []
    
    def op_operacoes(event=None):
        operacao_selecionada = combo_operacoes.get()
        if operacao_selecionada == "insert":
            pass
        else:
            for widget in frame_formulario.winfo_children():
                widget.destroy()
            frame_formulario.grid_forget()  # Esconde o formulário
        
    def gerar_formulario(event=None):
        tabela_selecionada = combo_tabelas.get()
        operacao_selecionada = combo_operacoes.get()

        if operacao_selecionada == "insert" and tabela_selecionada:
            conexao = sqlite3.connect(buscaDB)
            cursor = conexao.cursor()
            cursor.execute(f"PRAGMA table_info({tabela_selecionada})")
            colunas = [coluna[1] for coluna in cursor.fetchall()]
            conexao.close()

            for widget in frame_formulario.winfo_children():
                widget.destroy()

            for i, coluna in enumerate(colunas):
                label = ttk.Label(frame_formulario, text=coluna.capitalize() + ":")
                label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

                entry = ttk.Entry(frame_formulario)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)

                form_entries[coluna] = entry

            frame_formulario.grid(row=2, column=0, columnspan=2, sticky=tk.W)  # Mostra o formulário
        else:
            for widget in frame_formulario.winfo_children():
                widget.destroy()
            frame_formulario.grid_forget()  # Esconde o formulário

    def gerar_script():
        tabela_selecionada = combo_tabelas.get()
        operacao_selecionada = combo_operacoes.get()

        if tabela_selecionada and operacao_selecionada:
            if operacao_selecionada == "insert":
                colunas = ', '.join(form_entries.keys())
                valores_inseridos = [f"'{entry.get()}'" for entry in form_entries.values()]
                valores = ', '.join(valores_inseridos)
                script_sql = f"INSERT INTO {tabela_selecionada} ({colunas}) VALUES ({valores});"

                texto_script.config(state="normal")  # Define o estado como "normal" para permitir a inserção de texto
                texto_script.delete(1.0, tk.END)  # Limpa o conteúdo da área de texto
                texto_script.insert(tk.END, script_sql)  # Insere o script gerado na área de texto
                texto_script.config(state="disabled")  # Define o estado como "disabled" novamente para tornar o texto somente leitura

            else:
                script_sql = f"{operacao_selecionada.upper()} * FROM {tabela_selecionada};"

                
                texto_script.config(state="normal")  # Define o estado como "normal" para permitir a inserção de texto
                texto_script.delete(1.0, tk.END)  # Limpa o conteúdo da área de texto
                texto_script.insert(tk.END, script_sql)  # Insere o script gerado na área de texto
                texto_script.config(state="disabled")  # Define o estado como "disabled" novamente para tornar o texto somente leitura
        else:
            messagebox.showwarning("Aviso", "Selecione uma tabela e uma operação antes de gerar o script.")

    
    def exibir_tabela(dados, cursor):
        # Criar uma nova janela para exibir a tabela
        janela_tabela = tk.Toplevel()
        janela_tabela.title("Tabela Resultante")
        
        # Criar uma treeview para exibir os dados em forma de tabela
        tree = ttk.Treeview(janela_tabela)

        if not dados:  # Verificar se os dados estão vazios
            tree['columns'] = ('Mensagem',)
            tree.heading('#0', text='Mensagem')
            tree.column('#0', width=200)
            tree.insert('', 'end', values=('Nenhum dado disponível',))
        else:
            tree['columns'] = tuple(range(len(dados[0])))
            
            # Obter os nomes reais das colunas do cursor
            colunas = cursor.description
            
            # Definir os nomes das colunas
            for i, info_coluna in enumerate(colunas):
                nome_coluna = info_coluna[0]
                tree.heading(i, text=nome_coluna)
            
            # Adicionar os dados à treeview
            for linha in dados:
                tree.insert('', 'end', values=linha)
        
        # Adicionar barra de rolagem
        scroll_y = ttk.Scrollbar(janela_tabela, orient="vertical", command=tree.yview)
        scroll_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scroll_y.set)
        
        # Exibir a treeview
        tree.pack(expand=True, fill="both")
        
        # Adicionar barra de rolagem
        scroll_y = ttk.Scrollbar(janela_tabela, orient="vertical", command=tree.yview)
        scroll_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scroll_y.set)
        
        # Exibir a treeview
        tree.pack(expand=True, fill="both")

    def exe_script():
        operacao_selecionada = combo_operacoes.get()
        if operacao_selecionada == "insert":
            script_sql = texto_script.get("1.0", tk.END)  # Obtém o script SQL do widget texto_script
            try:
                conexao = sqlite3.connect(buscaDB)
                cursor = conexao.cursor()

                # Divide o script em instruções individuais
                instrucoes = script_sql.split(';')
                
                # Remove espaços em branco e linhas vazias
                instrucoes = [instrucao.strip() for instrucao in instrucoes if instrucao.strip()]
                
                # Executa cada instrução individualmente
                for instrucao in instrucoes:
                    cursor.execute(instrucao)

                conexao.commit()  # Confirma as alterações no banco de dados
                conexao.close()
                print("Script executado com sucesso!")
            except sqlite3.Error as error:
                print(error)
                messagebox.showerror("Erro", f"Erro ao executar o script: {error}")
        elif operacao_selecionada == "select":
            script_sql = texto_script.get("1.0", tk.END)
            try:
                conexao = sqlite3.connect(buscaDB)
                cursor = conexao.cursor()
                cursor.execute(script_sql)
                dados = cursor.fetchall()
                exibir_tabela(dados, cursor)  # Passa o cursor como argumento
            except sqlite3.Error as error:
                messagebox.showerror("Erro", f"Erro ao executar o script de seleção: {error}")


   
    # Criar o frame principal
    frame = ttk.Frame(janela, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Adicionar o seletor de operações
    label_operacoes = ttk.Label(frame, text="Operações:")
    label_operacoes.grid(row=1, column=0, sticky=tk.W)

    operacoes = ["select", "insert"]
    combo_operacoes = ttk.Combobox(frame, values=operacoes, state="readonly")
    combo_operacoes.grid(row=0, column=1, sticky=tk.W)

    # Adicionar o seletor de tabelas
    label_tabelas = ttk.Label(frame, text="Tabelas:")
    label_tabelas.grid(row=0, column=0, sticky=tk.W)

    tabelas = obter_tabelas()
    combo_tabelas = ttk.Combobox(frame, values=tabelas, state="readonly")
    combo_tabelas.grid(row=1, column=1, sticky=tk.W)

    # Adicionar o frame para o formulário dinâmico
    frame_formulario = ttk.Frame(frame, padding="10")
    frame_formulario.grid(row=2, column=0, columnspan=2, sticky=tk.W)

    # Dicionário para armazenar as entradas do formulário
    form_entries = {}

    # Adicionar a área de texto para o script SQL
    label_script = ttk.Label(frame, text="Script SQL:")
    label_script.grid(row=3, column=0, sticky=tk.W)

    texto_script = tk.Text(frame, width=50, height=10, state="disabled")
    texto_script.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)


    # Adicionar o botão para gerar o script
    # Criar um frame para os botões
    frame_botoes = ttk.Frame(frame)
    frame_botoes.grid(row=4, column=0, columnspan=2, pady=10)

    # Adicionar o botão para gerar o script
    botao_gerar = ttk.Button(frame_botoes, text="Gerar Script", command=gerar_script)
    botao_gerar.grid(row=0, column=0, padx=(0, 10))

    # Adicionar o botão para exibir o script
    botao_exibir_script = ttk.Button(frame_botoes, text="Executar Script", command=exe_script)
    botao_exibir_script.grid(row=0, column=1)


    # Associar a função gerar_formulario à mudança de seleção no seletor de tabelas
    combo_tabelas.bind("<<ComboboxSelected>>", lambda event: gerar_formulario(combo_tabelas.get()))
    combo_operacoes.bind("<<ComboboxSelected>>", op_operacoes)
    
    
    

# Chamar a função para criar a tela
# commandScreen(janela)
# janela.mainloop()
