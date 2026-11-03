# PowerShell Installer for corporate-latex-plugin
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  Antigravity Corporate LaTeX Suite & Plugin Installer (PS5/PS7)" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$DestDir = Join-Path $HOME ".gemini\config\plugins\corporate-latex-plugin"
$SrcDir = $PSScriptRoot

Write-Host "`n[1/3] Copying plugin to: $DestDir" -ForegroundColor Yellow
if (!(Test-Path $DestDir)) { New-Item -ItemType Directory -Path $DestDir -Force | Out-Null }

foreach ($folder in @(".gemini-plugin", "skills", "scripts", "tests")) {
    $src = Join-Path $SrcDir $folder
    $dest = Join-Path $DestDir $folder
    if (Test-Path $src) {
        if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
        Copy-Item -Path $src -Destination $dest -Recurse -Force
        Write-Host "  - Copied $folder/" -ForegroundColor Green
    }
}

Write-Host "`n[2/3] Checking pdflatex..." -ForegroundColor Yellow
try {
    $latexVer = pdflatex --version
    Write-Host "  [OK] pdflatex is installed." -ForegroundColor Green
} catch {
    Write-Host "  [WARN] pdflatex not found in PATH." -ForegroundColor DarkYellow
}

Write-Host "`n[3/3] Installation Complete! The skill 'corporate-latex' is now active." -ForegroundColor Green
