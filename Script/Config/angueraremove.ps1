
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -Path 'System Dll/System.Data.SQLite.dll'

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

# Criar uma área scrollável
$scrollablePanel = New-Object System.Windows.Forms.Panel
$scrollablePanel.Dock = [System.Windows.Forms.DockStyle]::Fill  
$scrollablePanel.AutoScroll = $true

# Adicionar a área scrollável à aba
$tab1.Controls.Add($scrollablePanel)

# Criar o botão "Remover Todo o Sistema"
$button_remover_sistema = New-Object System.Windows.Forms.Button
$button_remover_sistema.Text = "Deletar Sys"
$button_remover_sistema.Size = New-Object System.Drawing.Size(100, 30) 
$button_remover_sistema.Location = New-Object System.Drawing.Point(20, 20)  
$scrollablePanel.Controls.Add($button_remover_sistema)

# Criar o botão "Resetar o Banco de Dados"
$button_resetar_banco = New-Object System.Windows.Forms.Button
$button_resetar_banco.Text = "Resete DB"
$button_resetar_banco.Size = New-Object System.Drawing.Size(100, 30) 
$button_resetar_banco.Location = New-Object System.Drawing.Point(130, 20)   
$scrollablePanel.Controls.Add($button_resetar_banco)

# Criar o botão "Checar DLL"
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

