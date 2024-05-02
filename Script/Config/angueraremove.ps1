
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


$tab1 = New-Object System.Windows.Forms.TabPage
$tab1.Text = "Deletar Sistema"
$tabControl.Controls.Add($tab1)


$form.ShowDialog() | Out-Null

