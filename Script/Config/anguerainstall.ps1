
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$diretorioPai = $PWD.Path
$diretorioDll = $PWD.Path
$diretorioPadrao = "."
$diretorioDll = if ($PWD -ne $null) { $PWD.Path } else { $diretorioPadrao }

function CriarLogs {

    param (
        [string]$caminhoLog,
        [string[]]$logs  # Aceita um array de strings para múltiplos logs
    )

    if (-not (Test-Path $caminhoLog)) {
        New-Item -ItemType Directory -Force -Path (Split-Path $caminhoLog)
        New-Item -ItemType File -Force -Path $caminhoLog
    }

    # Adiciona cada log em uma nova linha no arquivo
    $logs | ForEach-Object {
        $_ | Out-File -FilePath $caminhoLog -Encoding ASCII -Append
    }

    return "Sucesso: Logs carregados."
}


function CarregarLogs {

    param (
        [string]$caminhoLog
    )

    if (-not (Test-Path $caminhoLog)) {
        New-Item -ItemType Directory -Force -Path (Split-Path $caminhoLog)
        New-Item -ItemType File -Force -Path $caminhoLog
    }

    return Get-Content -Path $caminhoLog
}



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
$labelPhpVersion.Text = "PHP -> [5.4]"
$labelPhpVersion.AutoSize = $true
$labelPhpVersion.Location = New-Object System.Drawing.Point(20, 20)
$tab1.Controls.Add($labelPhpVersion)

$comboBox = New-Object System.Windows.Forms.ComboBox
$comboBox.Location = New-Object System.Drawing.Point(100, 15)
$comboBox.Size = New-Object System.Drawing.Size(100, 50)
$comboBox.Font = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold) 

$comboBox.Items.Add("php5.4.0.zip")
$comboBox.Text = "Versoes..."


Write-Host $diretorioPai
$caminhoPrincipal = "$diretorioPai\Packages\Import"
$nomeDiretorio = "php5.4.0.zip"
$caminhoSubdiretorio = Join-Path -Path $caminhoPrincipal -ChildPath $nomeDiretorio

if (Test-Path -Path $caminhoSubdiretorio) {
    Write-Host "Arquivo '$nomeDiretorio' encontrado."
    $logMessage = "Arquivo '$nomeDiretorio' encontrado."
    $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessage))
}
else {
    [System.Windows.Forms.MessageBox]::Show("Versao do PHP nao encontrada.")
    $form.Close()
}


$inputPhpVersion = New-Object System.Windows.Forms.TextBox
$inputPhpVersion.Text = $nomeDiretorio
$inputPhpVersion.Location = New-Object System.Drawing.Point(220, 15)
$inputPhpVersion.Size = New-Object System.Drawing.Size(150, 23)
$inputPhpVersion.Multiline = $true
$inputPhpVersion.Enabled = $false
$tab1.Controls.Add($inputPhpVersion)
$tab1.Controls.Add($comboBox)


