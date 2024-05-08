
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$diretorioPai = $PWD.Path
$diretorioDll = $PWD.Path
$diretorioPadrao = "."
$diretorioDll = if ($PWD -ne $null) { $PWD.Path } else { $diretorioPadrao }
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

function VerificarExistenciaPasta {
    param(
        [string]$caminho_pasta
    )

    if (Test-Path $caminho_pasta -PathType Container) {
        return $true
    }
    else {
        return $false
    }
}

# Exemplo de uso da função
# $caminho_arquivo = "App\Browsers\Browser.ini"
# $resultado = VerificarExistenciaArquivo $caminho_arquivo
# Write-Host "O arquivo existe? $resultado"



$form = New-Object System.Windows.Forms.Form
$form.Text = "Painel angueraBooks"
$form.Size = New-Object System.Drawing.Size(440, 380)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedSingle"


$tabControl = New-Object System.Windows.Forms.TabControl
$tabControl.Size = New-Object System.Drawing.Size(400, 330)
$tabControl.Location = New-Object System.Drawing.Point(10, 10)
$form.Controls.Add($tabControl)




function FecharFormulario {
    # Carregar o texto do arquivo de log
    $pid_Painel = CarregarLogs -caminhoLog "$diretorioPai\Script\Processamento_Form\pid.txt"
    
    # Expressão regular para encontrar o número do PID
    $regex = [regex]"\b\d+\b"
    
    # Extrair o número do PID usando a expressão regular
    $pid_Painel_Numero = $regex.Match($pid_Painel).Value

    if ($pid_Painel_Numero -ne "") {
        try {
            # Tentar obter o processo com o PID extraído
            $processoParaEncerrar = Get-Process -Id $pid_Painel_Numero -ErrorAction Stop
            if ($processoParaEncerrar) {
                # Encerrar o processo se ele existir
                $processoParaEncerrar.Kill()
                Write-Host "Janela Encerrada" 
            }
            else {
                Write-Host "Nenhum processo encontrado com o PID $pid_Painel_Numero."
            }
        }
        catch {
            Write-Host "Erro ao encerrar o processo com PID $pid_Painel_Numero."
        }
    }
    else {
        Write-Host "Nenhum PID fornecido para encerrar o processo."
    }
}

$buttonFechar = New-Object System.Windows.Forms.Button
$buttonFechar.Text = "Fechar"
$buttonFechar.Size = New-Object System.Drawing.Size(200, 30)
$buttonFechar.Location = New-Object System.Drawing.Point(170, 260)
$buttonFechar.BackColor = [System.Drawing.Color]::Red
$buttonFechar.ForeColor = [System.Drawing.Color]::White


$form.Add_FormClosing({
        FecharFormulario
    })





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


function ModificarOuObterChaveEmINI {
    param(
        [string]$arquivo_ini,
        [string]$secao,
        [string]$chave,
        [string]$novo_valor
    )

    # Verifica se o arquivo INI existe
    if (Test-Path $arquivo_ini -PathType Leaf) {
        # Lê o conteúdo do arquivo INI
        $conteudo_ini = Get-Content $arquivo_ini

        # Variável para armazenar o valor da chave
        $valor_chave = $null

        # Variável para verificar se a seção foi encontrada
        $secao_encontrada = $false

        # Loop pelo conteúdo do arquivo INI
        for ($i = 0; $i -lt $conteudo_ini.Length; $i++) {
            $linha = $conteudo_ini[$i]

            # Verifica se a seção foi encontrada
            if ($linha -match "^\[$secao\]") {
                $secao_encontrada = $true
            }
            # Verifica se a chave foi encontrada dentro da seção
            elseif ($secao_encontrada -and $linha -match "^$chave\s*=") {
                $valor_chave = $linha -replace "^$chave\s*=\s*"
                # Se um novo valor for fornecido, modifica o valor da chave
                if ($novo_valor -ne "") {
                    $linha_modificada = "$chave = $novo_valor"
                    $conteudo_ini[$i] = $linha_modificada
                    $conteudo_ini | Set-Content $arquivo_ini -Force
                }
                break
            }
        }

        # Se a seção não foi encontrada, exibe uma mensagem de erro
        if (-not $secao_encontrada) {
            Write-Host "A seção especificada não foi encontrada no arquivo INI."
        }

        # Retorna o valor da chave
        return $valor_chave
    }
    else {
        Write-Host "O arquivo INI especificado não existe."
    }
}


