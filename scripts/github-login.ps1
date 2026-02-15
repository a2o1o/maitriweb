<# 
  Ensures GitHub CLI authentication is set up for this machine.

  Usage:
    powershell -ExecutionPolicy Bypass -File .\scripts\github-login.ps1

  Notes:
  - Prefers HTTPS + Git Credential Manager ("web" flow).
  - Safe to re-run; it will no-op if already logged in.
#>

[CmdletBinding()]
param(
  [ValidateSet("github.com","github.mit.edu")]
  [string] $HostName = "github.com"
)

$ErrorActionPreference = "Stop"

function Require-Command([string] $Name) {
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Missing required command '$Name'. Install GitHub CLI (gh) and retry."
  }
}

Require-Command "gh"

try {
  $status = gh auth status -h $HostName 2>&1
  if ($LASTEXITCODE -eq 0) {
    Write-Host "Already authenticated to $HostName."
    exit 0
  }
} catch {
  # Continue to login flow
}

Write-Host "Starting GitHub CLI login for $HostName..."
Write-Host "If prompted: choose HTTPS, then authenticate via browser."

gh auth login -h $HostName -p https -w
if ($LASTEXITCODE -ne 0) { throw "gh auth login failed (exit $LASTEXITCODE)." }

gh auth status -h $HostName | Out-Host