function FecharFormulario {
    $pid_Painel = CarregarLogs -caminhoLog "$diretorioPai\Keys\Pid_PS1.txt"
    Write-Host $pid_Painel
    $processoPID = $pid_Painel
    if ($processoPID -ne "") {
        try {
            $processoParaEncerrar = Get-Process -Id $processoPID -ErrorAction Stop
            if ($processoParaEncerrar) {
                $processoParaEncerrar.Kill()
                $textAreaLogs.AppendText("Processo com PID $processoPID encerrado com sucesso." + [Environment]::NewLine)
                $textAreaLogs.AppendText("Fechando Janela..." + [Environment]::NewLine)
                Start-Sleep -Milliseconds 500
                $form.Close()
            }
            else {
                $textBox.AppendText("Nenhum processo encontrado com o PID $processoPID." + [Environment]::NewLine)
            }
        }
        catch {
            $textBox.AppendText("Erro ao encerrar o processo com PID $processoPID." + [Environment]::NewLine)
        }
    }
    else {
        $textBox.AppendText("Nenhum PID fornecido para encerrar o processo." + [Environment]::NewLine)
    }
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

function criarPastaExtrairZip {
    param (
        [string]$valor_destino,
        [string]$caminhoOrigemZip,
        [string]$caminhoDestino
    )

    # Verifica se o arquivo ZIP de origem existe
    if (Test-Path $caminhoOrigemZip -PathType Leaf) {
        $textAreaLogs.Clear()
        $textAreaLogs.ForeColor = "Green"

        # Extrai o conteúdo do arquivo ZIP diretamente na pasta de destino
        Expand-Archive -Path $caminhoOrigemZip -DestinationPath $caminhoDestino -Force

        # Adiciona uma mensagem ao log
        $logMessageArquivo = "Arquivo '$valor_destino.zip' extraido para '$caminhoDestino'."
        $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessageArquivo))
        $labelPhpWindows.Text = "PHP - Instalando"
        $labelPhpWindows.ForeColor = "Orange"

        $labelPhpWindows.Text = "Reiniciar ..."
        $labelPhpWindows.ForeColor = "Green"

        $tabControl.TabPages.Remove($tab2)
        $tabControl.TabPages.Remove($tab3)
        $tabControl.TabPages.Remove($tab4)
        CriarLogs -caminhoLog "$diretorioDll\Logs\Log_INS.log" -logs ""
        CriarLogs -caminhoLog "$diretorioDll\Logs\Log_INS.log" -logs $textAreaLogs.Text

        # Adiciona o caminho diretamente ao PATH se nao estiver presente
        if (-not ([System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::User) -like "*$caminhoPasta\$valor_destino*")) {
            $pathAtual = [System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::User)
            $pathAtual += ";$caminhoPasta\$valor_destino"
            [System.Environment]::SetEnvironmentVariable("PATH", $pathAtual, [System.EnvironmentVariableTarget]::User)
        }
        else {
            $logMessage = "O caminho ja esta no PATH."
            $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessage))
        }

        $buttonFechar.Visible = $true
        $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", "Sucesso Finalizado Configuracao"))
    }
    else {
        # Se o arquivo ZIP de origem nao existir, exibir uma mensagem de erro
        [System.Windows.Forms.MessageBox]::Show("O arquivo ZIP de origem nao foi encontrado.", "Erro", "OK", "Error")
    }
    
}



$buttonStartConfiguration.Add_Click({
        $unidade = $env:SystemDrive
        $pasta = "VersionPHP"
        
        $caminhoPasta = Join-Path -Path $unidade -ChildPath $pasta

        # Verificar se a pasta de destino ja existe
        if (-not (Test-Path $caminhoPasta)) {
            # Se a pasta nao existir, crie-a
            New-Item -ItemType Directory -Path $caminhoPasta -Force
            $logMessage = "Pasta '$pasta' criada em $unidade."

            $valor_destino = "php5.4.0" 
            $caminhoOrigemZip = "$diretorioPai\Packages\Import\$valor_destino.zip"  # Defina o caminho do arquivo ZIP de origem
            $caminhoDestino = $caminhoPasta  # Cria o caminho da pasta de destino

            criarPastaExtrairZip -valor_destino $valor_destino -caminhoOrigemZip $caminhoOrigemZip -caminhoDestino $caminhoDestino

        }
        else {
            # Se a pasta ja existir, peca confirmacao para reinstala-la
            $confirmacao = [System.Windows.Forms.MessageBox]::Show("A pasta '$pasta' ja existe. Deseja reinstala-la?", "Confirmacao", "YesNo", "Question")

            if ($confirmacao -eq "Yes") {
                # Se o usuario confirmar, remova a pasta e crie uma nova
                Remove-Item -Path $caminhoPasta -Recurse -Force
                New-Item -ItemType Directory -Path $caminhoPasta -Force
                $logMessage = "Pasta '$pasta' reinstalada em $unidade."
                $reinstalar = $true
            }
            else {
                # Se o usuario optar por nao reinstalar, apenas informe que a pasta ja existe
                $logMessage = "A pasta '$pasta' ja existe em $unidade."
                $reinstalar = $false
            }
        }

        # Adiciona o log ao textarea
        $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessage))

        if ($reinstalar) {
            $valor_destino = "php5.4.0" 
            $caminhoOrigemZip = "$diretorioPai\Packages\Import\$valor_destino.zip"  # Defina o caminho do arquivo ZIP de origem
            $caminhoDestino = $caminhoPasta  # Cria o caminho da pasta de destino

            criarPastaExtrairZip -valor_destino $valor_destino -caminhoOrigemZip $caminhoOrigemZip -caminhoDestino $caminhoDestino

            
        }

    })


