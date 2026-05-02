# Pipeline di release: build PyInstaller -> zip -> tag git -> GitHub Release.
#
# Uso:
#   .\scripts\release.ps1 -Version v1.1
#   .\scripts\release.ps1 -Version v1.1 -SkipTag       # solo build + zip + upload
#   .\scripts\release.ps1 -Version v1.1 -DryRun        # mostra i passi, nulla viene eseguito
#
# Prerequisiti: working tree pulito, branch main, gh CLI autenticato,
# .venv con PyInstaller installato.

param(
    [Parameter(Mandatory=$true)]
    [string]$Version,
    [switch]$SkipTag,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$Repo = Split-Path -Parent $PSScriptRoot
$Gh = "C:\Program Files\GitHub CLI\gh.exe"
$Python = Join-Path $Repo ".venv\Scripts\python.exe"
$ZipName = "CamperAppPlus_${Version}_windows.zip"
$ZipPath = Join-Path $Repo "dist\$ZipName"
$BundleDir = Join-Path $Repo "dist\CamperAppPlus"

function Step([string]$msg) {
    Write-Host ""
    Write-Host "==> $msg" -ForegroundColor Cyan
}

function Run([scriptblock]$cmd, [string]$desc) {
    if ($DryRun) {
        Write-Host "[dry-run] $desc" -ForegroundColor Yellow
        return
    }
    & $cmd
    if ($LASTEXITCODE -ne 0) {
        throw "Step fallito: $desc (exit $LASTEXITCODE)"
    }
}

Set-Location $Repo

# ---------- Pre-flight ----------
Step "Controllo prerequisiti"

if (-not (Test-Path $Python)) { throw "Python venv non trovato in $Python" }
if (-not (Test-Path $Gh))     { throw "gh CLI non trovata in $Gh" }

$status = git status --porcelain
if ($status -and -not $DryRun) {
    Write-Host $status
    throw "Working tree non pulito. Committa o stasha prima di rilasciare."
}

$branch = (git branch --show-current).Trim()
if ($branch -ne "main") {
    throw "Non sei su 'main' (branch corrente: '$branch')."
}

# Tag esistente? Evita riscritture accidentali.
$existingTag = git tag -l $Version
if ($existingTag -and -not $SkipTag) {
    throw "Tag $Version esiste gia'. Usa -SkipTag se vuoi solo ricaricare l'asset."
}

Write-Host "Repo:    $Repo"
Write-Host "Version: $Version"
Write-Host "Zip:     $ZipPath"

# ---------- 1. Build ----------
Step "Build PyInstaller"
Run { & $Python -m PyInstaller --noconfirm --clean CamperAppPlus.spec } "PyInstaller build"

if (-not $DryRun -and -not (Test-Path "$BundleDir\CamperAppPlus.exe")) {
    throw "Build non ha prodotto CamperAppPlus.exe in $BundleDir"
}

# ---------- 2. Zip ----------
Step "Creazione zip"
if (Test-Path $ZipPath) {
    Run { Remove-Item $ZipPath -Force } "Remove old zip"
}
Run {
    Compress-Archive -Path $BundleDir -DestinationPath $ZipPath -CompressionLevel Optimal
} "Compress-Archive -> $ZipName"

if (-not $DryRun) {
    $size = (Get-Item $ZipPath).Length
    Write-Host ("Zip creato: {0:N0} byte ({1:N1} MB)" -f $size, ($size / 1MB))
}

# ---------- 3. Tag git + push ----------
if (-not $SkipTag) {
    Step "Creazione tag $Version e push"
    Run { git tag -a $Version -m "CAMPERappPLUS $Version" } "git tag $Version"
    Run { git push origin $Version } "git push origin $Version"
} else {
    Write-Host "Skip tag (flag -SkipTag attivo)"
}

# ---------- 4. GitHub Release ----------
Step "Creazione GitHub Release"
$releaseExists = $false
if (-not $DryRun) {
    & $Gh release view $Version *> $null
    if ($LASTEXITCODE -eq 0) { $releaseExists = $true }
}

if ($releaseExists) {
    Write-Host "Release $Version gia' esistente: aggiorno l'asset (--clobber)."
    Run { & $Gh release upload $Version $ZipPath --clobber } "gh release upload --clobber"
} else {
    Run {
        & $Gh release create $Version $ZipPath `
            --title "CAMPERappPLUS $Version" `
            --generate-notes
    } "gh release create $Version"
}

# ---------- Done ----------
Step "Done"
if (-not $DryRun) {
    & $Gh release view $Version --json url -q .url
    Write-Host "Apri la release nel browser? (gh release view $Version --web)" -ForegroundColor Green
}
