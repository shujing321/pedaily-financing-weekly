$ErrorActionPreference = 'Stop'
$Target = Join-Path (if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }) 'skills/pedaily-financing-weekly'
$Temp = Join-Path ([System.IO.Path]::GetTempPath()) ('pedaily-' + [guid]::NewGuid())
New-Item -ItemType Directory -Force -Path $Temp | Out-Null
try {
  Invoke-WebRequest 'https://github.com/zhichunyang/pedaily-financing-weekly/archive/refs/heads/main.zip' -OutFile (Join-Path $Temp 'skill.zip')
  Expand-Archive (Join-Path $Temp 'skill.zip') -DestinationPath $Temp
  New-Item -ItemType Directory -Force -Path (Split-Path $Target) | Out-Null
  if (Test-Path $Target) { Remove-Item -Recurse -Force $Target }
  Copy-Item -Recurse (Join-Path $Temp 'pedaily-financing-weekly-main/pedaily-financing-weekly') $Target
  Write-Host "Installed to: $Target"
} finally {
  Remove-Item -Recurse -Force $Temp -ErrorAction SilentlyContinue
}