$textAreaLogs = New-Object System.Windows.Forms.TextBox
$textAreaLogs.Multiline = $true
$textAreaLogs.ScrollBars = "Vertical"
$textAreaLogs.Location = New-Object System.Drawing.Point(20, 100)
$textAreaLogs.Size = New-Object System.Drawing.Size(350, 150)
$tab1.Controls.Add($textAreaLogs)

function VerificaPasta {
    param (
        [string]$caminho,
        [string]$nome
    )

    $caminhoPasta = Join-Path -Path $caminho -ChildPath $nome

    if (-not (Test-Path $caminhoPasta)) {
        return $false
    }
    else {
        return $true
    }
    
}

$pastaVersion = VerificaPasta -caminho $env:SystemDrive -nome "VersionPHP"
Write-Host $pastaVersion

if ($pastaVersion -eq $true) {
    $textAreaLogs.ForeColor = "Green"
    $logMessage = " Configuracao feita com Sucesso ,`r`n Pacotes Encontrados `r`n / 200"
    $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessage))

}
else {
    $textAreaLogs.ForeColor = "Red"
    $logMessage = " Inicie a Extracao de Pacotes Em `r`n / Pacotes Nao Encontrados `r`n / 404"
    $textAreaLogs.AppendText([System.String]::Format("{0}`r`n", $logMessage))
}


# Cria a aba para configuracao do banco de dados
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
    Write-Host "Arquivo nao encontrado: $caminhoArquivo_iniSelect"
    $temaAtual = "Retro"
}



# Define o evento de selecao do ComboBox
$comboBox.Add_SelectedIndexChanged({
        $temaSelecionado = $comboBox.SelectedItem
        $caminhoArquivo = "config.ini"
        $conteudoArquivo = CarregarOuCriarArquivo -caminhoCompleto $caminhoArquivo
        $conteudoArquivoAtualizado = $conteudoArquivo -replace "Theme = .+", "Theme = $temaSelecionado"
        $conteudoArquivoAtualizado | Out-File -FilePath $caminhoArquivo -Force
        $textBoxConfig.Clear()

        # Carrega novamente o conteúdo do arquivo atualizado
        $conteudoArquivoAtualizado = Get-Content $caminhoArquivo
        # Procura pelo valor de "Lang" no conteúdo do arquivo atualizado
        $valorLang = $conteudoArquivoAtualizado | Where-Object { $_ -match "^Lang\s*=\s*(.*)" } | ForEach-Object { $Matches[1] }
        $valorHost = $conteudoArquivoAtualizado | Where-Object { $_ -match "^Host\s*=\s*(.*)" } | ForEach-Object { $Matches[1] }
        $valorPort = $conteudoArquivoAtualizado | Where-Object { $_ -match "^Port\s*=\s*(.*)" } | ForEach-Object { $Matches[1] }
        $valorPass = $conteudoArquivoAtualizado | Where-Object { $_ -match "^Pass\s*=\s*(.*)" } | ForEach-Object { $Matches[1] }
        $valorDir = $conteudoArquivoAtualizado | Where-Object { $_ -match "^Dir\s*=\s*(.*)" } | ForEach-Object { $Matches[1] }
        # Exibe o valor de Lang
        # Write-Host "Valor de Lang: $valorLang"

        $conteudoArquivoFormatado = @"
[Panel]
Theme = $temaSelecionado
Lang  = $valorLang
Host  = $valorHost
Port  = $valorPort
Pass  = $valorPass
Dir   = $valorDir
"@
        # Cria o arquivo com o conteúdo padrao
        $conteudoArquivoFormatado

        # Salva o conteúdo atualizado no arquivo
        $conteudoArquivoFormatado | Out-File -FilePath $caminhoArquivo -Force

        # Carrega novamente o conteúdo do arquivo atualizado
        $conteudoArquivoAtualizado = Get-Content $caminhoArquivo

        $textBoxConfig.AppendText($conteudoArquivoFormatado)
    })

$tab2.Controls.Add($comboBox)


