[CmdletBinding()]
param([switch]$Json)

function Get-Output([string]$Name, [string[]]$Arguments) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { return $null }
    try { return ((& $Name @Arguments 2>&1) | Out-String) }
    catch { return $null }
}

$rtk = Get-Output 'rtk' @('gain')
$headroom = Get-Output 'headroom' @('savings')
$rtkCommands = $null
$rtkSaved = $null
$rtkReduction = $null
if ($rtk) {
    if ($rtk -match 'Total commands:\s*([\d,]+)') { $rtkCommands = $Matches[1] }
    if ($rtk -match 'Tokens saved:\s*([\d.,]+[KMB]?)\s*\(([\d.]+)%\)') {
        $rtkSaved = $Matches[1]
        $rtkReduction = $Matches[2]
    }
}
$headroomSaved = $null
$headroomReduction = $null
$headroomNewInputReduction = $null
if ($headroom) {
    $monthLine = ($headroom -split "\r?\n" | Where-Object { $_ -match '^\s*Last 30 days' } | Select-Object -First 1)
    if ($monthLine -match 'saved\s*([\d,]+)\s*/') { $headroomSaved = $Matches[1] }
    if ($monthLine -match '([\d.]+)%\s+saved') { $headroomReduction = $Matches[1] }
    if ($monthLine -match 'of new input\s+([\d.]+)%') { $headroomNewInputReduction = $Matches[1] }
}
$report = [pscustomobject]@{
    Timestamp = (Get-Date).ToString('o')
    RTK = [pscustomobject]@{ Scope = 'Lifetime global'; Commands = $rtkCommands; Saved = $rtkSaved; ReductionPercent = $rtkReduction }
    Headroom = [pscustomobject]@{ Scope = 'Last 30 days'; Saved = $headroomSaved; TotalInputReductionPercent = $headroomReduction; NewInputReductionPercent = $headroomNewInputReduction }
    Note = 'Metrics are different scopes and denominators. Do not add savings or interpret as plan quota.'
}
if ($Json) { $report | ConvertTo-Json -Depth 5; return }
Write-Host 'Agent Optimization Kit | Savings'
Write-Host '--------------------------------'
Write-Host "RTK      | $($report.RTK.Saved) tokens saved | $($report.RTK.ReductionPercent)% output reduction | $($report.RTK.Commands) commands (lifetime)"
Write-Host "Headroom | $($report.Headroom.Saved) tokens saved | $($report.Headroom.NewInputReductionPercent)% of new input (last 30 days)"
Write-Host ''
Write-Host 'Not additive: separate measurement bases and time periods.'
if (-not $rtk -or -not $headroom) { Write-Warning 'One or more source tools are unavailable; missing metrics are not estimated.' }
