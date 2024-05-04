<?php
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

function gerar_id_aleatorio($tamanho = 6)
{
    $caracteres = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $id = '';
    for ($i = 0; $i < $tamanho; $i++) {
        $id .= $caracteres[rand(0, strlen($caracteres) - 1)];
    }
    return $id;
}

function usuario_existe($usuario, $usuarios)
{
    foreach ($usuarios as $u) {
        if ($u["usuario"] === $usuario) {
            return true;
        }
    }
    return false;
}

function salvar_usuario($usuario, $senha, $caminho_arquivo)
{
    $usuarios = ler_usuarios($caminho_arquivo);

    if (usuario_existe($usuario, $usuarios)) {
        echo "Usuário já existe!";
        return;
    }

    $id_usuario = gerar_id_aleatorio();
    $hash_senha = hash('sha256', $senha);
    $timestamp = date('Y-m-d H:i:s');
    $novo_usuario = [
        "id" => $id_usuario,
        "usuario" => $usuario,
        "senha_hash" => $hash_senha,
        "criacao" => $timestamp,
        "atualizacao" => $timestamp,
        "img" => ""
    ];
    $usuarios[] = $novo_usuario;
    $json_usuarios = json_encode($usuarios, JSON_PRETTY_PRINT);
    file_put_contents($caminho_arquivo, $json_usuarios);
    header("Location: criarUsuario.php");
    exit; 
}

// Verificar se o formulário foi submetido
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $usuario = $_POST["usuario"];
    $senha = $_POST["senha"];
    $caminho_arquivo = "../../secret/users.json";
    salvar_usuario($usuario, $senha, $caminho_arquivo);
}