# Define a funcao para carregar ou criar um arquivo de configuracao
function CarregarOuCriarArquivo {
    param(
        [string]$caminhoCompleto
    )

    # Verifica se o arquivo existe
    if (Test-Path $caminhoCompleto -PathType Leaf) {
        # Lê o conteúdo do arquivo
        $conteudoArquivo = Get-Content -Path $caminhoCompleto

        # Separa a primeira linha (com o nome do painel) e as configuracões restantes
        $panel = $conteudoArquivo[0]
        $configuracoes = $conteudoArquivo[1..($conteudoArquivo.Length - 1)]

        # Formata as configuracões do arquivo para exibir as chaves e valores em linhas separadas
        $conteudoArquivoFormatado = $panel + "`r`n" + ($configuracoes -join "`r`n")
    }
    else {
        # Se o arquivo nao existir, cria o conteúdo padrao
        $conteudoArquivoFormatado = @"
[Panel]
Theme = Retro
Lang  = en
Host  = localhost
Port  = 8000
Pass  = admin
Dir   = .
"@
        # Cria o arquivo com o conteúdo padrao
        $conteudoArquivoFormatado | Out-File -FilePath $caminhoCompleto
    }

    return $conteudoArquivoFormatado
}


# Define a funcao para salvar as configuracões no arquivo
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

# TextArea para as configuracões
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
# Botao de Reset
$buttonReset = New-Object System.Windows.Forms.Button
$buttonReset.Location = New-Object System.Drawing.Point(20, 20)
$buttonReset.Size = New-Object System.Drawing.Size(100, 30)
$buttonReset.Text = "Reset"
$tab2.Controls.Add($buttonReset)

# Botao de Salvar
$buttonSave = New-Object System.Windows.Forms.Button
$buttonSave.Location = New-Object System.Drawing.Point(140, 20)
$buttonSave.Size = New-Object System.Drawing.Size(100, 30)
$buttonSave.Text = "Save"
$tab2.Controls.Add($buttonSave)

# Acao do botao Reset
$buttonReset.Add_Click({
        ReseteConfiguracoes -caminhoCompleto $caminhoArquivo
    })

# Acao do botao Save
$buttonSave.Add_Click({
        SalvarConfiguracoes -caminhoCompleto $caminhoArquivo -novoConteudo $textBoxConfig.Text
    })

function LerVariavelDoArquivoIni {
    param (
        [string]$caminhoCompleto,
        [string]$variavelDesejada
    )

    # Define uma variavel para armazenar o valor da variavel desejada
    $valorVariavel = ""

    # Verifica se o arquivo existe
    if (Test-Path $caminhoCompleto -PathType Leaf) {
        # Lê o conteúdo do arquivo
        $linhas = Get-Content -Path $caminhoCompleto

        # Loop pelas linhas do arquivo
        foreach ($linha in $linhas) {
            # Verifica se a linha contém a variavel desejada
            if ($linha -match "^\s*$variavelDesejada\s*=\s*(.*)\s*$") {
                $valorVariavel = $matches[1]
                break  # Se encontrarmos a variavel desejada, podemos parar de percorrer o arquivo
            }
        }
    }
    else {
        Write-Host "O arquivo nao foi encontrado no caminho especificado."
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

$labelTest = New-Object System.Windows.Forms.Label
$labelTest.Text = "Start"
$labelTest.ForeColor = "Green"
$labelTest.AutoSize = $true
$labelTest.Location = New-Object System.Drawing.Point(270, 20)
$labelTest.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)  
$tab3.Controls.Add($labelTest)

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

# Input 3
$pid_input = New-Object System.Windows.Forms.TextBox
$pid_input.Location = New-Object System.Drawing.Point(250, 50)
$pid_input.Enabled = $false
$pid_input.Text = ""
$pid_input.Size = New-Object System.Drawing.Size(100, 20)
$tab3.Controls.Add($pid_input)

# Botao
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

$labelPhpWindows = New-Object System.Windows.Forms.Label
$labelPhpWindows.Text = ""
$labelPhpWindows.ForeColor = "Green"
$labelPhpWindows.AutoSize = $true
$labelPhpWindows.Location = New-Object System.Drawing.Point(250, 55)
$labelPhpWindows.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)  
$tab1.Controls.Add($labelPhpWindows)

