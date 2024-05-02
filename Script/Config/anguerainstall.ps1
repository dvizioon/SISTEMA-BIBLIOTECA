
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing



$form = New-Object System.Windows.Forms.Form
$form.Text = "Painel angueraBooks"
$form.Size = New-Object System.Drawing.Size(440, 380)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedSingle"


$tabControl = New-Object System.Windows.Forms.TabControl
$tabControl.Size = New-Object System.Drawing.Size(400, 330)
$tabControl.Location = New-Object System.Drawing.Point(10, 10)
$form.Controls.Add($tabControl)


$tab1 = New-Object System.Windows.Forms.TabPage
$tab1.Text = "Instalador 1.0"
$tabControl.Controls.Add($tab1)


$labelPhpVersion = New-Object System.Windows.Forms.Label
$labelPhpVersion.Text = "PHP --version [5.4]"
$labelPhpVersion.AutoSize = $true
$labelPhpVersion.Location = New-Object System.Drawing.Point(20, 20)
$tab1.Controls.Add($labelPhpVersion)


$caminhoPrincipal = "./Packages"
$nomeDiretorio = "php5.4.0"
$caminhoSubdiretorio = Join-Path -Path $caminhoPrincipal -ChildPath $nomeDiretorio

if (Test-Path -Path $caminhoSubdiretorio -PathType Container) {
    Write-Host "Diretorio '$nomeDiretorio' encontrado."
    $logMessage = "Diretorio '$nomeDiretorio' encontrado."
    $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessage))
}
else {
    [System.Windows.Forms.MessageBox]::Show("Versao do PHP nao encontrada.")
    $form.Close()
}

$inputPhpVersion = New-Object System.Windows.Forms.TextBox
$inputPhpVersion.Text = $nomeDiretorio
$inputPhpVersion.Location = New-Object System.Drawing.Point(150, 20)
$inputPhpVersion.Size = New-Object System.Drawing.Size(300, 20)
$inputPhpVersion.Enabled = $false
$tab1.Controls.Add($inputPhpVersion)


function FecharFormulario {
    $form.Close()
}
$buttonFechar = New-Object System.Windows.Forms.Button
$buttonFechar.Text = "Fechar"
$buttonFechar.Size = New-Object System.Drawing.Size(200, 30)
$buttonFechar.Location = New-Object System.Drawing.Point(170, 260)
$buttonFechar.BackColor = [System.Drawing.Color]::Red
$buttonFechar.ForeColor = [System.Drawing.Color]::White

$buttonFechar.Visible = $false
$buttonFechar.Add_Click({
        FecharFormulario
    })

$tab1.Controls.Add($buttonFechar)

$buttonStartConfiguration = New-Object System.Windows.Forms.Button
$buttonStartConfiguration.Text = "Iniciar Instalacao"
$buttonStartConfiguration.Size = New-Object System.Drawing.Size(200, 30)
$buttonStartConfiguration.Location = New-Object System.Drawing.Point(20, 50)
$tab1.Controls.Add($buttonStartConfiguration)



