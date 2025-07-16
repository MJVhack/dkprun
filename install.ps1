Param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl
)

$targetDir = "C:\dkprun"

Write-Host "🚀 Clonage du repo $RepoUrl dans $targetDir"
if (Test-Path $targetDir) {
    Remove-Item $targetDir -Recurse -Force
}
git clone $RepoUrl $targetDir

if (-not (Test-Path "$targetDir\dkprun.py")) {
    Write-Host "❌ dkprun.py introuvable dans le repo." -ForegroundColor Red
    exit 1
}
if (-not (Test-Path "$targetDir\dkprun.bat")) {
    Write-Host "❌ dkprun.bat introuvable dans le repo." -ForegroundColor Red
    exit 2
}

Write-Host "✅ Fichiers trouvés dans $targetDir"

# Ajout du dossier au PATH système
$envName = "PATH"
$envValue = [Environment]::GetEnvironmentVariable($envName, [EnvironmentVariableTarget]::Machine)
if ($envValue -notlike "*$targetDir*") {
    Write-Host "🔧 Ajout de $targetDir au PATH Windows..."
    $newValue = "$envValue;$targetDir"
    [Environment]::SetEnvironmentVariable($envName, $newValue, [EnvironmentVariableTarget]::Machine)
    Write-Host "✅ PATH mis à jour (système). Redémarre le terminal pour que les changements soient pris en compte."
} else {
    Write-Host "ℹ️ $targetDir est déjà dans le PATH."
}

Write-Host "✅ Installation terminée !"