<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulário de Cadastro de Usuário</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #008080;
            margin: 0;
            padding: 0;
            color: #000;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border: 2px solid #000;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            text-align: center;
        }

        h1 {
            font-size: 2em;
            color: #0000ff;
        }

        p {
            font-size: 1.2em;
            color: #000;
        }

        .btn {
            background-color: #008080;
            color: #fff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 1.2em;
            border: none;
            cursor: pointer;
        }

        .btn:hover {
            background-color: #005555;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Cadastro de Usuário</h1>
        <form id="form-cadastro" action="cadastro_usuario.php" method="post">
            <label for="usuario">Usuário:</label>
            <input type="text" id="usuario" name="usuario" required>
            <label for="senha">Senha:</label>
            <input type="password" id="senha" name="senha" required>
            <button type="submit" class="btn">Cadastrar</button>
        </form>
    </div>

    <div class="container" id="usuarios-container">
        <h1>Usuários Cadastrados</h1>
        <ul id="usuarios-list">
            <?php
            echo $dir_pai = dirname(dirname(__DIR__));
            function listar_usuarios($caminho_arquivo)
            {
                $usuarios = ler_usuarios($caminho_arquivo);
                foreach ($usuarios as $usuario) {
                    echo "<li>{$usuario['usuario']}</li>";
                }
            }

            // Função para ler os usuários do arquivo JSON
            function ler_usuarios($caminho_arquivo)
            {
                if (file_exists($caminho_arquivo)) {
                    $conteudo_arquivo = file_get_contents($caminho_arquivo);
                    $usuarios = json_decode($conteudo_arquivo, true);
                    if ($usuarios === null) {
                        $usuarios = [];
                    }
                } else {
                    $usuarios = [];
                }
                return $usuarios;
            }

            // Exibir os usuários cadastrados
            $caminho_arquivo = "$dir_pai\secret\users.json";
            listar_usuarios($caminho_arquivo);
            ?>
        </ul>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#form-cadastro').submit(function(event) {
                event.preventDefault(); // Evita o envio padrão do formulário

                // Envia o formulário via AJAX
                $.ajax({
                    url: $(this).attr('action'),
                    type: $(this).attr('method'),
                    data: $(this).serialize(),
                    success: function(response) {
                        // Limpa os campos do formulário
                        $('#usuario').val('');
                        $('#senha').val('');

                        // Adiciona o novo usuário à lista
                        $('#usuarios-list').append('<li>' + response + '</li>');
                        window.location.reload(false);
                    },
                    error: function(xhr, status, error) {
                        console.error(error); // Exibe erros no console
                    }
                });
            });
        });
    </script>
</body>

</html>