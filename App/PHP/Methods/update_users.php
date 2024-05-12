<?php
$dir_pai = dirname(dirname(dirname(__DIR__)));
$directory = str_replace('\\', '/', "$dir_pai/secret");
// echo $dir_pai;

// Verifica se o método de requisição é POST e se o parâmetro 'content' está definido
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['content'])) {
    // Caminho para o arquivo users.json
    $usersJsonFile = "$directory/users.json";

    // Conteúdo recebido do formulário
    $newContent = $_POST['content'];

    // Tenta escrever o novo conteúdo no arquivo users.json
    if (file_put_contents($usersJsonFile, $newContent)) {
        // Responde com uma mensagem de sucesso
        echo "Alterações salvas com sucesso!";
    } else {
        // Responde com uma mensagem de erro
        echo "Erro ao salvar as alterações.";
    }
} else {
    // Responde com uma mensagem de erro se a requisição não for POST ou se o parâmetro 'content' não estiver definido
    echo "Requisição inválida.";
}
