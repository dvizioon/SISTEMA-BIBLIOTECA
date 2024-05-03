
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing



function RemoverAll {
    param (
        [string]$caminho
    )

    try {

        # Obter todos os arquivos e diretorios dentro do diretorio e seus subdiretorios até três níveis de profundidade
        $itens = Get-ChildItem -Path $caminho -Recurse -Depth 3

        $msg = "Deseja realmente remover todos os arquivos e diretorios encontrados?"
        $titulo = "Confirmacao de Remocao"
        $icon = [System.Windows.Forms.MessageBoxIcon]::Question
        $botoes = [System.Windows.Forms.MessageBoxButtons]::YesNo

        $resultado = [System.Windows.Forms.MessageBox]::Show($msg, $titulo, $botoes, $icon)

        if ($resultado -eq "Yes") {

            $unidade = $env:SystemDrive
            $pasta = "VersionPHP"
  
            $caminho = Join-Path -Path $unidade -ChildPath $pasta

            # Define o caminho a ser removido do PATH
            $caminhoPasta = $caminho
            $valor_destino = "php5.4.0"

            # Obtém o valor atual do PATH do usuário
            $pathAtual = [System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::User)

            # Verifica se o caminho a ser removido está presente no PATH
            if ($pathAtual -like "*$caminhoPasta\$valor_destino*") {
                # Remove o caminho desejado do PATH
                $novoPath = $pathAtual -replace [regex]::Escape("$caminhoPasta\$valor_destino"), ""
                $novoPath = $novoPath -replace ";;", ";"  # Remove quaisquer ocorrências extras de ponto e vírgula
                $novoPath = $novoPath.TrimEnd(";")  # Remove ponto e vírgula no final do caminho, se houver
                # Define o novo valor do PATH
                [System.Environment]::SetEnvironmentVariable("PATH", $novoPath, [System.EnvironmentVariableTarget]::User)
                Write-Host "O caminho foi removido com sucesso do PATH."
                $textBox_logs.AppendText("O caminho foi removido com sucesso do PATH $([Environment]::NewLine)")
            }
            else {
                Write-Host "O caminho não está presente no PATH."
                $textBox_logs.AppendText("O caminho não está presente no PATH. $([Environment]::NewLine)")
            }


            if (Test-Path -Path $caminho -PathType Container) {
                # Se a pasta existe, remova-a
                Remove-Item -Path $caminho -Recurse -Force
                Write-Host "A pasta $pasta foi removida com sucesso."
                $textBox_logs.AppendText("A pasta foi removida com sucesso => $($pasta + [Environment]::NewLine)")
                $textBox_logs.AppendText("Caminho da Pasta foi removida com sucesso => $($caminho + [Environment]::NewLine)")
            }
            else {
                $textBox_logs.AppendText("A pasta não existe => $($pasta + [Environment]::NewLine)")
                Write-Host "A pasta $pasta não existe."
            }

            foreach ($item in $itens) {
                if ($item -is [System.IO.FileInfo]) {
                    $textBox_logs.ForeColor = "Green"
                    $textBox_logs.AppendText("Encontrado arquivo => $($item.FullName + [Environment]::NewLine)")

                    # Remover arquivo
                    Remove-Item -Path $item.FullName -Force -ErrorAction Stop

                    $form.Close()
                }
                elseif ($item -is [System.IO.DirectoryInfo]) {
                    $textBox_logs.ForeColor = "Green"
                    $textBox_logs.AppendText("Encontrado diretorio => $($item.FullName + [Environment]::NewLine)")

                    # Remover diretorio
                    Remove-Item -Path $item.FullName -Recurse -Force -ErrorAction Stop
                }
            }

            Start-Sleep -Milliseconds 1000

            # Verificar se há arquivos ou diretorios restantes
            if ((Get-ChildItem -Path $caminho -Recurse -Depth 3).Count -eq 0) {
                Write-Host "Todos os arquivos e diretorios foram removidos com sucesso."
            }
            else {
                Write-Host "Alguns arquivos ou diretorios nao puderam ser removidos."
            }
        }
        else {
            Write-Host "Operacao cancelada pelo usuário."
        }
    }
    catch {
        Write-Host "Erro ao acessar o diretorio: $_"
    }
}




# Cria uma nova janela
$form = New-Object System.Windows.Forms.Form
$form.Text = "Uninstall angueraBooks"
$form.Size = New-Object System.Drawing.Size(440, 380)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedSingle"

# Cria um controle TabControl para as abas
$tabControl = New-Object System.Windows.Forms.TabControl
$tabControl.Size = New-Object System.Drawing.Size(400, 330)
$tabControl.Location = New-Object System.Drawing.Point(10, 10)
$form.Controls.Add($tabControl)


# Criar a aba "Deletar Sistema"
$tab1 = New-Object System.Windows.Forms.TabPage
$tab1.Text = "Deletar Sistema"

# Adicionar a aba ao controle de abas
$tabControl.Controls.Add($tab1)

# Criar uma area scrollavel
$scrollablePanel = New-Object System.Windows.Forms.Panel
$scrollablePanel.Dock = [System.Windows.Forms.DockStyle]::Fill  
$scrollablePanel.AutoScroll = $true

# Adicionar a area scrollavel à aba
$tab1.Controls.Add($scrollablePanel)

# Criar o botao "Remover Todo o Sistema"
$button_remover_sistema = New-Object System.Windows.Forms.Button
$button_remover_sistema.Text = "Deletar Sys"
$button_remover_sistema.Size = New-Object System.Drawing.Size(100, 30) 
$button_remover_sistema.Location = New-Object System.Drawing.Point(20, 20)  


$button_remover_sistema.Add_Click({ RemoverAll -caminho "." })
$scrollablePanel.Controls.Add($button_remover_sistema)

# Criar o botao "Resetar o Banco de Dados"
$button_resetar_banco = New-Object System.Windows.Forms.Button
$button_resetar_banco.Text = "Resete DB"
$button_resetar_banco.Size = New-Object System.Drawing.Size(100, 30) 
$button_resetar_banco.Location = New-Object System.Drawing.Point(130, 20)   
$scrollablePanel.Controls.Add($button_resetar_banco)

# Criar o botao "Checar DLL"
$button_checar_dll = New-Object System.Windows.Forms.Button
$button_checar_dll.Text = "Checar DLL"
$button_checar_dll.Size = New-Object System.Drawing.Size(100, 30) 
$button_checar_dll.Location = New-Object System.Drawing.Point(240, 20) 
$scrollablePanel.Controls.Add($button_checar_dll)

# Criar o controle de texto (TextBox) para exibir logs
$textBox_logs = New-Object System.Windows.Forms.TextBox
$textBox_logs.Multiline = $true  
$textBox_logs.ScrollBars = "Vertical"  
$textBox_logs.Width = 360
$textBox_logs.Height = 200
$textBox_logs.Location = New-Object System.Drawing.Point(20, 80)  
$scrollablePanel.Controls.Add($textBox_logs)


$form.ShowDialog() | Out-Null

