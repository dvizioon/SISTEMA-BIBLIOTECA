Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Carregar a DLL do System.Data.SQLite
$diretorioDll = $PWD.Path
[Reflection.Assembly]::LoadFile("$diretorioDll\Packages\.NET\System.Data.SQLite.dll")

function CriarBancoDeDados {
    param(
        [string]$databaseName,
        [string]$databasePath,
        [string]$sqlScript
    )

    # Verifica se o arquivo do banco de dados ja existe
    $databaseExists = Test-Path "$databasePath\$databaseName"

    if (-not $databaseExists) {
        # Cria o diretório do banco de dados, se necessario
        if (-not (Test-Path $databasePath)) {
            New-Item -ItemType Directory -Path $databasePath -ErrorAction SilentlyContinue
        }

        # Cria o banco de dados SQLite
        $connectionString = "Data Source=$databasePath\$databaseName;Version=3;"
        $connection = New-Object System.Data.SQLite.SQLiteConnection($connectionString)
        $connection.Open()

        # Executa o script SQL fornecido
        $command = $connection.CreateCommand()
        $command.CommandText = $sqlScript
        $command.ExecuteNonQuery()

        [System.Windows.Forms.MessageBox]::Show("Banco de dados criado com sucesso", "Sucesso", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)


        Write-Host "Banco de dados criado com sucesso em: $databasePath\$databaseName"
        $connection.Close()
    }
    else {
        [System.Windows.Forms.MessageBox]::Show("Erro ao criar o banco de dados:`n Banco ja Existe", "Erro", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
    }
}


# Criar o formulario
$form = New-Object System.Windows.Forms.Form
$form.Text = "Ferramentas angueraBook"
$form.Size = New-Object System.Drawing.Size(440, 380)
$form.StartPosition = "CenterScreen"
$form.BackColor = "LightGray"
$form.FormBorderStyle = "FixedSingle"

# Criar um controle de tabulacao
$tabControl = New-Object System.Windows.Forms.TabControl
$tabControl.Size = New-Object System.Drawing.Size(400, 200)
$tabControl.Location = New-Object System.Drawing.Point(10, 10)
$tabControl.BackColor = "White"
$form.Controls.Add($tabControl)

# Criar a Tab1
$tab1 = New-Object System.Windows.Forms.TabPage
$tab1.Text = "Configuracao do Banco de Dados"
$tab1.BackColor = "White"
$tabControl.TabPages.Add($tab1)

# Elementos da Tab1
$label1 = New-Object System.Windows.Forms.Label
$label1.Text = "Nome do Banco de Dados:"
$label1.Size = New-Object System.Drawing.Size(200, 20)
$label1.Location = New-Object System.Drawing.Point(20, 20)
$label1.ForeColor = "Black"
$tab1.Controls.Add($label1)

$textBox1 = New-Object System.Windows.Forms.TextBox
$textBox1.Size = New-Object System.Drawing.Size(200, 20)
$textBox1.Location = New-Object System.Drawing.Point(20, 40)
$textBox1.Text = "angueraBook.sqlite" # Nome do banco de dados fixo
$textBox1.Enabled = $false # Impede a edicao do nome
$tab1.Controls.Add($textBox1)

$label2 = New-Object System.Windows.Forms.Label
$label2.Text = "Caminho do Banco de Dados:"
$label2.Size = New-Object System.Drawing.Size(200, 20)
$label2.Location = New-Object System.Drawing.Point(20, 70)
$label2.ForeColor = "Black"
$tab1.Controls.Add($label2)

$textBox2 = New-Object System.Windows.Forms.TextBox
$textBox2.Size = New-Object System.Drawing.Size(200, 20)
$textBox2.Text = "$diretorioDll\Packages\phpLiteAdmin"
$textBox2.Enabled = $false
$textBox2.Location = New-Object System.Drawing.Point(20, 90)
$textBox2.ForeColor = "Black"
$tab1.Controls.Add($textBox2)

$label2_table = New-Object System.Windows.Forms.Label
$label2_table.Text = "Tabelas do Banco"
$label2_table.Size = New-Object System.Drawing.Size(200, 15)
$label2_table.Location = New-Object System.Drawing.Point(250, 5)
$label2_table.ForeColor = "Black"
$tab1.Controls.Add($label2_table)

$textBox_table = New-Object System.Windows.Forms.TextBox
$textBox_table.Multiline = $true  
$textBox_table.ScrollBars = "Vertical"  
$textBox_table.Width = 150
$textBox_table.Height = 140
$textBox_table.Enabled = $false
$textBox_table.ForeColor = "Red"
$textBox_table.Location = New-Object System.Drawing.Point(230, 20)  
$textBox_table.Text = @"

-- Tabela Aluno
CREATE TABLE Aluno (
    ra INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20)
);