$buttonStartConfiguration.Add_Click({
        $unidade = $env:SystemDrive
        $pasta = "VersionPHP"  
        $caminhoPasta = Join-Path -Path $unidade -ChildPath $pasta

        if (-not (Test-Path $caminhoPasta)) {
            # Se a pasta não existir, crie-a
            New-Item -ItemType Directory -Path $caminhoPasta -Force
            $logMessage = "Pasta '$pasta' criada em $unidade."
        }
        else {
            # Se a pasta Ja existir, peça confirmacao para reinstalá-la
            $confirmacao = [System.Windows.Forms.MessageBox]::Show("A pasta '$pasta' Ja existe. Deseja reinstala-la?", "Confirmacao", "YesNo", "Question")

            if ($confirmacao -eq "Yes") {
                # Se o usuário confirmar, remova a pasta e crie uma nova
                Remove-Item -Path $caminhoPasta -Recurse -Force
                New-Item -ItemType Directory -Path $caminhoPasta -Force
                $logMessage = "Pasta '$pasta' reinstalada em $unidade."
            }
            else {
                # Se o usuário optar por não reinstalar, apenas informe que a pasta Ja existe
                $logMessage = "A pasta '$pasta' Ja existe em $unidade."
            }
        }

        # Adiciona o log ao textarea
        $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessage))
        $valor_destino = "php5.4.0" 
        # Copia todos os arquivos e subdiretórios da pasta de origem para a pasta de destino
        $caminhoOrigem = "./Packages/$valor_destino"  # Defina o caminho da pasta de origem
        $caminhoDestino = Join-Path -Path $caminhoPasta -ChildPath "$valor_destino"  # Cria o caminho da pasta de destino

        # Verifica se a pasta de origem existe
        if (Test-Path $caminhoOrigem -PathType Container) {
            # Copia todos os arquivos e subdiretórios da pasta de origem para a pasta de destino
            Copy-Item -Path $caminhoOrigem -Destination $caminhoDestino -Recurse -Force
        
            # Obtém a lista de arquivos da pasta de origem
            $arquivos = Get-ChildItem -Path $caminhoOrigem -File

            # Para cada arquivo na lista, copie-o para o destino
            foreach ($arquivo in $arquivos) {
                # Copia o arquivo para o destino
                Copy-Item -Path $arquivo.FullName -Destination $caminhoDestino -Force
        
                # Adiciona uma mensagem ao log
                $logMessageArquivo = "Arquivo '$($arquivo.Name)' copiado para '$caminhoDestino'."
                $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessageArquivo))
            }

            # Define o nome da variável de ambiente
            $variavelAmbiente = "PHP_VERSION"

            if (-not ([System.Environment]::GetEnvironmentVariable($variavelAmbiente, [System.EnvironmentVariableTarget]::User))) {
                $valorVariavel = "$caminhoPasta\$valor_destino"
                [System.Environment]::SetEnvironmentVariable($variavelAmbiente, $valorVariavel, [System.EnvironmentVariableTarget]::User)
                $pathAtual = [System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::User)
                $pathAtual += ";%PHP_VERSION%"
                [System.Environment]::SetEnvironmentVariable("PATH", $pathAtual, [System.EnvironmentVariableTarget]::User)
                
            }
            else {
                $logMessage = "PHP_VERSION Ja Encontrada ..."
                $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessage))
            }
            $buttonFechar.Visible = $true
            $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", "Sucesso Finalizado Configuracao..."))
        }
        else {
            # Se a pasta de origem não existir, exibe uma mensagem de erro
            [System.Windows.Forms.MessageBox]::Show("A pasta de origem não foi encontrada.", "Erro", "OK", "Error")
        }
    })

$textAreaLogs = New-Object System.Windows.Forms.TextBox
$textAreaLogs.Multiline = $true
$textAreaLogs.ScrollBars = "Vertical"
$textAreaLogs.Location = New-Object System.Drawing.Point(20, 100)
$textAreaLogs.Size = New-Object System.Drawing.Size(350, 150)
$tab1.Controls.Add($textAreaLogs)

# Cria a aba para configuração do banco de dados
$tab2 = New-Object System.Windows.Forms.TabPage
$tab2.Text = "Config INI"
$tabControl.Controls.Add($tab2)

# Criar ComboBox
$comboBox = New-Object System.Windows.Forms.ComboBox
$comboBox.Location = New-Object System.Drawing.Point(20, 60)
$comboBox.Size = New-Object System.Drawing.Size(170, 50)
$comboBox.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold) 

