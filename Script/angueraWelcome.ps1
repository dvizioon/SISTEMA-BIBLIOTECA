$diretorioPai = $PWD.Path
Write-Host $diretorioPai

if (-not (Test-Path $diretorioPai)) {
    Write-Host "Erro Ditorio Pai nao Existe $($diretorioPai)"
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "AngueraBook"
$form.Size = New-Object System.Drawing.Size(400, 500)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedSingle"

$imagePath = Join-Path $diretorioPai "Assets\Logo.png"
if (Test-Path $imagePath) {
    $image = [System.Drawing.Image]::FromFile($imagePath)  
    $picturebox = New-Object System.Windows.Forms.PictureBox
    $picturebox.Image = $image
    $picturebox.Size = New-Object Drawing.Size(400, 300)
    $picturebox.SizeMode = "Zoom"
    $picturebox.Location = New-Object Drawing.Point(0, 0)
    $form.Controls.Add($picturebox)
}
else {
    Write-Host "Imagem não encontrada: $imagePath"
}


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
$comboBox.Items.Add("Instalar Banco")
$comboBox.Text = "Instalar"

Add-Type @"
    using System;
    using System.Runtime.InteropServices;

    public class Win32 {
        [DllImport("user32.dll", SetLastError=true)]
        public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);

        [DllImport("user32.dll", SetLastError=true)]
        public static extern IntPtr GetForegroundWindow();
    }
"@



$pidFilePath = "$diretorioPai\Keys\Pid_PS1.txt"
if (-not (Test-Path $pidFilePath)) {
    New-Item -ItemType Directory -Force -Path "$diretorioPai\Keys"
    New-Item -ItemType File -Force -Path $pidFilePath
}

$pid | Out-File -FilePath $pidFilePath -Encoding ASCII -Force

function abriJanela {
    param (
        [string] $option
    )

    if ($option -eq "Instalar") {
        Start-Process powershell.exe -NoNewWindow -ArgumentList "-ExecutionPolicy Bypass", "-File", ".\Script\Config\anguerainstall.ps1"
    }
    elseif ($option -eq "Remover") {
        Start-Process powershell.exe -NoNewWindow -ArgumentList "-ExecutionPolicy Bypass", "-File", ".\Script\Config\angueraremove.ps1"
    }
    elseif ($option -eq "Instalar Banco") {
        Start-Process powershell.exe -NoNewWindow -ArgumentList "-ExecutionPolicy Bypass", "-File", ".\Script\Config\anguerainstallDB.ps1"
    }
    else {
        [System.Windows.Forms.MessageBox]::Show("Item Selecionado Nao Esta na Lista de Argumentacao", "Erro",[System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
    }
    
}

$button = New-Object System.Windows.Forms.Button
$button.Location = New-Object System.Drawing.Point(200, 350) 
$button.Size = New-Object System.Drawing.Size(150, 30)
$button.Text = "Execultar"
$button.Add_Click({
        
        # [System.Windows.Forms.MessageBox]::Show("Selecionado: $($comboBox.SelectedItem)")
        # Write-Host "Host -> Action [$($comboBox.SelectedItem)]"
        # abriJanela -option $comboBox.SelectedItem
        # Write-Host $comboBox.SelectedItem
        if(-not $comboBox.SelectedItem){
            [System.Windows.Forms.MessageBox]::Show("Erro Argumentacao em Branco!", "Erro", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
        }else{
            # [System.Windows.Forms.MessageBox]::Show("Selecionado: $($comboBox.SelectedItem)")
            # Write-Host "Host -> Action [$($comboBox.SelectedItem)]"
            abriJanela -option $comboBox.SelectedItem
        }
    })
$button.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold) 

$form.Controls.Add($label)
$form.Controls.Add($labelCriador)
$form.Controls.Add($comboBox)
$form.Controls.Add($button)
$form.Controls.Add($picturebox)

$form.ShowDialog() | Out-Null