# Criar a aba (TabPage) "Processos"
$tab4 = New-Object System.Windows.Forms.TabPage
$tab4.Text = "Processos"
# $tabControl.Controls.Add($tab4)


$tabControl.TabPages.Remove($tab2)
$tabControl.TabPages.Remove($tab3)
$tabControl.TabPages.Remove($tab4)
$unidade = $env:SystemDrive
$pasta = "VersionPHP"
$caminhoCompleto = Join-Path -Path $unidade -ChildPath $pasta
if (Test-Path -Path $caminhoCompleto -PathType Container) {
    Write-Host "A pasta '$pasta' existe em '$unidade'."
    $labelPhpWindows.Text = "PHP - 200"
    $labelPhpWindows.ForeColor = "Green"
    $tabControl.TabPages.Add($tab2)
    $tabControl.TabPages.Add($tab3)
    $tabControl.TabPages.Add($tab4)
}
else {
    $labelPhpWindows.Text = "PHP - 404"
    $labelPhpWindows.ForeColor = "Red"
    $tabControl.TabPages.Remove($tab2)
    $tabControl.TabPages.Remove($tab3)
    $tabControl.TabPages.Remove($tab4)
}


# Criar a TextBox para a saída do texto
$prefixTextarea = New-Object System.Windows.Forms.TextBox
$prefixTextarea.Multiline = $true
$prefixTextarea.ScrollBars = "Vertical"
$prefixTextarea.Width = 50
$prefixTextarea.Height = 10
$prefixTextarea.Anchor = "Top, Left, Right, Bottom"
$tab4.Controls.Add($prefixTextarea)

# Caminho do arquivo _pfx.json
$caminhoArquivoPRE = ".\_pfx.json"

# Verificar se o arquivo existe
if (Test-Path $caminhoArquivoPRE -PathType Leaf) {
    # Ler o conteúdo do arquivo como texto simples
    $conteudoTextoPREFIXO = Get-Content -Path $caminhoArquivoPRE -Raw
    $prefixTextarea.Text = $conteudoTextoPREFIXO

    # Ajustar o tamanho da fonte e a cor do texto
    $prefixTextarea.Font = New-Object System.Drawing.Font("Arial", 12)
    $prefixTextarea.ForeColor = "Green"
}
else {
    Write-Host "O arquivo não foi encontrado: $caminhoArquivoPRE"
}

$labelPhpSistem = New-Object System.Windows.Forms.Label
$labelPhpSistem.Text = "En-VRT"
$labelPhpSistem.AutoSize = $true
$labelPhpSistem.Location = New-Object System.Drawing.Point(250, 20)
$labelPhpSistem.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)  
$tab4.Controls.Add($labelPhpSistem)

# Criar um TextBox de entrada
$inputTextBoxProcess = New-Object System.Windows.Forms.TextBox
$inputTextBoxProcess.Location = New-Object System.Drawing.Point(250, 55)
$inputTextBoxProcess.Enabled = $false
$tab4.Controls.Add($inputTextBoxProcess)

$unidade = $env:SystemDrive
$pasta = "VersionPHP\php5.4.0"
$caminhoPasta = Join-Path -Path $unidade -ChildPath $pasta

# Verificar se a pasta existe
if (Test-Path $caminhoPasta -PathType Container) {
    # Procurar por arquivos com o nome "php_" dentro da pasta
    $arquivosPhp = Get-ChildItem -Path $caminhoPasta -Filter "php_*" -File
    
    if ($arquivosPhp.Count -gt 0) {
        # Exibir o nome dos arquivos encontrados
        foreach ($arquivo in $arquivosPhp) {
            $inputTextBoxProcess.Text = $arquivo.Name
            Write-Host "Arquivo encontrado: $($arquivo.Name)"
        }
    }
    else {
        Write-Host "Nenhum arquivo com o nome 'php_' encontrado na pasta: $caminhoPasta"
    }
}
else {
    Write-Host "A pasta não foi encontrada: $caminhoPasta"
}


