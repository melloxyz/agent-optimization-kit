[CmdletBinding()]
param([switch]$Json)

$apps = @('python', 'git', 'rtk', 'headroom', 'graphify', 'claude', 'codex', 'gemini', 'opencode', 'orca')
$rows = @()
foreach ($name in $apps) {
    $tool = Get-Command $name -ErrorAction SilentlyContinue
    $version = $null
    if ($tool) {
        try { $version = (& $name --version 2>&1 | Select-Object -First 1 | Out-String).Trim() }
        catch { $version = 'installed (version unknown)' }
    }
    $rows += [pscustomobject]@{ Tool = $name; Installed = [bool]$tool; Version = $version }
}

$configPaths = @{
    Claude = Join-Path $HOME '.claude\settings.json'
    Codex  = Join-Path $HOME '.codex\hooks.json'
    Gemini = Join-Path $HOME '.gemini\settings.json'
}
$hooks = @()
foreach ($name in @('Claude', 'Codex', 'Gemini')) {
    $path = $configPaths[$name]
    $rtk = $false
    $guard = $false
    if (Test-Path -LiteralPath $path) {
        try {
            $raw = Get-Content -LiteralPath $path -Raw -Encoding UTF8
            $config = $raw | ConvertFrom-Json
            $hooksString = $config.hooks | ConvertTo-Json -Depth 35
            $rtk = $hooksString -match '(?i)\brtk\b|rtk-hook'
            $guard = $hooksString -match 'context_guard\.py'
        } catch { Write-Warning "Cannot parse $name hooks: $($_.Exception.Message)" }
    }
    $hooks += [pscustomobject]@{ Agent = $name; ConfigExists = (Test-Path $path); RTKHook = $rtk; ContextGuard = $guard }
}
$provider = $false
$codexToml = Join-Path $HOME '.codex\config.toml'
if (Test-Path $codexToml) {
    $provider = [bool](Select-String -LiteralPath $codexToml -Pattern '^\s*model_provider\s*=\s*["'']headroom["'']' -Quiet)
}

$report = [pscustomobject]@{
    Timestamp = (Get-Date).ToString('o')
    Tools = $rows
    Hooks = $hooks
    CodexHeadroomProvider = $provider
}
if ($Json) {
    $report | ConvertTo-Json -Depth 6
    return
}
Write-Host 'Agent Optimization Kit | Doctor'
Write-Host '-------------------------------'
$rows | Format-Table Tool, Installed, Version -AutoSize | Out-Host
Write-Host 'Hook integrations (metadata only; no secret values)'
$hooks | Format-Table Agent, ConfigExists, RTKHook, ContextGuard -AutoSize | Out-Host
Write-Host "Codex routed through Headroom config: $provider"
Write-Host 'No configuration was modified.'