$comboBox.Items.Add("AlternateBlue")
$comboBox.Items.Add("Bootstrap")
$comboBox.Items.Add("Default")
$comboBox.Items.Add("dynamic_myAdmin")
$comboBox.Items.Add("Dynamic")
$comboBox.Items.Add("MiamiNights")
$comboBox.Items.Add("Modern")
$comboBox.Items.Add("pitchGray")
$comboBox.Items.Add("PlasticDream")
$comboBox.Items.Add("PlasticNightmare")
$comboBox.Items.Add("Retro")
$comboBox.Items.Add("Shadow")
$comboBox.Items.Add("Sheep")
$comboBox.Items.Add("simpleGray")
$comboBox.Items.Add("SoftieBlue")
$comboBox.Items.Add("Ugur3d")


$caminhoArquivo_iniSelect = "config.ini"
if (Test-Path $caminhoArquivo_iniSelect -PathType Leaf) {
    $conteudoArquivo = Get-Content -Path $caminhoArquivo_iniSelect

    # Procura pela linha que contém o tema
    foreach ($linha in $conteudoArquivo) {
        if ($linha -match '^Theme\s*=\s*(.*)') {
            $temaAtual = $matches[1].Trim()
            $comboBox.SelectedItem = $temaAtual 
            break 
        }
    }
}
else {
    Write-Host "Arquivo não encontrado: $caminhoArquivo_iniSelect"
    $temaAtual = "Retro"
}



# Define o evento de seleção do ComboBox
$comboBox.Add_SelectedIndexChanged({
        $temaSelecionado = $comboBox.SelectedItem
        $caminhoArquivo = "config.ini"
        $conteudoArquivo = CarregarOuCriarArquivo -caminhoCompleto $caminhoArquivo
        $conteudoArquivoAtualizado = $conteudoArquivo -replace "Theme = .+", "Theme = $temaSelecionado"
        $conteudoArquivoAtualizado | Out-File -FilePath $caminhoArquivo -Force
        $textBoxConfig.Clear()
        $conteudoArquivoFormatado = @"
[Panel]
Theme = $temaSelecionado
Lang  = en
Host  = localhost
Port  = 8000
Pass  = admin
Dir   = .
"@
        # Cria o arquivo com o conteúdo padrão
        $conteudoArquivoFormatado
       
        $textBoxConfig.AppendText($conteudoArquivoFormatado)
    })
$tab2.Controls.Add($comboBox)


# Define a função para carregar ou criar um arquivo de configuração
function CarregarOuCriarArquivo {
    param(
        [string]$caminhoCompleto
    )

    # Verifica se o arquivo existe
    if (Test-Path $caminhoCompleto -PathType Leaf) {
        # Lê o conteúdo do arquivo
        $conteudoArquivo = Get-Content -Path $caminhoCompleto

        # Separa a primeira linha (com o nome do painel) e as configurações restantes
        $panel = $conteudoArquivo[0]
        $configuracoes = $conteudoArquivo[1..($conteudoArquivo.Length - 1)]

        # Formata as configurações do arquivo para exibir as chaves e valores em linhas separadas
        $conteudoArquivoFormatado = $panel + "`r`n" + ($configuracoes -join "`r`n")
    }
    else {
        # Se o arquivo não existir, cria o conteúdo padrão
        $conteudoArquivoFormatado = @"
[Panel]
Theme = Retro
Lang  = en
Host  = localhost
Port  = 8000
Pass  = admin
Dir   = .
"@
        # Cria o arquivo com o conteúdo padrão
        $conteudoArquivoFormatado | Out-File -FilePath $caminhoCompleto
    }

    return $conteudoArquivoFormatado
}


# Define a função para salvar as configurações no arquivo
function SalvarConfiguracoes {
    param(
        [string]$caminhoCompleto,
        [string]$novoConteudo
    )
    [System.Windows.Forms.MessageBox]::Show("Arquivo Atualizado com Sucesso...")
    # Escreve o novo conteúdo no arquivo
    $novoConteudo | Set-Content -Path $caminhoCompleto
}