function ProcessarEAtualizarArquivo {
    $novoConteudo = $prefixTextarea.Text
    $caminhoArquivo = "$diretorioPai\_pfx.json"
    if (Test-Path $caminhoArquivo -PathType Leaf) {
        $novoConteudo | Set-Content -Path $caminhoArquivo -Force
        [System.Windows.Forms.MessageBox]::Show("Conteúdo atualizado com sucesso em: $caminhoArquivo")
        Write-Host "Conteúdo atualizado com sucesso em: $caminhoArquivo"
    }
    else {
        [System.Windows.Forms.MessageBox]::Show("erro", "O arquivo não foi encontrado: $caminhoArquivo")
        Write-Host "O arquivo não foi encontrado: $caminhoArquivo"
    }
}



$makeFile_prf_ = @"
[
    {
        "_prf_":"php_5.exe"
    }
]
"@

function ProcessarResetaPrefixo {
    $caminhoArquivo = "$diretorioPai\_pfx.json"
    if (Test-Path $caminhoArquivo -PathType Leaf) {
        $prefixTextarea.Text = $makeFile_prf_
        $makeFile_prf_ | Set-Content -Path $caminhoArquivo -Force
        [System.Windows.Forms.MessageBox]::Show("Conteúdo restaurado com sucesso em: $caminhoArquivo")
        Write-Host "Conteúdo restaurado com sucesso em: $caminhoArquivo"
    }
    else {
        [System.Windows.Forms.MessageBox]::Show("O arquivo não foi encontrado: $caminhoArquivo", "Erro")
        Write-Host "O arquivo não foi encontrado: $caminhoArquivo"
    }
}


$buttonProcessarPrefixo = New-Object System.Windows.Forms.Button
$buttonProcessarPrefixo.Text = "Processar Prefixo"
$buttonProcessarPrefixo.Location = New-Object System.Drawing.Point(40, 230)
$buttonProcessarPrefixo.Width = 150
$buttonProcessarPrefixo.Add_Click({ ProcessarEAtualizarArquivo })
$tab4.Controls.Add($buttonProcessarPrefixo)

$buttonProcessarReset = New-Object System.Windows.Forms.Button
$buttonProcessarReset.Text = "Reseta Prefixo"
$buttonProcessarReset.Location = New-Object System.Drawing.Point(40, 260)
$buttonProcessarReset.Width = 150
$buttonProcessarReset.Add_Click({ ProcessarResetaPrefixo })
$tab4.Controls.Add($buttonProcessarReset)



# $button_iniciar.Add_Click({
#         # Obtém o PID do processo anterior, se existir
#         $processoAnteriorPID = $pid_input.Text
#         if ($processoAnteriorPID -ne "") {
#             # Tenta encerrar o processo anterior
#             try {
#                 $processoAnterior = Get-Process -Id $processoAnteriorPID -ErrorAction Stop
#                 $processoAnterior.Kill()
#                 $textBox.AppendText("Processo anterior (PID: $processoAnteriorPID) encerrado com sucesso." + [Environment]::NewLine)
#             }
#             catch {
#                 $textBox.AppendText("Erro ao encerrar o processo anterior (PID: $processoAnteriorPID)." + [Environment]::NewLine)
#             }
#         }

#         # Define o comando a ser executado
#         $comando = "cd ./Packages && cd phpLiteAdmin && php_5.exe -S $($_Host):$($_Port)"

#         # Cria um processo para executar o comando e redireciona a saida padrao
#         $processo = Start-Process -FilePath "cmd.exe" -ArgumentList "/c $comando" -NoNewWindow -PassThru

#         # Se o processo foi iniciado com sucesso
#         if ($processo) {
#             Wait-Process $processId = $processo.Id  # Obtém o PID do processo

#             # Atualiza o valor de $pid_input.Text com o PID atual
#             $pid_input.Text = $processId

#             $textBox.AppendText("O PHP Server foi iniciado com sucesso. PID: $processId" + [Environment]::NewLine)
#             $textBox.AppendText("Iniciando Teste ..." + [Environment]::NewLine)
#             # URL a ser aberta

#             # Funcao para ler a saida do processo e exibir na caixa de texto
#             $leituraProcesso = {
#                 param($processo, $textBox)

