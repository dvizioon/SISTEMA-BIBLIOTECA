Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Carregar a DLL do System.Data.SQLite
$diretorioPadrao = "."
$diretorioDll = if ($PWD -ne $null) { $PWD.Path } else { $diretorioPadrao }

[Reflection.Assembly]::LoadFile("$diretorioDll\Packages\.NET\System.Data.SQLite.dll")

# Criar o formulario
$form = New-Object System.Windows.Forms.Form
$form.Text = "Criar Banco de Dados e Tabelas"
$form.Size = New-Object System.Drawing.Size(415, 360)
$form.StartPosition = "CenterScreen"
$form.BackColor = "LightGray"
$form.FormBorderStyle = "FixedSingle"

# Criar um controle de tabulacao
$tabControl = New-Object System.Windows.Forms.TabControl
$tabControl.Size = New-Object System.Drawing.Size(380, 300)
$tabControl.Location = New-Object System.Drawing.Point(10, 10)
$tabControl.BackColor = "White"
$form.Controls.Add($tabControl)

# Criar a Tab1
$tab1 = New-Object System.Windows.Forms.TabPage
$tab1.Text = "Criar Banco de Dados e Tabelas"
$tab1.BackColor = "White"
$tabControl.TabPages.Add($tab1)

# Elementos da Tab1
$label1 = New-Object System.Windows.Forms.Label
$label1.Text = "Nome do Banco de Dados:"
$label1.Size = New-Object System.Drawing.Size(200, 20)
$label1.Location = New-Object System.Drawing.Point(20, 20)
$tab1.Controls.Add($label1)

$textBox1 = New-Object System.Windows.Forms.TextBox
$textBox1.Size = New-Object System.Drawing.Size(200, 20)
$textBox1.Location = New-Object System.Drawing.Point(20, 40)
$textBox1.Text = "angueraBook.sqlite" # Nome do banco de dados fixo
$textBox1.ReadOnly = $true
$tab1.Controls.Add($textBox1)

$label2 = New-Object System.Windows.Forms.Label
$label2.Text = "Diretorio do Banco de Dados:"
$label2.Size = New-Object System.Drawing.Size(200, 20)
$label2.Location = New-Object System.Drawing.Point(20, 70)
$tab1.Controls.Add($label2)

$textBox2 = New-Object System.Windows.Forms.TextBox
$textBox2.Size = New-Object System.Drawing.Size(200, 20)
$textBox2.Location = New-Object System.Drawing.Point(20, 90)
$textBox2.Text = "$diretorioDll\Packages\phpLiteAdmin" 
$textBox2.ReadOnly = $true
$tab1.Controls.Add($textBox2)

$buttonCreateDB = New-Object System.Windows.Forms.Button
$buttonCreateDB.Text = "Criar Banco de Dados e Tabelas"
$buttonCreateDB.Size = New-Object System.Drawing.Size(200, 30)
$buttonCreateDB.Location = New-Object System.Drawing.Point(20, 130)
$buttonCreateDB.Add_Click({
        CriarBancoETabelas -databaseName $textBox1.Text -databaseDirectory $textBox2.Text
    })
$tab1.Controls.Add($buttonCreateDB)

# Criar as tabelas no script SQL
$scriptSQL = @"
CREATE TABLE IF NOT EXISTS Aluno (
    ra INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Livro (
    isbn VARCHAR(13) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    autor VARCHAR(100),
    paginas INT
);

CREATE TABLE IF NOT EXISTS Colaborador (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    cargo VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Emprestimo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataEmprestimo DATE NOT NULL,
    dataDevolucao DATE,
    livroIsbn VARCHAR(13),
    colaboradorCpf VARCHAR(11),
    FOREIGN KEY (livroIsbn) REFERENCES Livro(isbn),
    FOREIGN KEY (colaboradorCpf) REFERENCES Colaborador(cpf)
);
"@

# Criar a Tab2
$tab2 = New-Object System.Windows.Forms.TabPage
$tab2.Text = "Script SQL"
$tab2.BackColor = "White"
$tabControl.TabPages.Add($tab2)

# Elementos da Tab2
$textBoxScript = New-Object System.Windows.Forms.TextBox
$textBoxScript.Size = New-Object System.Drawing.Size(340, 120)
$textBoxScript.Multiline = $true
$textBoxScript.ReadOnly = $true
$textBoxScript.ScrollBars = "Vertical"
$textBoxScript.Location = New-Object System.Drawing.Point(20, 20)
$textBoxScript.Text = $scriptSQL
$tab2.Controls.Add($textBoxScript)

# $buttonExecuteScript = New-Object System.Windows.Forms.Button
# $buttonExecuteScript.Text = "Executar Script SQL"
# $buttonExecuteScript.Size = New-Object System.Drawing.Size(200, 30)
# $buttonExecuteScript.Location = New-Object System.Drawing.Point(20, 160)
# $buttonExecuteScript.Add_Click({
        
#     })
# $tab2.Controls.Add($buttonExecuteScript)


function CriarBancoETabelas {
    param(
        [string]$databaseName,
        [string]$databaseDirectory
    )

    # Verifica se o banco de dados ja existe
    $databasePath = Join-Path -Path $databaseDirectory -ChildPath $databaseName
    if (Test-Path $databasePath -PathType Leaf) {
        [System.Windows.Forms.MessageBox]::Show("O banco de dados ja existe.", "Aviso", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Warning)
        return
    }

    $script = $textBoxScript.Text
    if (-not [string]::IsNullOrWhiteSpace($script)) {
        try {
            # Cria a conexao com o banco de dados
            $connectionString = "Data Source=$databasePath;Version=3;"
            $connection = New-Object System.Data.SQLite.SQLiteConnection($connectionString)
            $connection.Open()

            # Executa o script SQL
            $command = $connection.CreateCommand()
            $command.CommandText = $script
            $command.ExecuteNonQuery()

            # Fecha a conexao
            $connection.Close()

            [System.Windows.Forms.MessageBox]::Show("Script SQL executado com sucesso", "Sucesso", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
        }
        catch {
            [System.Windows.Forms.MessageBox]::Show("Erro ao executar o script SQL: $_", "Erro", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
        }
    }
    else {
        [System.Windows.Forms.MessageBox]::Show("Por favor, insira um script SQL válido", "Erro", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
    }
}



# Exibir o formulario
$form.ShowDialog() | Out-Null
