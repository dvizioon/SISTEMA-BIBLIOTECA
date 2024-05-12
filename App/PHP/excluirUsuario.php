<?php
$usuario = $_POST["usuario"];
$dir_pai = dirname(dirname(__DIR__));
$caminho_arquivo = "$dir_pai/secret/users.json";

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

function buscar_usuario_por_nome($usuario, $usuarios)
{
    foreach ($usuarios as $key => $u) {
        if ($u["usuario"] === $usuario) {
            return $key;
        }
    }
    return false;
}

function excluir_usuario($usuario, $caminho_arquivo)
{
    $usuarios = ler_usuarios($caminho_arquivo);
    $posicao_usuario = buscar_usuario_por_nome($usuario, $usuarios);
    if ($posicao_usuario !== false) {
        unset($usuarios[$posicao_usuario]);
        $json_usuarios = json_encode($usuarios, JSON_PRETTY_PRINT);
        file_put_contents($caminho_arquivo, $json_usuarios);
        return true;
    }
    return false;
}

if (excluir_usuario($usuario, $caminho_arquivo)) {
    echo "Usuário '$usuario' excluído com sucesso!";
} else {
    echo "Usuário '$usuario' não encontrado!";
}