#                 while (!$processo.HasExited) {
#                     $linha = $processo.StandardOutput.ReadLine()
#                     if ($linha -ne $null) {
#                         $textBox.BeginInvoke([Action[string]] { param($line) $textBox.AppendText($line + [Environment]::NewLine) }, $linha) | Out-Null
#                     }
#                     Start-Sleep -Milliseconds 100  # Aguarda um curto periodo para evitar bloqueios
#                 }
#             }

#             # Inicia a leitura da saida do processo em segundo plano
#             Start-Job -ScriptBlock $leituraProcesso -ArgumentList $processo, $textBox

#             Start-Sleep -Seconds 3
#             $url = "http://$($_Host):$($_Port)/angueraAdmin.php"
#             Start-Process $url
#         }
#         else {
#             # Se ocorreu um erro ao iniciar o processo
#             $textBox.AppendText("Erro ao iniciar o PHP Server." + [Environment]::NewLine)
#         }
#     })

function AbrirJanelaComNavegador {
    param (
        [string]$url
    )

    # Crie uma nova instância do formulario
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Navegador angueraAdmin 0.1"
    $form.Size = New-Object System.Drawing.Size(800, 600)

    # Crie uma instância do controle WebBrowser
    $webBrowser = New-Object System.Windows.Forms.WebBrowser
    $webBrowser.Dock = "Fill"
    $webBrowser.Location = New-Object System.Drawing.Point(0, 0)
    # $webBrowser.Visible = $true

    # Navegue para a URL especificada
    $webBrowser.Navigate($url)

    # Defina algumas configuracões de seguranca para permitir a execucao de scripts
    $webBrowser.ScriptErrorsSuppressed = $true # Suprime erros de script
    $webBrowser.WebBrowserShortcutsEnabled = $true # Habilita atalhos do navegador
    $webBrowser.ObjectForScripting = $true # Permite a comunicacao entre o navegador e o código PowerShell

    # Adicione o controle WebBrowser ao formulario
    $form.Controls.Add($webBrowser)

    # Exiba o formulario
    $form.ShowDialog() | Out-Null
}

function LerJson {
    param (
        [string]$CaminhoArquivo,
        [string]$NomeChave
    )

    if (Test-Path $CaminhoArquivo) {
        $conteudoJson = Get-Content -Path $CaminhoArquivo -Raw | ConvertFrom-Json
        if ($conteudoJson.$NomeChave) {
            return $conteudoJson.$NomeChave
        }
        else {
            Write-Host "A chave '$NomeChave' não foi encontrada no arquivo JSON."
            return $null
        }
    }
    else {
        Write-Host "O arquivo $CaminhoArquivo não foi encontrado."
        return $null
    }
}





