import os
import json
import requests
import zipfile
import sys
from tqdm import tqdm

sys.path.append(".")
t = """
                                               _____ _ _ 
     /\                                       / ____| (_)
    /  \   _ __   __ _ _   _  ___ _ __ __ _  | |    | |_ 
   / /\ \ | '_ \ / _` | | | |/ _ \ '__/ _` | | |    | | |
  / ____ \| | | | (_| | |_| |  __/ | | (_| | | |____| | |
 /_/    \_\_| |_|\__, |\__,_|\___|_|  \__,_|  \_____|_|_|
                  __/ |                                  
                 |___/     
 V.0.2                                        dvizioon.com                                              

"""

print(t)

def baixar_e_extrair_arquivo(url, destino, destino_extracao):
    # Envia uma solicitação GET para o URL
    response = requests.get(url, stream=True)

    # Verifica se a solicitação foi bem-sucedida (status code 200)
    if response.status_code == 200:
        # Define o tamanho total do arquivo para a barra de progresso
        tamanho_total = int(response.headers.get('content-length', 0))

        # Cria a barra de progresso
        barra_de_progresso = tqdm(total=tamanho_total, unit='B', unit_scale=True, desc="Download")

        # Salva o conteúdo da resposta em um arquivo local
        with open(destino, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                barra_de_progresso.update(len(chunk))

        # Fecha a barra de progresso
        barra_de_progresso.close()

        print(f"Arquivo baixado com sucesso de {url}")

        # Extrai o conteúdo do arquivo ZIP
        with zipfile.ZipFile(destino, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                # Verifica se o arquivo é um diretório
                if file_info.is_dir():
                    continue  # Ignora diretórios, já que eles são criados automaticamente

                # Extrai apenas o nome do arquivo
                filename = os.path.basename(file_info.filename)

                # Extrai o arquivo
                zip_ref.extract(file_info, destino_extracao)
                print(f"Arquivo extraído: {filename}")

        # Remove o arquivo ZIP após a extração
        os.remove(destino)
        print(f"Arquivo {destino} removido após a extração.")
    else:
        print(f"Falha ao baixar o arquivo de {url}: {response.reason}")

# Ler o conteúdo do arquivo JSON
with open('./App/Http/Path.json', 'r') as json_file:
    data = json.load(json_file)

destino_extracao = data[0]['_cDE']
destino_CriarPasta = data[0]['_cPE']
url_extracao = data[0]['_url']

baixar_e_extrair_arquivo(url_extracao, destino_extracao, destino_CriarPasta)
