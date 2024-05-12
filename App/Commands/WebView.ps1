$diretorioDll = $PWD.Path
$diretorioPai = $PWD.Path
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function LerVariavelDoArquivoIni {
    param (
        [string]$caminhoCompleto,
        [string]$variavelDesejada
    )

    $valorVariavel = ""

    if (Test-Path $caminhoCompleto -PathType Leaf) {
        $linhas = Get-Content -Path $caminhoCompleto

        foreach ($linha in $linhas) {
            if ($linha -match "^\s*$variavelDesejada\s*=\s*(.*)\s*$") {
                $valorVariavel = $matches[1]
                break
            }
        }
    }
    else {
        Write-Host "O arquivo não foi encontrado no caminho especificado."
    }

    return $valorVariavel
}

$caminhoArquivoIni = "config.ini"
$_Host = LerVariavelDoArquivoIni -caminhoCompleto $caminhoArquivoIni -variavelDesejada "Host"
$_Port = LerVariavelDoArquivoIni -caminhoCompleto $caminhoArquivoIni -variavelDesejada "Port"

$caminhoArquivoBrowser = "App/Tools/Browser.ini"
$_opBrowser = LerVariavelDoArquivoIni -caminhoCompleto $caminhoArquivoBrowser -variavelDesejada "navegador"
Write-Host $_opBrowser

$form = New-Object System.Windows.Forms.Form
$form.Text = "Navegador angueraAdmin 0.1"
$form.Size = New-Object System.Drawing.Size(800, 600)
$form.WindowState = "Maximized"



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


    
$phpProcess = LerJson -CaminhoArquivo "$diretorioDll\_pfx.json" -NomeChave "_prf_"
Write-Host "Processo do PHP $phpProcess"

function AbrirJanelaComNavegador {
    param (
        [string]$url
    )

    $label = New-Object System.Windows.Forms.Label
    $label.Text = "PID -> EXE:"
    $label.Size = New-Object System.Drawing.Size(200, 30)
    $label.Location = New-Object System.Drawing.Point(20, 450)
    $label.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
    $form.Controls.Add($label)

    $textBox = New-Object System.Windows.Forms.TextBox
    $textBox.Location = New-Object System.Drawing.Point(20, 500)
    $textBox.Size = New-Object System.Drawing.Size(200, 40)
    $textBox.Multiline = $true
    $textBox.Enabled = $false
    $textBox.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
    $textBox.Text = $PID  # Inicializar com o valor de $PID
    $form.Controls.Add($textBox)

    $webBrowser = New-Object System.Windows.Forms.WebBrowser
    $webBrowser.Dock = "Fill"
    $webBrowser.Location = New-Object System.Drawing.Point(0, 40)
    $webBrowser.Visible = $true
    $webBrowser.Navigate($url)
    # $webBrowser.ScriptErrorsSuppressed = $true  # Suprime erros de script
    # $webBrowser.WebBrowserShortcutsEnabled = $true  # Habilita atalhos do navegador
    # $webBrowser.ObjectForScripting = $true  # Permite a comunicação entre o navegador e o código PowerShell
    # $webBrowser.IsWebBrowserContextMenuEnabled = $true  # Habilita o menu de contexto do navegador
    # $webBrowser.AllowNavigation = $true  # Permite a navegação no navegador
    # $webBrowser.AllowWebBrowserDrop = $true  # Permite a solta de arquivos no navegador
    # $webBrowser.AllowWebBrowserDrop = $true  # Permite a solta de arquivos no navegador
    # $webBrowser.IsWebBrowserContextMenuEnabled = $true  # Habilita o menu de contexto do navegador
    # $webBrowser.AllowNavigation = $true  # Permite a navegação no navegador
    # $webBrowser.AllowWebBrowserDrop = $true  # Permite a solta de arquivos no navegador
    # $webBrowser.ScriptErrorsSuppressed = $true  # Suprime erros de script
    # $webBrowser.WebBrowserShortcutsEnabled = $true  # Habilita atalhos do navegador
    # $webBrowser.ObjectForScripting = $true  # Permite a comunicação entre o navegador e o código PowerShell
    # $webBrowser.AllowNavigation = $true  # Permite a navegação no navegador
    # $webBrowser.AllowWebBrowserDrop = $true  # Permite a solta de arquivos no navegador
    # $webBrowser.IsWebBrowserContextMenuEnabled = $true  # Habilita o menu de contexto do navegador
    # $webBrowser.AllowNavigation = $true  # Permite a navegação no navegador
    # $webBrowser.AllowWebBrowserDrop = $true  # Permite a solta de arquivos no navegador
    # $webBrowser.ScriptErrorsSuppressed = $true  # Suprime erros de script
    # $webBrowser.WebBrowserShortcutsEnabled = $true  # Habilita atalhos do navegador
    # $webBrowser.ObjectForScripting = $true  # Permite a comunicação entre o navegador e o código PowerShell
    # $webBrowser.AllowNavigation = $true  # Permite a navegação no navegador
    # $webBrowser.AllowWebBrowserDrop = $true  # Permite a solta de arquivos no navegador
    # $webBrowser.IsWebBrowserContextMenuEnabled = $true  # Habilita o menu de contexto do navegador
    # $webBrowser.AllowNavigation = $true  # Permite a navegação no navegador
    # $webBrowser.AllowWebBrowserDrop = $true  # Permite a solta de arquivos no navegador

    $webBrowser.ScriptErrorsSuppressed = $true  # Suprime erros de script
    $webBrowser.WebBrowserShortcutsEnabled = $true  # Habilita atalhos do navegador
    $webBrowser.ObjectForScripting = $true  # Permite a comunicação entre o navegador e o código PowerShell
    $webBrowser.AllowNavigation = $true  # Permite a navegação no navegador
    $webBrowser.IsWebBrowserContextMenuEnabled = $true  # Habilita o menu de contexto do navegador
    $webBrowser.AllowWebBrowserDrop = $true  # Permite a solta de arquivos no navegador


    
    $form.Controls.Add($webBrowser)

    
    # Evento de fechar a janela

    $form.Add_FormClosing({
            try {
                # Lê todos os conteúdos do arquivo pid.txt
                $processes = Get-Content -Path "$($diretorioDll)\App\Commands\Proccess\pid.txt"
                foreach ($process in $processes) {
                    if ($process -match 'pr\d+\s+=\s+(\d+)') {
                        $processId = $matches[1]  # Renomear para processId
                        try {
                            $processoParaEncerrar = Get-Process -Id $processId -ErrorAction Stop
                            if ($processoParaEncerrar) {
                                $processoParaEncerrar.Kill()
                                Write-Host "Processo com PID $processId encerrado com sucesso."
                            }
                            else {
                                Write-Host "Nenhum processo encontrado com o PID $processId."
                            }
                        }
                        catch {
                            Write-Host "Erro ao encerrar o processo com PID $processId."
                        }
                    }
                }
                # Limpar o conteúdo do arquivo pid.txt
                Set-Content -Path "$($diretorioDll)\App\Commands\Proccess\pid.txt" -Value ""
            }
            catch {
                Write-Host "Erro ao tentar ler e limpar o arquivo pid.txt: $_"
            }
        })



}

