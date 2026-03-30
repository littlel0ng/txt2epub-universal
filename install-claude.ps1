param(
    [string]$ClaudeHome = "$env:APPDATA\Claude"
)

$ErrorActionPreference = 'Stop'
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceSkill = Join-Path $ScriptRoot 'skill\txt2epub'
$TargetRoot = Join-Path $ClaudeHome 'skills'
$TargetSkill = Join-Path $TargetRoot 'txt2epub'

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
if (Test-Path $TargetSkill) {
    Remove-Item -Recurse -Force -LiteralPath $TargetSkill
}
Copy-Item -Recurse -Force -LiteralPath $SourceSkill -Destination $TargetSkill
Write-Host 'Installed txt2epub to' $TargetSkill
