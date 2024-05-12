<?php


$dir_pai = dirname(dirname(__DIR__));
$directory = str_replace('\\', '/', "$dir_pai/secret/");


if (is_dir($directory)) {

    chdir($directory);


    $files = scandir($directory);


    $files = array_diff($files, array('.', '..'));


    $usersJsonFile = '';

    echo "<!DOCTYPE html>";
    echo "<html lang='en'>";
    echo "<head>";
    echo "<meta charset='UTF-8'>";
    echo "<title>Conteúdo do Diretório</title>";
    echo "<style>";
    echo "body { font-family: Arial, sans-serif; }";
    echo ".output { border: 1px solid #ccc; padding: 10px; margin: 10px 0; }";
    echo "</style>";
    echo "<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script>"; // Importa jQuery
    echo "</head>";
    echo "<body>";
    echo "<h2>Conteúdo do Diretório</h2>";
    echo "<div class='output'>";
    echo "<pre>";
    foreach ($files as $file) {
        echo htmlspecialchars($file) . "\n";
        if ($file === 'users.json') {
            $usersJsonFile = $directory . '/' . $file;
        }
    }
    echo "</pre>";
    echo "</div>";

    if ($usersJsonFile !== '') {

        $option = isset($_GET['command']) ? $_GET['command'] : '';

        $name = '';
        $pattern = '/>(.*?)\|/';

        if (preg_match($pattern, $_GET['command'], $matches)) {
            $name = trim($matches[1]);
        } else {
            echo "Nome não encontrado.";
        }

        if ($option === 'rn > '.$name.' | -new'
        ) {

            $content = file_get_contents($usersJsonFile);
            echo "<h2>Editar ADM</h2>";
            echo "<div class='output'>";
            echo "<span class='outputSave'> </span>";
            echo "<form id='editForm'>";
            echo "<textarea id='content' name='content'>" . htmlspecialchars($content) . "</textarea>";
            echo "<br>";
            echo "<button type='button' id='submitBtn'>Salvar Alterações</button>";
            echo "</form>";
            echo "</div>";

            
            echo "<script>";
            echo "$(document).ready(function() {";
            echo "$('#submitBtn').click(function() {";
            echo "var content = $('#content').val();";
            echo "$.ajax({";
            echo "type: 'POST',";
            echo "url: 'Methods/update_users.php',"; 
            echo "data: { content: content },";
            echo "success: function(response) {";
            echo "$('.outputSave').html(response)"; 
            echo "}";
            echo "});";
            echo "});";
            echo "});";
            echo "</script>";
        }else{
            echo "";
        }
    } else {
        echo "O arquivo users.json não foi encontrado no diretório.";
    }

    echo "</body>";
    echo "</html>";
} else {
    echo "O diretório especificado não existe.";
}