-- Tabela Livro
CREATE TABLE Livro (
    isbn VARCHAR(13) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    autor VARCHAR(100),
    paginas INT
);

-- Tabela Colaborador
CREATE TABLE Colaborador (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    cargo VARCHAR(100)
);

-- Tabela Empréstimo
CREATE TABLE Emprestimo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataEmprestimo DATE NOT NULL,
    dataDevolucao DATE,
    livroIsbn VARCHAR(13),
    colaboradorCpf VARCHAR(11),
    FOREIGN KEY (livroIsbn) REFERENCES Livro(isbn),
    FOREIGN KEY (colaboradorCpf) REFERENCES Colaborador(cpf)
);
"@

$tab1.Controls.Add($textBox_table)

$buttonCreate = New-Object System.Windows.Forms.Button
$buttonCreate.Text = "Criar Banco de Dados"
$buttonCreate.Size = New-Object System.Drawing.Size(150, 30)
$buttonCreate.Location = New-Object System.Drawing.Point(20, 130)
$buttonCreate.ForeColor = "White"
$buttonCreate.BackColor = "DarkSlateBlue"
$buttonCreate.Add_Click({
        $databaseName = $textBox1.Text
        $databasePath = $textBox2.Text
        $sqlScript = $textBox_table.Text

        CriarBancoDeDados -databaseName $databaseName -databasePath $databasePath -sqlScript $sqlScript
    })
$tab1.Controls.Add($buttonCreate)


# Criar a Tab2
$tab2 = New-Object System.Windows.Forms.TabPage
$tab2.Text = "Gerenciamento do Banco de Dados"
$tab2.BackColor = "White"
$tabControl.TabPages.Add($tab2)

# Elements for Tab2
$labelDelete = New-Object System.Windows.Forms.Label
$labelDelete.Text = "Excluir Banco de Dados:"
$labelDelete.Size = New-Object System.Drawing.Size(200, 20)
$labelDelete.Location = New-Object System.Drawing.Point(20, 20)
$labelDelete.ForeColor = "Black"
$tab2.Controls.Add($labelDelete)

