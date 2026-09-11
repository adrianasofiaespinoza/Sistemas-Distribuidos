Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Start CMD with a command
$proc = Start-Process cmd.exe -ArgumentList '/c', 'nslookup yachaytech.edu.ec 8.8.8.8 & pause' -PassThru
Start-Sleep -Seconds 2

# Screen dimensions
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)

$outputPath = "c:\Users\User\Desktop\8vo\Sistemas-Distribuidos\Sistemas-Distribuidos\Workshop4\imagenes\test_real_cmd.png"
$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bitmap.Dispose()

if ($proc -and -not $proc.HasExited) {
    Stop-Process -Id $proc.Id -Force
}

Write-Host "Real screen capture saved to $outputPath"
