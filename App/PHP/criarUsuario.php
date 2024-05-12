<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulário de Cadastro de Usuário</title>

    <style>
        ::selection {
            background: #ff5e99;
        }

        #container {
            padding: 1em 1.5em 1em 1em;
        }

        #container output {
            clear: both;
            width: 100%;
        }

        #container output h3 {
            margin: 0;
        }

        #container output pre {
            margin: 0;
        }

        #prompt {
            float: left;
            color: white;
            margin-right: 7px;
            font-family: Arial, sans-serif;
            font-weight: 700;
            font-variant: small-caps;
            letter-spacing: 0.1rem;
            background-color: #00c300;
            padding: 0.4rem;
            border-radius: 22rem;
        }

        #header img {
            width: 100%;
        }

        #cmdline {
            float: left;
            margin: 0;
            width: 96%;
            font: inherit;
            border: none;
            background-color: transparent;
            outline: none;
            color: inherit;
            font-weight: 600;
            color: #dc143c;
        }

        .cmd-output {
            width: 100%;
            overflow: hidden;
            height: 8rem;
            overflow-y: scroll;
        }


        .cmdline_cli {
            display: flex;
            align-items: center;
        }
    </style>

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e90ff;
            /* Azul claro estilo Windows */
            margin: 0;
            padding: 0;
            color: #000;
            /* Cor do texto */
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100vw;
            height: 100vh;
            gap: 1rem;
        }

        .container {
            width: 45%;
            height: 80%;
            background-color: #ffffff;
            /* Branco para contraste */
            border: 2px solid #4682b4;
            /* Azul escuro para borda */
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            text-align: left;
            padding: 1rem;
            color: #000;
            /* Cor do texto dentro do contêiner */
        }

        h1 {
            font-size: 2em;
            color: #4169e1;
            /* Azul mais escuro para título */
            margin-bottom: 20px;
        }

        input {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: 1px solid #a9a9a9;
            /* Cinza mais claro para borda */
            width: 100%;
            box-sizing: border-box;
        }

        .btn {
            background-color: #4169e1;
            /* Azul escuro para botão */
            color: #fff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 1.2em;
            border: none;
            cursor: pointer;
        }

        .btn:hover {
            background-color: #1e90ff;
            /* Azul mais claro ao passar o mouse */
        }

        .excluir-usuario {
            background-color: #ff4500;
            /* Vermelho para botão de exclusão */
            color: #fff;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .excluir-usuario:hover {
            background-color: #dc143c;
            /* Vermelho mais escuro ao passar o mouse */
        }

        .comunicado {
            max-width: 600px;
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin-top: 1rem;
        }

        .comunicado img {
            width: 150px;
            height: 100px;
        }

        .comunicado p {
            font-size: 16px;
            line-height: 1.5;
            color: #333;
            text-align: justify;
        }

        .comunicado a {
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }

        .comunicado a:hover {
            text-decoration: underline;
        }

        pre {
            background-color: #f4f4f4;
            border: 1px solid #ccc;
            padding: 10px;
            margin: 10px 0;
            white-space: pre-wrap;
            overflow: hidden;
            height: 5rem;
            overflow-y: scroll;
            /* Permite quebrar linhas */
        }

        code {
            display: block;
            /* Exibe cada comando em uma linha separada */
            font-family: monospace;
            /* Usa uma fonte monoespaçada para manter a formatação */
            color: #333;
            /* Cor do texto */
        }
    </style>

    <style>
        .command-line {
            font-size: 14px;
            width: 600px;
            height: 400px;
            background: #000;
            overflow-x: hidden;
            overflow-y: scroll;
        }

        .command-line.light {
            background-color: #fff;
        }

        .command-line.light .command-row {
            position: relative;
            margin-bottom: 5px;
        }

        .command-line.light .command-row.active {
            background: #f5f5f5;
        }

        .command-line.light .command-row .command-time {
            color: #000;
        }

        .command-line.light .command-row .command-user {
            color: #000;
        }

        .command-line.light .command-row .command-entry {
            color: #000;
        }

        .command-line .command-row {
            position: relative;
            margin-bottom: 5px;
        }

        .command-line .command-row.active {
            background: #1d1d1d;
        }

        .command-line .command-row .command-time {
            color: #e7e7e7;
            display: inline-block;
            padding-right: 5px;
        }

        .command-line .command-row .command-user {
            color: #e7e7e7;
            font-weight: 700;
            display: inline-block;
            padding-right: 5px;
        }

        .command-line .command-row .command-entry {
            padding-right: 5px;
            color: #fff;
            display: inline;
            /* These are technically the same, but use both */
            overflow-wrap: break-word;
            word-wrap: break-word;
            -ms-word-break: break-all;
            /* This is the dangerous one in WebKit, as it breaks things wherever */
            word-break: break-all;
            /* Adds a hyphen where the word breaks, if supported (No Blink) */
            -ms-hyphens: auto;
            -moz-hyphens: auto;
            -webkit-hyphens: auto;
            hyphens: auto;
        }

        .command-line .command-row .command-entry.command-entry-protected:empty {
            display: none;
        }

        .command-line .command-row .command-entry.block {
            display: block;
        }

        .command-line .command-row .command-entry:focus {
            outline: none;
        }

        .command-line .command-row .secret {
            position: absolute;
            width: 100%;
            height: 100%;
            left: 0;
            opacity: 0;
        }

        .command-line .command-row.error .command-entry {
            font-weight: 700;
            color: red;
        }

        .command-line .command-row.success .command-entry {
            font-weight: 700;
            color: #00c300;
        }

        .command-line .command-row.info .command-entry {
            font-weight: 700;
            color: #00a9ff;
        }

        .command-line .command-row.warning .command-entry {
            font-weight: 700;
            color: orange;
        }

        .mac-window {
            border-radius: 5px;
            margin: 40px auto;
            overflow: hidden;
            width: 600px;
            -webkit-box-shadow: 0px 10px 60px rgba(0, 0, 0, 0.2);
            box-shadow: 0px 10px 60px rgba(0, 0, 0, 0.2);
        }

        .mac-window.minimize {
            top: 125%;
            -webkit-transform: translateY(-50%) translateX(-50%) scale(1);
            -ms-transform: translateY(-50%) translateX(-50%) scale(1);
            transform: translateY(-50%) translateX(-50%) scale(1);
            opacity: 1;
            -webkit-transition: all 0.5s;
            transition: all 0.5s;
        }

        .mac-window.minimize:hover {
            top: 120%;
            -webkit-transition: all 0.5s;
            transition: all 0.5s;
        }

        .mac-window.maximize {
            height: 100%;
            max-height: 100%;
            width: 100%;
            max-width: 100%;
            -webkit-transform: translateY(-50%) translateX(-50%) scale(1);
            -ms-transform: translateY(-50%) translateX(-50%) scale(1);
            transform: translateY(-50%) translateX(-50%) scale(1);
        }

        .mac-window .title-bar {
            background: #d0cfd0;
            background: -webkit-gradient(linear, left bottom, left top, from(#c8c5c8), to(#eae7ea));
            background: -webkit-linear-gradient(bottom, #c8c5c8, #eae7ea);
            background: linear-gradient(to top, #c8c5c8, #eae7ea);
            height: 20px;
            border-bottom: 1px solid #b4b4b4;
            width: 100%;
            clear: both;
        }

        .mac-window .title-bar .buttons {
            height: 100%;
            width: 51px;
            float: left;
            margin-left: 9px;
        }

        .mac-window .title-bar .buttons .close,
        .mac-window .title-bar .buttons .minimize,
        .mac-window .title-bar .buttons .maximize {
            float: left;
            height: 10px;
            width: 10px;
            border-radius: 50%;
            margin-top: 5px;
            background: #fb4948;
            border: solid 1px rgba(214, 46, 48, 0.15);
            position: relative;
        }

        .mac-window .title-bar .buttons .close:before,
        .mac-window .title-bar .buttons .minimize:before,
        .mac-window .title-bar .buttons .maximize:before {
            content: '';
            position: absolute;
            height: 1px;
            width: 8px;
            background: #360000;
            top: 50%;
            left: 50%;
            -webkit-transform: translateY(-50%) translateX(-50%) rotate(45deg);
            -ms-transform: translateY(-50%) translateX(-50%) rotate(45deg);
            transform: translateY(-50%) translateX(-50%) rotate(45deg);
            opacity: 0;
        }

        .mac-window .title-bar .buttons .close:after,
        .mac-window .title-bar .buttons .minimize:after,
        .mac-window .title-bar .buttons .maximize:after {
            content: '';
            position: absolute;
            height: 1px;
            width: 8px;
            background: #360000;
            top: 50%;
            left: 50%;
            -webkit-transform: translateY(-50%) translateX(-50%) rotate(-45deg);
            -ms-transform: translateY(-50%) translateX(-50%) rotate(-45deg);
            transform: translateY(-50%) translateX(-50%) rotate(-45deg);
            opacity: 0;
        }

        .mac-window .title-bar .buttons .minimize {
            background: #fdb225;
            margin-left: 8.5px;
            border-color: rgba(213, 142, 27, 0.15);
            position: relative;
        }

        .mac-window .title-bar .buttons .minimize:before {
            content: '';
            position: absolute;
            height: 1px;
            width: 8px;
            background: #864502;
            top: 50%;
            left: 50%;
            -webkit-transform: translateY(-50%) translateX(-50%);
            -ms-transform: translateY(-50%) translateX(-50%);
            transform: translateY(-50%) translateX(-50%);
        }

        .mac-window .title-bar .buttons .minimize:after {
            display: none;
        }

        .mac-window .title-bar .buttons .maximize {
            float: right;
            background: #2ac833;
            border-color: rgba(30, 159, 32, 0.15);
        }

        .mac-window .title-bar .buttons .maximize:before {
            width: 6px;
            height: 6px;
            background: #0b5401;
            -webkit-transform: translateY(-50%) translateX(-50%);
            -ms-transform: translateY(-50%) translateX(-50%);
            transform: translateY(-50%) translateX(-50%);
            border: solid #2ac833 1px;
            border-radius: 2px;
        }

        .mac-window .title-bar .buttons .maximize:after {
            width: 10px;
            height: 2px;
            background: #2ac833;
            -webkit-transform: translateY(-50%) translateX(-50%) rotate(45deg);
            -ms-transform: translateY(-50%) translateX(-50%) rotate(45deg);
            transform: translateY(-50%) translateX(-50%) rotate(45deg);
        }

        .mac-window .title-bar .buttons:hover .close:before,
        .mac-window .title-bar .buttons:hover .minimize:before,
        .mac-window .title-bar .buttons:hover .maximize:before {
            opacity: 1;
        }

        .mac-window .title-bar .buttons:hover .close:after,
        .mac-window .title-bar .buttons:hover .minimize:after,
        .mac-window .title-bar .buttons:hover .maximize:after {
            opacity: 1;
        }

        .mac-window .title-bar .title {
            height: 100%;
            text-align: center;
            margin-right: 60px;
            font-family: ' Helvetica Neue', helvetica, arial, sans-serif;
            line-height: 21px;
            font-size: 13px;
            color: #222022;
        }

        .mac-window .window {
            background: white;
            max-height: 90vh;
            height: 100%;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Cadastro de Administrador</h1>
        <form id="form-cadastro" action="cadastro_usuario.php" method="post">
            <label for="usuario">Usuário:</label>
            <input type="text" id="usuario" name="usuario" required>
            <label for="senha">Senha:</label>
            <input type="password" id="senha" name="senha" required>
            <button type="submit" class="btn">Cadastrar</button>
        </form>

        <div class="comunicado">
            <img src="https://static.vecteezy.com/system/resources/thumbnails/012/042/301/small_2x/warning-sign-icon-transparent-background-free-png.png" alt="Alerta">
            <p>Se você esqueceu sua senha, será necessário recriar sua conta de Administrador. Isso ocorre porque sua senha é criptografada, o que significa que não podemos recuperá-la diretamente. <a href="https://pt.wikipedia.org/wiki/Fun%C3%A7%C3%A3o_hash" target="_blank">Saiba mais sobre hash</a>.</p>
        </div>
    </div>

    <div class="container" id="usuarios-container">
        <h1>Administrador Cadastrados</h1>
        <ul id="usuarios-list">
            <?php
            $dir_pai = dirname(dirname(__DIR__));

            echo ">>> " . $dir_pai;
            function listar_usuarios($caminho_arquivo)
            {
                $usuarios = ler_usuarios($caminho_arquivo);
                foreach ($usuarios as $usuario) {
                    echo "<li class='li-user'>{$usuario['usuario']} <button class='excluir-usuario' data-usuario='{$usuario['usuario']}'>Excluir</button></li>";
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

        <!-- First Screen -->
        <div class="mac-window active">
            <div class="title-bar">
                <div class="buttons">
                    <div class="close"></div>
                    <div class="minimize"></div>
                    <div class="maximize"></div>
                </div>
                <div class="title">
                    Terminal
                </div>
            </div>
            <div class="window" style="padding: 1rem;">

                <div id="header">
                    <img src="./cliBook.png" />
                </div>
                <output id="output">
                </output>
                <div class="cmdline_cli">
                    <div id="prompt"><?php echo ler_usuarios($caminho_arquivo)['0']['usuario'] ?>[AngueraBook/secret]></div>
                    <input id="cmdline">
                </div>

            </div>
        </div>

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
                        $('#usuarios-list').append('<li>' + response + ' </li> ');
                        window.location.reload(false);
                    },
                    error: function(xhr, status, error) {
                        console.error(error); // Exibe erros no console
                    }
                });
            });
        });

        // Evento de clique no botão de exclusão de usuário
        $(document).on("click", ".excluir-usuario", function() {
            var usuario = $(this).data("usuario");
            $.ajax({
                url: "excluirUsuario.php", // Script PHP para exclusão do usuário
                method: "POST",
                data: {
                    usuario: usuario
                },
                success: function(response) {
                    window.location.reload(false);
                },
                error: function(xhr, status, error) {
                    console.error(error); // Exibe erros no console
                }
            });
        });
    </script>

    <script>
        var Terminal = Terminal || {};
        var Command = Command || {};

        output.innerHTML = `
<pre>
<code>--help || -h || help</code>
<code>rn > <?php echo ler_usuarios($caminho_arquivo)['0']['usuario'] ?> | -new </code>
</pre>
                        `

        Terminal.FilesystemErrorHandler = function(event) {
            // Manipulação de erros do sistema de arquivos aqui
        };

        Terminal.Events = function(inputElement, outputElement) {
                var input = document.getElementById(inputElement);
                var output = document.getElementById(outputElement);

                input.onkeydown = function(event) {
                        if (event.key === 'Enter') {
                            var inputValue = input.value.trim();

                            // Verifica se inputValue é "--help" ou "-help"
                            if (inputValue === "--help" || inputValue === "-h" || inputValue === "help") {
                                output.innerHTML = `
<pre>
<code>rn > <?php echo ler_usuarios($caminho_arquivo)['0']['usuario']  ?> | -new </code>
</pre>
                        `;
                            } else if (inputValue !== '') {
                                output.innerHTML = ''; // Limpa o conteúdo anterior
                                sendAjaxRequest(inputValue); // Envia a solicitação AJAX
                            } else {
                                output.innerHTML = `
<pre>
<code>rn > <?php echo ler_usuarios($caminho_arquivo)['0']['usuario']  ?> | -new </code>
</pre> `
                    }
                }
            };



        };

        // Função para enviar a solicitação AJAX
        function sendAjaxRequest(command) {
            $.ajax({
                url: './ExecCli.php',
                type: 'GET',
                data: {
                    command: command
                },
                success: function(response) {
                    $('#output').append('<div class="cmd-output">' + response + '</div>');
                },
                error: function() {
                    console.error('Erro ao enviar solicitação AJAX.');
                }
            });
        }

        window.onload = function() {
            new Terminal.Events('cmdline', 'output');
        };
    </script>

</body>

</html>