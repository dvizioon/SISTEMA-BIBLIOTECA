<?php

$config = parse_ini_file("./config.ini", true);
?>


<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema</title>
</head>

<body>
    <h1> Bem vindos AngueraAdmin</h1>
    <ul>
        <li>
            <a href="<?php echo "http://" . $config["Panel"]["Host"] . ":" . $config["Panel"]["Port"] . "/angueraAdmin.php" ?>">Entrar no SGBD</a>
        </li>
        <li>
            <a href="">Configurar SGBD</a>
        </li>
    </ul>

</body>

</html>