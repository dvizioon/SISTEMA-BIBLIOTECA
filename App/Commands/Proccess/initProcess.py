import subprocess
import atexit
import os
import subprocess

def process(script, caminho):
    # Verifica se o arquivo pid.txt existe
    if not os.path.exists(caminho):
        # Se não existir, cria o arquivo vazio
        with open(caminho, "w") as arquivo:
            arquivo.write("")  # Cria um arquivo vazio
        print("Arquivo pid.txt criado.")

    # Inicia o processo
    processo = subprocess.Popen(["powershell.exe", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    pid_do_processo = processo.pid
    # Adiciona o novo valor de PID ao arquivo pid.txt
    with open(caminho, "a") as arquivo:  # Abre o arquivo em modo de adição
         arquivo.write(f"pr1 = {pid_do_processo}\n")  # Adiciona o novo valor ao final do arquivo
    print("Processamento Inicializado")

def encerrar_processo():
    try:
        # Lê o PID do arquivo
        with open("App\Commands\Proccess\pid.txt", "r") as arquivo:
            pid = int(arquivo.read())
        # Encerra o processo com o PID
        os.system(f"taskkill /F /PID {pid}")
        print("Processo PowerShell encerrado.")
    except Exception as e:
        print("Erro ao tentar encerrar o processo PowerShell:", str(e))

# Registra a função encerrar_processo para ser executada quando o script terminar
# atexit.register(encerrar_processo)

# Chama a função process para iniciar o script PowerShell
# process("App\Commands\WebView.ps1","App\Commands\Proccess\pid.txt")