$buttonDelete = New-Object System.Windows.Forms.Button
$buttonDelete.Text = "Excluir Banco de Dados"
$buttonDelete.Size = New-Object System.Drawing.Size(150, 30)
$buttonDelete.Location = New-Object System.Drawing.Point(20, 50)
$buttonDelete.ForeColor = "White"
$buttonDelete.BackColor = "DarkRed"
$buttonDelete.Add_Click({
        # Verifica se o banco de dados existe
        $databaseExists = Test-Path "./Packages/phpLiteAdmin/angueraBook.sqlite"

        if ($databaseExists) {
            # Exibe uma mensagem de confirmacao antes de deletar o banco de dados
            $result = [System.Windows.Forms.MessageBox]::Show("Tem certeza de que deseja deletar o banco de dados? Esta acao e irreversivel.", "Deletar Banco de Dados", [System.Windows.Forms.MessageBoxButtons]::YesNo, [System.Windows.Forms.MessageBoxIcon]::Question)

            if ($result -eq "Yes") {
                try {
                    # Remove o arquivo do banco de dados
                    Remove-Item -Path "./Packages/phpLiteAdmin/angueraBook.sqlite" -Force

                    Write-Host "O banco de dados foi deletado com sucesso!"
                    $textBoxLog.AppendText("`nO banco de dados foi deletado com sucesso!")
                }
                catch {
                    Write-Host "Erro ao deletar o banco de dados: $_"
                    $textBoxLog.AppendText("`nErro ao deletar o banco de dados: $_")
                }
            }
        }
        else {
            # Se o banco de dados nao existir, exibe uma mensagem de erro
            [System.Windows.Forms.MessageBox]::Show("O banco de dados nao existe.", "Erro", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
            $textBoxLog.AppendText("`nErro: O banco de dados nao existe.")
        }
    })


$tab2.Controls.Add($buttonDelete)

$buttonReset = New-Object System.Windows.Forms.Button
$buttonReset.Text = "Redefinir Todas as Tabelas"
$buttonReset.Size = New-Object System.Drawing.Size(150, 30)
$buttonReset.Location = New-Object System.Drawing.Point(20, 90)
$buttonReset.ForeColor = "White"
$buttonReset.BackColor = "DarkGreen"
$buttonReset.Add_Click({
        # Verifica se o banco de dados existe

        $databaseExists = Test-Path "./Packages/phpLiteAdmin/angueraBook.sqlite"
    
        if ($databaseExists) {
            # Exibe uma mensagem de confirmacao antes de redefinir as tabelas
            $result = [System.Windows.Forms.MessageBox]::Show("Tem certeza de que deseja redefinir todas as tabelas? Esta acao e irreversivel.", "Redefinir Todas as Tabelas", [System.Windows.Forms.MessageBoxButtons]::YesNo, [System.Windows.Forms.MessageBoxIcon]::Question)

            if ($result -eq "Yes") {
                try {
                    # Cria uma conexao com o banco de dados
                    $connectionString = "Data Source=./Packages/phpLiteAdmin/angueraBook.sqlite;Version=3;"
                    $connection = New-Object System.Data.SQLite.SQLiteConnection($connectionString)
                    $connection.Open()

                    # Define as consultas para limpar as tabelas
                    $queries = @(
                        "DROP TABLE IF EXISTS Aluno;",
                        "DROP TABLE IF EXISTS Livro;",
                        "DROP TABLE IF EXISTS Colaborador;",
                        "DROP TABLE IF EXISTS Emprestimo;",
                        "CREATE TABLE IF NOT EXISTS Aluno (ra INTEGER PRIMARY KEY, nome TEXT NOT NULL, email TEXT, telefone TEXT);",
                        "CREATE TABLE IF NOT EXISTS Livro (isbn TEXT PRIMARY KEY, nome TEXT NOT NULL, autor TEXT, paginas INTEGER);",
                        "CREATE TABLE IF NOT EXISTS Colaborador (cpf TEXT PRIMARY KEY, nome TEXT NOT NULL, email TEXT, cargo TEXT);",
                        "CREATE TABLE IF NOT EXISTS Emprestimo (id INTEGER PRIMARY KEY AUTOINCREMENT, dataEmprestimo DATE NOT NULL, dataDevolucao DATE, livroIsbn TEXT, colaboradorCpf TEXT, FOREIGN KEY (livroIsbn) REFERENCES Livro(isbn), FOREIGN KEY (colaboradorCpf) REFERENCES Colaborador(cpf));"
                    )

                    # Executa as consultas para limpar e recriar as tabelas
                    foreach ($query in $queries) {
                        $command = $connection.CreateCommand()
                        $command.CommandText = $query
                        $command.ExecuteNonQuery()
                    }
                    $connection.Close()

                    Write-Host "Todas as tabelas foram resetadas com sucesso!"
                    $textBoxLog.AppendText("`nTodas as tabelas foram resetadas com sucesso!")
                }
                catch {
                    Write-Host "Erro ao resetar as tabelas: $_"
                    $textBoxLog.AppendText("`nErro ao resetar as tabelas: $_")
                }
                finally {
                    $connection.Close()
                }
            }
        }
        else {
            # Se o banco de dados nao existir, exibe uma mensagem de erro
            [System.Windows.Forms.MessageBox]::Show("O banco de dados nao existe.", "Erro", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
            $textBoxLog.AppendText("`nErro: O banco de dados nao existe.")
        }
    })
$tab2.Controls.Add($buttonReset)

# TextBox for Logs
$textBoxLog = New-Object System.Windows.Forms.TextBox
$textBoxLog.Multiline = $true  
$textBoxLog.ScrollBars = "Vertical"  
$textBoxLog.Width = 180
$textBoxLog.Height = 140
$textBoxLog.Location = New-Object System.Drawing.Point(200, 20)  
$tab2.Controls.Add($textBoxLog)


# Exibir o formulario
$form.ShowDialog() | Out-Null
