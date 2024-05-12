<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bem-vindo à AnguerBook</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f3f3f3;
            margin: 0;
            padding: 0;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100vw;
            height: 100vh;
        }

        .container {
            width: 600px;
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            font-size: 32px;
            margin-bottom: 20px;
            color: #333;
            text-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
        }

        p {
            font-size: 18px;
            margin-bottom: 20px;
            color: #555;
        }

        a {
            color: #ff4500;
            text-decoration: none;
            font-weight: bold;
            border-bottom: 1px solid #ff4500;
            transition: border-bottom 0.3s ease;
        }

        a:hover {
            border-bottom: 2px solid #ff4500;
        }

        .img {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .img img {
            width: 40%;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="img">
            <img src="./Logo.png" />
        </div>
        <h1>Bem-vindo à AnguerBook</h1>
        <p>Para começar a usar nossos serviços, você precisa criar uma conta de administrador.</p>
        <p>Crie sua conta de administrador <a href="criarUsuario.php">aqui</a>.</p>
    </div>
</body>

</html>