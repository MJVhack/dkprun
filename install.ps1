Param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl
)

$targetDir = "C:\dkprun"

Write-Host "Cloning repo $RepoUrl into $targetDir"
if (Test-Path $targetDir) {
    Remove-Item $targetDir -Recurse -Force
}
git clone $RepoUrl $targetDir

if (-not (Test-Path "$targetDir\dkprun.py")) {
    Write-Host "dkprun.py not found in the repo." -ForegroundColor Red
    exit 1
}
if (-not (Test-Path "$targetDir\dkprun.bat")) {
    Write-Host "dkprun.bat not found in the repo." -ForegroundColor Red
    exit 2
}

Write-Host "Files found in $targetDir"

# Add the folder to the system PATH
$envName = "PATH"
try {
    $envValue = [Environment]::GetEnvironmentVariable($envName, [EnvironmentVariableTarget]::Machine)
    if ([string]::IsNullOrEmpty($envValue)) {
        $newValue = "$targetDir"
    } else {
        $newValue = "$envValue;$targetDir"
    }
    if ($envValue -notlike "*$targetDir*") {
        Write-Host "Adding $targetDir to Windows PATH..."
        [Environment]::SetEnvironmentVariable($envName, $newValue, [EnvironmentVariableTarget]::Machine)
        Write-Host "PATH updated (system). Restart your terminal to apply the changes."
    } else {
        Write-Host "$targetDir is already in PATH."
    }
} catch {
    Write-Host "Error while updating system PATH. Please run this script as administrator." -ForegroundColor Red
    exit 3
}

Write-Host "Installation complete!"
} else {
    Write-Host "ℹ️ $targetDir est déjà dans le PATH."
}

Write-Host "✅ Installation terminée !"
