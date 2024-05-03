
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing


$form = New-Object System.Windows.Forms.Form
$form.Text = "AngueraBook"
$form.Size = New-Object System.Drawing.Size(400, 500)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedSingle"

$image = [System.Drawing.Image]::FromFile("./Assets/Logo.png")  
$picturebox = New-Object Windows.Forms.PictureBox
$picturebox.Image = $image
$picturebox.Size = New-Object Drawing.Size(400, 300)
$picturebox.SizeMode = "Zoom"
$picturebox.Location = New-Object Drawing.Point(0, 0)

$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(0, 270) 
$label.Size = New-Object System.Drawing.Size(400, 50)  
$label.TextAlign = "MiddleCenter"
$label.Text = "Instalador AngueraBook!"
$label.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)  


$labelCriador = New-Object System.Windows.Forms.Label
$labelCriador.Location = New-Object System.Drawing.Point(0, 400) 
$labelCriador.Size = New-Object System.Drawing.Size(400, 50)  
$labelCriador.TextAlign = "MiddleCenter"
$labelCriador.Text = "Suporte:danielmartinsjob@gmail.com"
$labelCriador.Font = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)  



$comboBox = New-Object System.Windows.Forms.ComboBox
$comboBox.Location = New-Object System.Drawing.Point(20, 350)
$comboBox.Size = New-Object System.Drawing.Size(170, 50)
$comboBox.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold) 

$comboBox.Items.Add("Instalar")
$comboBox.Items.Add("Remover")
$comboBox.Items.Add("Ferramentas")

$comboBox.Text = "Instalar"

function abriJanela {
    param (
        [string] $option
    )

    if ($option -eq "Instalar") {
        Start-Process powershell.exe -NoNewWindow "./Script/Config/anguerainstall.ps1"
        $form.Close()
    }
    elseif ($option -eq "Remover") {
        Start-Process powershell.exe -NoNewWindow "./Script/Config/angueraremove.ps1"
        $form.Close()
    }
    
}

$button = New-Object System.Windows.Forms.Button
$button.Location = New-Object System.Drawing.Point(200, 350) 
$button.Size = New-Object System.Drawing.Size(150, 30)
$button.Text = "Execultar"
$button.Add_Click({
        
        # [System.Windows.Forms.MessageBox]::Show("Selecionado: $($comboBox.SelectedItem)")
        Write-Host "Host -> Action [$($comboBox.SelectedItem)]"
        abriJanela -option $comboBox.SelectedItem
    })
$button.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold) 

$form.Controls.Add($label)
$form.Controls.Add($labelCriador)
$form.Controls.Add($comboBox)
$form.Controls.Add($button)
$form.Controls.Add($picturebox)

$form.ShowDialog() | Out-Null
