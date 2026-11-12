[CmdletBinding()]
param(
    [string[]]$Agent = @('Claude', 'Codex'),
    [switch]$Apply,
    [switch]$Remove,
    [string]$ConfigRoot = $HOME
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$scriptPath = (Resolve-Path (Join-Path $PSScriptRoot '..\hooks\context-guard\context_guard.py')).Path
if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw 'Python launcher (py) not found. Install Python 3 or adjust the command.'
}

function Ensure-Property($Object, [string]$Name, $Value) {
    if (-not $Object.PSObject.Properties[$Name]) {
        $Object | Add-Member -MemberType NoteProperty -Name $Name -Value $Value
    }
}

$targets = @{
    Claude = @{ Path = '.claude\settings.json'; Events = @('UserPromptSubmit', 'Stop'); Slug = 'claude' }
    Codex = @{ Path = '.codex\hooks.json'; Events = @('UserPromptSubmit', 'PostModelRequest'); Slug = 'codex' }
    Gemini = @{ Path = '.gemini\settings.json'; Events = @('BeforeAgent', 'AfterModel'); Slug = 'gemini' }
}

$selectedAgents = @($Agent | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ } | Select-Object -Unique)
foreach ($name in $selectedAgents) {
    if (-not $targets.ContainsKey($name)) { throw "Unsupported agent: $name" }
    $target = $targets[$name]
    $configFile = Join-Path $ConfigRoot $target.Path
    $settings = if (Test-Path -LiteralPath $configFile) {
        Get-Content -LiteralPath $configFile -Raw -Encoding UTF8 | ConvertFrom-Json
    } else { [pscustomobject]@{} }

    Ensure-Property $settings 'hooks' ([pscustomobject]@{})
    $command = 'py -3 "' + $scriptPath + '" hook --agent ' + $target.Slug
    $changed = $false

    foreach ($eventName in $target.Events) {
        Ensure-Property $settings.hooks $eventName @()
        $groups = @($settings.hooks.$eventName)
        $matched = @($groups | Where-Object {
            $group = $_
            @($group.hooks | Where-Object {
                $_.command -and $_.command -match 'context_guard\.py' -and
                $_.command -match ('--agent\s+' + $target.Slug)
            }).Count -gt 0
        })

        if ($Remove) {
            if ($matched.Count -gt 0) {
                $groups = @($groups | Where-Object {
                    $group = $_
                    @($group.hooks | Where-Object {
                        $_.command -and $_.command -match 'context_guard\.py' -and
                        $_.command -match ('--agent\s+' + $target.Slug)
                    }).Count -eq 0
                })
                $settings.hooks.$eventName = @($groups)
                $changed = $true
            }
        } elseif ($matched.Count -eq 0) {
            $entry = [pscustomobject]@{
                hooks = @([pscustomobject]@{
                    type = 'command'
                    command = $command
                    timeout = 10
                })
            }
            $settings.hooks.$eventName = @($groups) + @($entry)
            $changed = $true
        }
    }

    $action = if ($Remove) { 'remove' } else { 'install' }
    if (-not $changed) {
        Write-Host "[$name] No changes required: $configFile"
        continue
    }
    if (-not $Apply) {
        Write-Host "[$name] PREVIEW $action in $configFile"
        Write-Host "  Events: $($target.Events -join ', ')"
        Write-Host "  Run with -Apply to save. Existing hooks are preserved."
        continue
    }

    $parent = Split-Path -Parent $configFile
    if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
    if (Test-Path $configFile) {
        $backup = $configFile + '.agent-kit.' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '.bak'
        Copy-Item -LiteralPath $configFile -Destination $backup -ErrorAction Stop
        Write-Host "[$name] Backup: $backup"
    }
    $json = $settings | ConvertTo-Json -Depth 60
    $temporary = $configFile + '.agent-kit.tmp'
    Set-Content -LiteralPath $temporary -Value $json -Encoding UTF8
    Move-Item -LiteralPath $temporary -Destination $configFile -Force
    Write-Host "[$name] Done: $action"
}

Write-Host 'Global agent hooks in your actual profile were not changed unless -Apply was provided.'