function ReseteConfiguracoes {
    param(
        [string]$caminhoCompleto

    )
    $conteudoArquivoFormatado = @"
[Panel]
Theme = Retro
Lang  = en
Host  = localhost
Port  = 8000
Pass  = admin
Dir   = .
"@
    $textBoxConfig.Text = $conteudoArquivoFormatado 
    [System.Windows.Forms.MessageBox]::Show("Arquivo Resetado com Sucesso...")
    # Escreve o novo conteúdo no arquivo
    $conteudoArquivoFormatado | Set-Content -Path $caminhoCompleto
}


$caminhoArquivo = "config.ini"

$textoArquivo = CarregarOuCriarArquivo -caminhoCompleto $caminhoArquivo

# TextArea para as configurações
$textBoxConfig = New-Object System.Windows.Forms.TextBox
$textBoxConfig.Multiline = $true
$textBoxConfig.Text = $textoArquivo
$textBoxConfig.ScrollBars = "Vertical"
$textBoxConfig.Location = New-Object System.Drawing.Point(20, 100)
$textBoxConfig.Size = New-Object System.Drawing.Size(350, 150)

# Define a fonte e a cor do texto
$fonte = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Regular)
$textBoxConfig.Font = $fonte
$textBoxConfig.ForeColor = [System.Drawing.Color]::Black

$tab2.Controls.Add($textBoxConfig)
# Botão de Reset
$buttonReset = New-Object System.Windows.Forms.Button
$buttonReset.Location = New-Object System.Drawing.Point(20, 20)
$buttonReset.Size = New-Object System.Drawing.Size(100, 30)
$buttonReset.Text = "Reset"
$tab2.Controls.Add($buttonReset)

# Botão de Salvar
$buttonSave = New-Object System.Windows.Forms.Button
$buttonSave.Location = New-Object System.Drawing.Point(140, 20)
$buttonSave.Size = New-Object System.Drawing.Size(100, 30)
$buttonSave.Text = "Save"
$tab2.Controls.Add($buttonSave)

# Ação do botão Reset
$buttonReset.Add_Click({
        ReseteConfiguracoes -caminhoCompleto $caminhoArquivo
    })

# Ação do botão Save
$buttonSave.Add_Click({
        SalvarConfiguracoes -caminhoCompleto $caminhoArquivo -novoConteudo $textBoxConfig.Text
    })

function LerVariavelDoArquivoIni {
    param (
        [string]$caminhoCompleto,
        [string]$variavelDesejada
    )

    # Define uma variável para armazenar o valor da variável desejada
    $valorVariavel = ""

    # Verifica se o arquivo existe
    if (Test-Path $caminhoCompleto -PathType Leaf) {
        # Lê o conteúdo do arquivo
        $linhas = Get-Content -Path $caminhoCompleto

        # Loop pelas linhas do arquivo
        foreach ($linha in $linhas) {
            # Verifica se a linha contém a variável desejada
            if ($linha -match "^\s*$variavelDesejada\s*=\s*(.*)\s*$") {
                $valorVariavel = $matches[1]
                break  # Se encontrarmos a variável desejada, podemos parar de percorrer o arquivo
            }
        }
    }
    else {
        Write-Host "O arquivo não foi encontrado no caminho especificado."
    }

    return $valorVariavel
}

# Caminho para o arquivo INI
$caminhoArquivoIni = "config.ini"

$_Host = LerVariavelDoArquivoIni -caminhoCompleto $caminhoArquivoIni -variavelDesejada "Host"
$_Port = LerVariavelDoArquivoIni -caminhoCompleto $caminhoArquivoIni -variavelDesejada "Port"


# Criando a aba "Test Servidor"
$tab3 = New-Object System.Windows.Forms.TabPage
$tab3.Text = "Teste AngueraBookAdmin"
$tabControl.Controls.Add($tab3)

