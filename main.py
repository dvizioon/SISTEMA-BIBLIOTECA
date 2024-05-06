import sys
sys.path.append(".")
import psutil
import os
from App.Screens.Apresentation import apresentation
from App.Screens.Login import login_loop
from App.Modules.LerYaml import LerYaml
from App.Sys.ProcessPid import pidProcess

caminhoDB = LerYaml(".Yaml","caminhoDB",index=1)

op = 'cPID'
pid = os.getpid()
arquivo_pid = "App\Sys\pid.txt"
print(pidProcess(op, pid, arquivo_pid))

def verificarBanco(caminho, nomeDB):
    db_directory = f"./{caminho}"
    db_filename = nomeDB
    db_path = os.path.join(db_directory, db_filename)

    # Verifica se o diretório existe
    if not os.path.exists(db_directory):
        return False

    # Verifica se o banco de dados existe
    if os.path.exists(db_path):
        return True
    else:
        return False


if not verificarBanco(caminhoDB, "angueraBook.sqlite"):
    apresentation()
else:
    login_loop()