# Exemplo de uso para modificar uma chave:
# ModificarOuObterChaveEmINI -arquivo_ini "config.ini" -secao "Navegador" -chave "navegador" -novo_valor "N[System] / N[Compiler]"

# Exemplo de uso para obter o valor de uma chave:
# $valor_chave = ModificarOuObterChaveEmINI -arquivo_ini "config.ini" -secao "Navegador" -chave "navegador"
# if ($valor_chave) {
#     Write-Host "O valor da chave 'navegador' é: $valor_chave"
# }

$caminho_browsePackager = "App\Browser"
$browsePackager = VerificarExistenciaPasta $caminho_browsePackager
Write-Host "O arquivo $caminho_browsePackager existe? $browsePackager"

# Tab "Navegador"
$tab3 = New-Object System.Windows.Forms.TabPage
$tab3.Text = "Navegador"
$tabControl.Controls.Add($tab3)

$btnbaixarPacotes = New-Object System.Windows.Forms.Button
$btnbaixarPacotes.Location = New-Object System.Drawing.Point(20, 50)
$btnbaixarPacotes.Size = New-Object System.Drawing.Size(200, 30)
$btnbaixarPacotes.Text = "Baixar Navegador Detalhado"
$tab3.Controls.Add($btnbaixarPacotes)

$lblBaixar = New-Object System.Windows.Forms.Label
$lblBaixar.Location = New-Object System.Drawing.Point(230, 55)
$lblBaixar.Size = New-Object System.Drawing.Size(300, 10)
$lblBaixar.Text = "-> Atualize Agora !"
$lblBaixar.Font = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)  # Definindo a fonte e o tamanho
$lblBaixar.AutoSize = $true  # Permitindo que o Label se ajuste automaticamente ao texto
$lblBaixar.ForeColor = [System.Drawing.Color]::Red
$tab3.Controls.Add($lblBaixar)

# Criar botão de opção "Navegador Otimizado"
$radioOtimizado = New-Object System.Windows.Forms.RadioButton
$radioOtimizado.Location = New-Object System.Drawing.Point(20, 20)
$radioOtimizado.Size = New-Object System.Drawing.Size(200, 20)
$radioOtimizado.Text = "Navegador Otimizado"
$tab3.Controls.Add($radioOtimizado)

$radioDetalhado = New-Object System.Windows.Forms.RadioButton
$radioDetalhado.Location = New-Object System.Drawing.Point(20, 50)
$radioDetalhado.Size = New-Object System.Drawing.Size(200, 20)
$radioDetalhado.Text = "Navegador Detalhado"
$tab3.Controls.Add($radioDetalhado)

if ($browsePackager -eq $false ) {
    
    $radioDetalhado.Visible = $false
    $lblNavegadorSelecionado.ForeColor = [System.Drawing.Color]::Green  # Definindo a cor do texto como verde
    $lblNavegadorSelecionado.BackColor = [System.Drawing.Color]::White  # Definindo o plano de fundo como branco
    $lblNavegadorSelecionado.Text = "Otmizado -> $fNv"
    $radioOtimizado.Checked = $true
    ModificarOuObterChaveEmINI -arquivo_ini "$diretorioPai\App\Tools\Browser.ini" -secao "Navegador" -chave "navegador" -novo_valor "N[System]"

}
else {
    # Criar botão de opção "Navegador Detalhado"
    $lblBaixar.ForeColor = [System.Drawing.Color]::Blue
    $lblBaixar.Text = " <- Versao 1.0 / CPM"
    $radioDetalhado.Visible = $true
    $btnbaixarPacotes.Visible = $false
    $lblBaixar.Location = New-Object System.Drawing.Point(200, 55)
    $lblBaixar.Size = New-Object System.Drawing.Size(200, 10)
}


# Criar botão de salvar
$btnSalvar = New-Object System.Windows.Forms.Button
$btnSalvar.Location = New-Object System.Drawing.Point(20, 90)
$btnSalvar.Size = New-Object System.Drawing.Size(200, 30)
$btnSalvar.Text = "Salvar"
$tab3.Controls.Add($btnSalvar)