$textBoxCli = New-Object System.Windows.Forms.TextBox
$textBoxCli.Location = New-Object System.Drawing.Point(20, 550)
$textBoxCli.Size = New-Object System.Drawing.Size(200, 40)
$textBoxCli.Multiline = $true
$textBoxCli.Enabled = $false
$textBoxCli.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$form.Controls.Add($textBoxCli)


$caminhoPHP = "$diretorioDll\Packages\phpLiteAdmin"
Write-Host "Caminho Atual: $($caminhoPHP)"

if (Test-Path -Path $caminhoPHP -PathType Container) {
    Write-Host "O diretório $caminhoPHP existe."

    Set-Location $caminhoPHP
    
    # Define a política de execução para Bypass
    Set-ExecutionPolicy Bypass -Scope Process -Force
    $processo = Start-Process -FilePath "$phpProcess" -ArgumentList "-S $($_Host):$($_Port)"  -NoNewWindow -PassThru
    Set-ExecutionPolicy Default -Scope Process -Force
    
    if ($processo) {
        $textBoxCli.Text = $processo.Id
        $pid_prc = $PID
        $url = "http://$($_Host):$($_Port)"
        Clear-Content -Path "$($diretorioDll)\App\Commands\Proccess\pid.txt"
        # Salvar os PIDs no arquivo pid.txt sem sobrescrever os valores antigos
        "pr2 = $($processo.Id)" | Add-Content -Path "$($diretorioDll)\App\Commands\Proccess\pid.txt"
        "pr3 = $($pid_prc)" | Add-Content -Path "$($diretorioDll)\App\Commands\Proccess\pid.txt"
        

        # AbrirJanelaComNavegador -url $url
        # $form.ShowDialog() | Out-Null

        if($_opBrowser -eq "N[System]"){
            AbrirJanelaComNavegador -url $url
            $form.ShowDialog() | Out-Null
        }
        elseif ($_opBrowser -eq "N[Compiler]") {
            $processoBrowser = Start-Process -FilePath "$diretorioDll\App\Browser\anguerabook.exe" -PassThru -Wait
            if ($processoBrowser) {
                $processIdBr = $processoBrowser.Id
                "pr4 = $($processIdBr)" | Add-Content -Path "$($diretorioDll)\App\Commands\Proccess\pid.txt"
                Write-Host "ID do processo do navegador: $processIdBr"
            }
            else {
                Write-Host "Falha ao iniciar o processo do navegador."
            }
        }


    }
    else {
        Write-Host("Falha ao iniciar o processo PHP dentro do diretório '$caminhoPHP'." + [Environment]::NewLine)
    }
}
else {
    Write-Host "O diretório $caminhoPHP não existe."
}



# Exibir o formulário
