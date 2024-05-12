<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Terminal - CodePen</title>
    <style>
        /* Estilos CSS aqui */
    </style>
</head>

<body>
    <div id="container">
        <output id="output"></output>
        <div class="cmdline_cli">
            <div id="prompt">$></div>
            <input id="cmdline">
        </div>
    </div>
</body>

<script>
    var Terminal = Terminal || {};
    var Command = Command || {};

    Terminal.FilesystemErrorHandler = function(event) {
        // Manipulação de erros do sistema de arquivos aqui
    };

    Terminal.Events = function(inputElement, outputElement) {
        var input = document.getElementById(inputElement);
        var output = document.getElementById(outputElement);

        input.onkeydown = function(event) {
            if (event.key === 'Enter') {
                var inputValue = input.value.trim();
                if (inputValue !== '') {
                    output.innerHTML = ''; // Limpa o conteúdo anterior
                    output.innerHTML += '<div class="cmd-output">Comando: ' + inputValue + '</div>'; // Adiciona a entrada do usuário ao output
                    sendAjaxRequest(inputValue); // Envia a solicitação AJAX
                    input.value = ''; // Limpa o campo de entrada
                }
            }
        };
    };

    // Função para enviar a solicitação AJAX
    function sendAjaxRequest(command) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'URL_DO_SEU_ENDPOINT?command=' + encodeURIComponent(command), true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                document.getElementById('output').innerHTML += '<div class="cmd-output">Resposta: ' + xhr.responseText + '</div>'; // Exibe a resposta no output
            } else {
                console.error('Erro ao enviar solicitação AJAX.');
            }
        };
        xhr.send();
    }

    window.onload = function() {
        new Terminal.Events('cmdline', 'output');
    };
</script>

</html>