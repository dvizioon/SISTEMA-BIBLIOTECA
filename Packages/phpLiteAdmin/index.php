<?php
$dir_pai = dirname(dirname(__DIR__));
$config = parse_ini_file($dir_pai . "\config.ini", true);

// Verifica se o formulário foi submetido
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Processa os dados do formulário
    $config['Panel']['Theme'] = $_POST['theme'];
    $config['Panel']['Lang'] = $_POST['lang'];
    $config['Panel']['Host'] = $_POST['host'];
    $config['Panel']['Port'] = $_POST['port'];
    $config['Panel']['Pass'] = $_POST['pass'];
    $config['Panel']['Dir'] = $_POST['dir'];

    // Salva os dados de volta no arquivo config.ini
    $configText = '';
    foreach ($config as $section => $values) {
        $configText .= "[$section]\n";
        foreach ($values as $key => $value) {
            $configText .= "$key = $value\n";
        }
    }
    file_put_contents($dir_pai . "\config.ini", $configText);

    // Redireciona para a mesma página para evitar o reenvio do formulário
    header("Location: " . $_SERVER['PHP_SELF']);
    exit;
}

// Se o arquivo de configuração foi carregado com sucesso, preencha o formulário com os valores
if ($config !== false && isset($config['Panel'])) {
    $theme = $config['Panel']['Theme'];
    $lang = $config['Panel']['Lang'];
}

$temas = array(
    "AlternateBlue",
    "Bootstrap",
    "Default",
    "dynamic_myAdmin",
    "Dynamic",
    "MiamiNights",
    "Modern",
    "pitchGray",
    "PlasticDream",
    "PlasticNightmare",
    "Retro",
    "Shadow",
    "Sheep",
    "simpleGray",
    "SoftieBlue",
    "Ugur3d"
);
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #000;
            color: #fff;
        }

        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #222;
            border: 2px solid #777;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            margin-bottom: 20px;
        }

        .button-container {
            text-align: center;
        }

        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
            border: 2px dotted #777;
            margin: 0 10px;
            width: 200px;
        }

        .button:hover {
            background-color: #0056b3;
        }

        /* Adicionado para ocultar o formulário inicialmente */
        #config-form {
            display: none;
            margin-top: 1rem;
        }

        /* Estilo adicional para o formulário */
        #config-form select,
        #config-form textarea,
        #config-form input[type="submit"] {
            display: block;
            width: calc(100% - 20px);
            margin: 10px auto;
            background-color: #333;
            color: #fff;
            border: 2px solid #777;
            border-radius: 5px;
            padding: 5px;
        }

        #config-form input[type="submit"] {
            background-color: #007bff;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        #config-form input[type="submit"]:hover {
            background-color: #0056b3;

        }
    </style>
</head>

<body>
    <div class="container">
        <div style="display:flex; align-items: center;
            justify-content: center;">

            <img src="imgs/Logo.png" style="width: 30%;margin:0 auto;">
        </div>
        <h1>Bem vindos AngueraAdmin</h1>
        <ul class="button-container">
            <li>
                <a class="button" href="<?php echo "http://" . $config["Panel"]["Host"] . ":" . $config["Panel"]["Port"] . "/angueraAdmin.php" ?>">Entrar no SGBD</a>
            </li>
            <li>
                <!-- Adicionado um id ao link para poder selecioná-lo com JavaScript -->
                <a class="button" id="config-link">Configurar SGBD</a>
                <!-- Formulário para configurar -->
                <form id="config-form" method="POST">
                    <select name="theme" id="theme">
                        <?php foreach ($temas as $tema) : ?>
                            <option value="<?php echo $tema; ?>"><?php echo $tema; ?></option>
                        <?php endforeach; ?>
                    </select>
                    <select name="lang" id="lang">
                        <option value="en">English</option>
                        <option value="pt">Português</option>
                    </select>
                    <textarea name="host" id="host"><?php echo $config['Panel']['Host']; ?></textarea>
                    <textarea name="port" id="port"><?php echo $config['Panel']['Port']; ?></textarea>
                    <textarea name="pass" id="pass"><?php echo $config['Panel']['Pass']; ?></textarea>
                    <textarea name="dir" id="dir"><?php echo $config['Panel']['Dir']; ?></textarea>
                    <input class="button" type="submit" value="Salvar">
                </form>
            </li>
        </ul>
    </div>

    <script>
        // Obtém o link de configuração e o formulário de configuração
        var configLink = document.getElementById("config-link");
        var configForm = document.getElementById("config-form");

        // Adiciona um ouvinte de eventos para o link de configuração
        configLink.addEventListener("click", function(event) {
            event.preventDefault(); // Impede o comportamento padrão do link
            configForm.style.display = "block"; // Exibe o formulário de configuração
        });
    </script>
</body>

</html>