# Adicionando os elementos à aba "Test Servidor"
# Input 1
$hots_input = New-Object System.Windows.Forms.TextBox
$hots_input.Location = New-Object System.Drawing.Point(20, 20)
$hots_input.Enabled = $false
$hots_input.Text = $_Host
$hots_input.Size = New-Object System.Drawing.Size(200, 20)
$tab3.Controls.Add($hots_input)

# Input 2
$port_input = New-Object System.Windows.Forms.TextBox
$port_input.Location = New-Object System.Drawing.Point(20, 50)
$port_input.Enabled = $false
$port_input.Text = $_Port
$port_input.Size = New-Object System.Drawing.Size(200, 20)
$tab3.Controls.Add($port_input)

# Botão
$button_iniciar = New-Object System.Windows.Forms.Button
$button_iniciar.Location = New-Object System.Drawing.Point(20, 80)
$button_iniciar.Size = New-Object System.Drawing.Size(150, 23)
$button_iniciar.Text = "Iniciar PHP Server"
$tab3.Controls.Add($button_iniciar)

$button_stop = New-Object System.Windows.Forms.Button
$button_stop.Location = New-Object System.Drawing.Point(200, 80)
$button_stop.Size = New-Object System.Drawing.Size(150, 23)
$button_stop.Text = "Para Server"
$tab3.Controls.Add($button_stop)


# TextArea
$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Multiline = $true
$textBox.ScrollBars = "Vertical"
$textBox.Location = New-Object System.Drawing.Point(20, 110)
$textBox.Size = New-Object System.Drawing.Size(350, 150)
$tab3.Controls.Add($textBox)

# Evento de clique do botão
$button_iniciar.Add_Click({
        # Define o comando a ser executado
        $comando = "cd ./Packages && cd phpLiteAdmin && php_5.exe -S $($_Host):$($_Port)"

        # Cria um processo para executar o comando e redireciona a saída padrão
        $processo = Start-Process -FilePath "cmd.exe" -ArgumentList "/c $comando" -NoNewWindow -PassThru

        # Se o processo foi iniciado com sucesso
        if ($processo) {
            $textBox.AppendText("O PHP Server foi iniciado com sucesso." + [Environment]::NewLine)
            $textBox.AppendText("Iniciando Teste ..." + [Environment]::NewLine)
            # URL a ser aberta

            # Função para ler a saída do processo e exibir na caixa de texto
            $leituraProcesso = {
                param($processo, $textBox)

                while (!$processo.HasExited) {
                    $linha = $processo.StandardOutput.ReadLine()
                    if ($linha -ne $null) {
                        $textBox.BeginInvoke([Action[string]] { param($line) $textBox.AppendText($line + [Environment]::NewLine) }, $linha) | Out-Null
                    }
                    Start-Sleep -Milliseconds 100  # Aguarda um curto período para evitar bloqueios
                }
            }

            # Inicia a leitura da saída do processo em segundo plano
            Start-Job -ScriptBlock $leituraProcesso -ArgumentList $processo, $textBox

            Start-Sleep -Seconds 3
            $url = "http://$($_Host):$($_Port)/angueraAdmin.php"
            Start-Process $url
        }
        else {
            # Se ocorreu um erro ao iniciar o processo
            $textBox.AppendText("Erro ao iniciar o PHP Server." + [Environment]::NewLine)
        }
    })


# Evento de clique do botão de parar
$button_stop.Add_Click({
        # Verifica se o processo foi criado
        if ($processo) {
            # Encerra o processo
            $processo.Kill()
        
            # Adiciona uma mensagem na caixa de texto
            $textBox.AppendText("Processo interrompido." + [Environment]::NewLine)
        }
        else {
            # Se o processo não foi criado, exibe uma mensagem de erro
            $textBox.AppendText("Nenhum processo em execução para interromper." + [Environment]::NewLine)
        }
    })





$form.ShowDialog() | Out-Null

