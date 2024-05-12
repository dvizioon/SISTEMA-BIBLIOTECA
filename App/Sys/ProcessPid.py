import sys
sys.path.append(".")
import psutil
import os

import os

def pidProcess(op, pid, arquivo_pid):
    if op == 'cPID':  # Criar um novo PID
        criarPid(pid, arquivo_pid)
        return f"PID {pid} criado e armazenado no arquivo '{arquivo_pid}'"
    elif op == 'lPID':  # Ler todos os PIDs armazenados no arquivo
        return lerPids(arquivo_pid)
    elif op == 'fPID':  # Buscar um PID específico no arquivo
        return buscarPid(pid, arquivo_pid)
    elif op == 'dPID':  # Limpar o arquivo, removendo todos os PIDs
        limparPids(arquivo_pid)
        return f"Arquivo '{arquivo_pid}' limpo com sucesso."
    else:
        return "Operação inválida. Opções válidas: 'cPID', 'lPID', 'fPID', 'dPID'"

def criarPid(pid, arquivo_pid):
    # Verificar se o arquivo já existe
    if os.path.exists(arquivo_pid):
        # Verificar se o arquivo está vazio
        if os.path.getsize(arquivo_pid) > 0:
            # Se o arquivo não estiver vazio, adicionar o PID em uma nova linha
            with open(arquivo_pid, 'a') as file:
                file.write('\n' + str(pid))
        else:
            # Se o arquivo estiver vazio, escrever o PID no arquivo
            with open(arquivo_pid, 'w') as file:
                file.write(str(pid))
    else:
        # Se o arquivo não existe, escrever o PID no arquivo
        with open(arquivo_pid, 'w') as file:
            file.write(str(pid))

def lerPids(arquivo_pid):
    # Verificar se o arquivo existe
    if os.path.exists(arquivo_pid):
        # Ler todos os PIDs do arquivo e retornar apenas os números
        with open(arquivo_pid, 'r') as file:
            pids = [linha.strip() for linha in file.readlines()]
            return pids
    else:
        return "Arquivo de PID não encontrado."

def buscarPid(pid, arquivo_pid):
    # Verificar se o arquivo existe
    if os.path.exists(arquivo_pid):
        # Buscar o PID específico no arquivo
        with open(arquivo_pid, 'r') as file:
            for linha in file:
                if linha.strip() == str(pid):
                    return f"PID {pid} encontrado no arquivo '{arquivo_pid}'."
            return f"PID {pid} não encontrado no arquivo '{arquivo_pid}'."
    else:
        return "Arquivo de PID não encontrado."

def limparPids(arquivo_pid):
    # Verificar se o arquivo existe
    if os.path.exists(arquivo_pid):
        print("Processamento Limpo")
        # Limpar o arquivo, removendo todos os PIDs
        with open(arquivo_pid, 'w') as file:
            pass
    else:
        print(f"Arquivo '{arquivo_pid}' não encontrado.")


# Criar um novo PID e armazenar no arquivo
# op = 'cPID'
# pid = os.getpid()
# arquivo_pid = "App\Sys\pid.txt"
# print(pidProcess(op, pid, arquivo_pid))

# # Ler todos os PIDs armazenados no arquivo
# op = 'lPID'
# print(pidProcess(op, None, arquivo_pid))

# # Buscar um PID específico no arquivo
# op = 'fPID'
# pid = 12345  # PID que você deseja buscar
# print(pidProcess(op, pid, arquivo_pid))

# # Limpar o arquivo de PIDs
# op = 'dPID'
# arquivo_pid = "App\Sys\pid.txt"
# print(pidProcess(op, None, arquivo_pid))
