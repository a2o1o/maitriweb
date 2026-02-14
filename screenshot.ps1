param(
  [string]$Url = "http://localhost:8080/",
  [string]$OutDir = "$PSScriptRoot\\_shots",
  [ValidateSet("auto","edge","chrome")]
  [string]$Browser = "auto"
)

$edge = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
if (-not (Test-Path $edge)) {
  $edge = "$env:ProgramFiles(x86)\\Microsoft\\Edge\\Application\\msedge.exe"
}
if (-not (Test-Path $edge)) {
  $edge = "$env:ProgramFiles\\Microsoft\\Edge\\Application\\msedge.exe"
}

$chrome = "$env:ProgramFiles\\Google\\Chrome\\Application\\chrome.exe"
if (-not (Test-Path $chrome)) { $chrome = "$env:ProgramFiles(x86)\\Google\\Chrome\\Application\\chrome.exe" }

$bin = $null
if ($Browser -eq "edge" -or ($Browser -eq "auto" -and (Test-Path $edge))) {
  $bin = $edge
} elseif ($Browser -eq "chrome" -or ($Browser -eq "auto" -and (Test-Path $chrome))) {
  $bin = $chrome
}

if (-not $bin -or -not (Test-Path $bin)) {
  throw "Browser not found. Set -Browser edge/chrome or update paths in screenshot.ps1."
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$out = Join-Path $OutDir ("home-" + $stamp + ".png")

# Chromium headless on locked-down Windows machines can fail with sandbox ACL operations.
# Use a repo-local profile dir to avoid corporate TEMP/AppContainer ACL issues.
$profile = Join-Path $OutDir ("profile-" + $stamp)
New-Item -ItemType Directory -Force -Path $profile | Out-Null

# Note: if the page depends on fonts loading, you can add a longer virtual-time budget.
$common = @(
  "--disable-gpu",
  "--hide-scrollbars",
  "--no-first-run",
  "--no-default-browser-check",
  "--disable-crash-reporter",
  "--disable-features=Crashpad,NetworkServiceSandbox,WinSboxAppContainer,RendererAppContainer,NetworkService",
  "--disable-background-networking",
  "--no-sandbox",
  "--disable-dev-shm-usage",
  "--disable-breakpad",
  "--virtual-time-budget=2500",
  "--window-size=1440,900",
  "--screenshot=$out",
  "--user-data-dir=$profile",
  $Url
)

# Headless can fail intermittently on locked-down Windows environments. Try a couple variants.
& $bin @("--headless=new") @common | Out-Null
if (-not (Test-Path $out)) {
  & $bin @("--headless") @common | Out-Null
}

if (-not (Test-Path $out)) {
  throw "Screenshot failed: file was not created at $out"
}

Write-Output $out
