import os
import json

def verificar_e_criar_users_json():
    diretorio_secret = "./secret"
    users_json_path = os.path.join(diretorio_secret, "users.json")

    # Verificar se o diretório './secret' existe
    if os.path.exists(diretorio_secret):
        print("O diretório './secret' já existe.")

        # Verificar se o arquivo 'users.json' existe
        if os.path.exists(users_json_path):
            print("O arquivo 'users.json' já existe.")
        else:
            # Criar o arquivo 'users.json' se não existir
            with open(users_json_path, 'w') as f:
                json.dump({}, f)
            print("O arquivo 'users.json' foi criado.")
    else:
        # Criar o diretório './secret' se não existir
        os.makedirs(diretorio_secret)
        print("O diretório './secret' foi criado.")

        # Criar o arquivo 'users.json'
        with open(users_json_path, 'w') as f:
            json.dump({}, f)
        print("O arquivo 'users.json' foi criado.")