$button_iniciar.Add_Click({

    
        $phpProcess = LerJson -CaminhoArquivo "$diretorioPai\_pfx.json" -NomeChave "_prf_"

        if ($jsonData -ne $null) {
            foreach ($objeto in $jsonData) {
                Write-Host "Prefixo: $($objeto._prf_)"
            }
        }
        else {
            Write-Host "Não foi possível ler os dados do arquivo JSON."
        }

        Start-Sleep -Milliseconds 400

        $processoAnteriorPID = $pid_input.Text
        if ($processoAnteriorPID -ne "") {
            # Tenta encerrar o processo anterior
            try {
                $processoAnterior = Get-Process -Id $processoAnteriorPID -ErrorAction Stop
                $processoAnterior.Kill()
                $textBox.AppendText("Processo anterior (PID: $processoAnteriorPID) encerrado com sucesso." + [Environment]::NewLine)
            }
            catch {
                $textBox.AppendText("Erro ao encerrar o processo anterior (PID: $processoAnteriorPID)." + [Environment]::NewLine)
            }
        }

        # Define o caminho para o diretório onde o PHP sera iniciado
        $caminhoPHP = "$diretorioDll\Packages\phpLiteAdmin"

        
        $textBox.AppendText("Caminho Encontrado => : $caminhoPHP " + [Environment]::NewLine)
        # Verifica se o diretório existe
        if (Test-Path $caminhoPHP -PathType Container) {
            # Entra no diretório onde o PHP sera iniciado
            Set-Location $caminhoPHP

            # Inicia o PHP diretamente
            $processo = Start-Process -FilePath "$phpProcess" -ArgumentList "-S $($_Host):$($_Port)"  -NoNewWindow -PassThru
            
            $textBox.AppendText("Processamento Criado => : $processo " + [Environment]::NewLine)
            $textBox.AppendText("Processamento Criado => : $($processo.MachineName) " + [Environment]::NewLine)
            $textBox.AppendText("Processamento Criado => : $($processo.CPU) " + [Environment]::NewLine)
            # Se o processo foi iniciado com sucesso
            if ($processo) {
                $processId = $processo.Id  # Obtém o PID do processo

                # Atualiza o valor de $pid_input.Text com o PID atual
                $pid_input.Text = $processId

                $textBox.AppendText("O PHP Server foi iniciado com sucesso. PID: $processId" + [Environment]::NewLine)
                $textBox.AppendText("Iniciando Teste ..." + [Environment]::NewLine)
                # URL a ser aberta

                # Funcao para ler a saida do processo e exibir na caixa de texto
                $leituraProcesso = {
                    param($processo, $textBox)

                    while (!$processo.HasExited) {
                        $linha = $processo.StandardOutput.ReadLine()
                        if ($linha -ne $null) {
                            $textBox.BeginInvoke([Action[string]] { param($line) $textBox.AppendText($line + [Environment]::NewLine) }, $linha) | Out-Null
                        }
                        Start-Sleep -Milliseconds 100  # Aguarda um curto periodo para evitar bloqueios
                    }
                }

                $labelTest.Text = "Stop"
                $labelTest.ForeColor = "Red"

                $pidFilePath = "$diretorioDll\Keys\Pid_PHP.txt"
                if (-not (Test-Path $pidFilePath)) {
                    New-Item -ItemType Directory -Force -Path "./Keys"
                    New-Item -ItemType File -Force -Path $pidFilePath
                }

                $processId | Out-File -FilePath $pidFilePath -Encoding ASCII -Force

                # $diretorioDll = $PWD.Path
                
                CriarLogs -caminhoLog "$diretorioDll\Logs\Log_PHP.log" -logs $textBox.Text
                
                # Inicia a leitura da saida do processo em segundo plano
                Start-Job -ScriptBlock $leituraProcesso -ArgumentList $processo, $textBox

                Start-Sleep -Seconds 2
                $url = "http://$($_Host):$($_Port)"
                AbrirJanelaComNavegador -url $url
                # $url = "http://$($_Host):$($_Port)/angueraAdmin.php"
                # Start-Process $url
            }
            else {
                # Se ocorreu um erro ao iniciar o processo
                $textBox.AppendText("Erro ao iniciar o PHP Server." + [Environment]::NewLine)
            }
        }
        else {
            # Se o diretório nao existir, exibe uma mensagem de erro
            $textBox.AppendText("O diretório '$caminhoPHP' nao foi encontrado." + [Environment]::NewLine)
        }
    })


$button_stop.Add_Click({
        $processoPID = $pid_input.Text
        if ($processoPID -ne "") {
            try {
                # Obtém o processo com o PID especificado
                $processoParaEncerrar = Get-Process -Id $processoPID -ErrorAction Stop

                $labelTest.Text = "Start"
                $labelTest.ForeColor = "Green"

                # Verifica se o processo foi encontrado
                if ($processoParaEncerrar) {
                    # Encerra o processo
                    $processoParaEncerrar.Kill()
                    $textBox.AppendText("Processo com PID $processoPID encerrado com sucesso." + [Environment]::NewLine)

                    # Fecha a janela após encerrar o processo
                    $textBox.AppendText("Fechando Janela..." + [Environment]::NewLine)
                    Start-Sleep -Milliseconds 2000
                    $form.Close()
                }
                else {
                    # Se o processo nao foi encontrado, exibe uma mensagem de erro
                    $textBox.AppendText("Nenhum processo encontrado com o PID $processoPID." + [Environment]::NewLine)
                }
            }
            catch {
                $textBox.AppendText("Erro ao encerrar o processo com PID $processoPID." + [Environment]::NewLine)
            }
        }
        else {
            $textBox.AppendText("Nenhum PID fornecido para encerrar o processo." + [Environment]::NewLine)
        }
    })


$form.ShowDialog() | Out-Null