# Criar rótulo para exibir o navegador selecionado
$lblNavegadorSelecionado = New-Object System.Windows.Forms.Label
$lblNavegadorSelecionado.Location = New-Object System.Drawing.Point(20, 130)
$lblNavegadorSelecionado.Size = New-Object System.Drawing.Size(300, 20)
$lblNavegadorSelecionado.Font = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)  # Definindo a fonte e o tamanho
$lblNavegadorSelecionado.AutoSize = $true  # Permitindo que o Label se ajuste automaticamente ao texto
$lblNavegadorSelecionado.Padding = New-Object System.Windows.Forms.Padding(5)  # Adicionando um pequeno espaçamento interno
$lblNavegadorSelecionado.BorderStyle = "Fixed3D"  # Adicionando um estilo de borda arredondada

$tab3.Controls.Add($lblNavegadorSelecionado)


$fNv = ModificarOuObterChaveEmINI -arquivo_ini "$diretorioPai\App\Tools\Browser.ini" -secao "Navegador" -chave "navegador"
if ($fNv) {
    
    if ($fNv -eq "N[Compiler]") {
        $lblNavegadorSelecionado.ForeColor = [System.Drawing.Color]::Orange  # Definindo a cor do texto como verde
        $lblNavegadorSelecionado.BackColor = [System.Drawing.Color]::White  # Definindo o plano de fundo como branco
        $lblNavegadorSelecionado.Text = "Detalhado -> $fNv"
        $radioDetalhado.Checked = $true
    }
    elseif ($fNv -eq "N[System]") {
        $lblNavegadorSelecionado.ForeColor = [System.Drawing.Color]::Green  # Definindo a cor do texto como verde
        $lblNavegadorSelecionado.BackColor = [System.Drawing.Color]::White  # Definindo o plano de fundo como branco
        $lblNavegadorSelecionado.Text = "Otmizado -> $fNv"
        $radioOtimizado.Checked = $true
    }

}


# Adicionar evento de clique ao label
$btnbaixarPacotes_Click = {
    # Caminho para o executável do angueraCli.exe
    $caminhoExe = "angueraCli.exe"

    # Verifica se o executável existe
    if (Test-Path $caminhoExe -PathType Leaf) {
        # Inicia o processo
        Start-Process -FilePath $caminhoExe
        $form.Close()
        $form.ShowDialog() | Out-Null
        Write-Host "Processo angueraCli.exe iniciado com sucesso."
    } else {
        Write-Host "O executável angueraCli.exe não foi encontrado no caminho especificado."
    }
}

# Associar o evento de clique ao label
$btnbaixarPacotes.Add_Click($btnbaixarPacotes_Click)

$tab3.Controls.Add($lblNavegadorSelecionado)

# Adicionar um evento de clique para o botão "Salvar"
$btnSalvar.Add_Click({
        if ($radioOtimizado.Checked) {
            $lblNavegadorSelecionado.ForeColor = [System.Drawing.Color]::Green  # Definindo a cor do texto como verde
            $lblNavegadorSelecionado.BackColor = [System.Drawing.Color]::White  # Definindo o plano de fundo como branco
            $lblNavegadorSelecionado.Text = "Otmizado -> $fNv"
            ModificarOuObterChaveEmINI -arquivo_ini "$diretorioPai\App\Tools\Browser.ini" -secao "Navegador" -chave "navegador" -novo_valor "N[System]"
            
        }
        elseif ($radioDetalhado.Checked) {
            $lblNavegadorSelecionado.ForeColor = [System.Drawing.Color]::Orange  # Definindo a cor do texto como verde
            $lblNavegadorSelecionado.BackColor = [System.Drawing.Color]::White  # Definindo o plano de fundo como branco
            $lblNavegadorSelecionado.Text = "Detalhado -> $fNv"
            ModificarOuObterChaveEmINI -arquivo_ini "$diretorioPai\App\Tools\Browser.ini" -secao "Navegador" -chave "navegador" -novo_valor "N[Compiler]"
           
        }
        else {
            $lblNavegadorSelecionado.Text = "Nenhum navegador selecionado"
        }

    })



# Criar a aba (TabPage) "Processos"
$tab4 = New-Object System.Windows.Forms.TabPage
$tab4.Text = "Processos"
$tabControl.TabPages.Add($tab4)

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


$form.ShowDialog() | Out-Null

