# AI Testing Script for PKM Backend (PowerShell)
# Quick automated testing of all AI features

param(
    [string]$BaseUrl = "http://localhost:8000",
    [switch]$Verbose
)

$ProgressPreference = 'SilentlyContinue'

function Write-TestResult {
    param($TestName, $Success, $ResponseTime, $Error = $null)
    
    $status = if ($Success) { "✅" } else { "❌" }
    $timeStr = "{0:F2}s" -f $ResponseTime
    
    Write-Host "$status $TestName ($timeStr)" -ForegroundColor $(if ($Success) { "Green" } else { "Red" })
    
    if (-not $Success -and $Error) {
        Write-Host "   Error: $Error" -ForegroundColor Red
    }
}

function Test-AIFeature {
    param($Endpoint, $Body, $TestName)
    
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    
    try {
        $response = Invoke-RestMethod -Uri "$BaseUrl$Endpoint" -Method POST -Body $Body -ContentType "application/json" -ErrorAction Stop
        $stopwatch.Stop()
        
        $success = $response.success -eq $true
        $responseTime = $stopwatch.Elapsed.TotalSeconds
        
        Write-TestResult -TestName $TestName -Success $success -ResponseTime $responseTime -Error $response.error
        
        if ($Verbose -and $success -and $response.response) {
            $preview = $response.response.Substring(0, [Math]::Min(100, $response.response.Length))
            Write-Host "   Preview: $preview..." -ForegroundColor DarkGray
        }
        
        return @{
            Success = $success
            ResponseTime = $responseTime
            ModelUsed = $response.model_used
            Error = $response.error
        }
    }
    catch {
        $stopwatch.Stop()
        $responseTime = $stopwatch.Elapsed.TotalSeconds
        
        Write-TestResult -TestName $TestName -Success $false -ResponseTime $responseTime -Error $_.Exception.Message
        
        return @{
            Success = $false
            ResponseTime = $responseTime
            ModelUsed = "unknown"
            Error = $_.Exception.Message
        }
    }
}

# Main testing function
Write-Host "🤖 AI Features Testing Suite" -ForegroundColor Blue
Write-Host "================================" -ForegroundColor Blue

# Check if server is running
try {
    $healthCheck = Invoke-RestMethod -Uri "$BaseUrl/health" -Method GET -ErrorAction Stop
    Write-Host "✅ Server is running" -ForegroundColor Green
}
catch {
    Write-Host "❌ Server is not running at $BaseUrl" -ForegroundColor Red
    Write-Host "Please start the server first: uv run uvicorn pkm_backend.main:app --reload" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Test 1: AI Rephrase (Academic)
$body1 = @{
    text = "This code is buggy and needs fixing badly"
    style = "academic"
} | ConvertTo-Json

$result1 = Test-AIFeature -Endpoint "/api/v1/ai/rephrase" -Body $body1 -TestName "AI Rephrase (Academic)"

# Test 2: AI Rephrase (Professional)
$body2 = @{
    text = "The algorithm sucks and is slow"
    style = "professional"
} | ConvertTo-Json

$result2 = Test-AIFeature -Endpoint "/api/v1/ai/rephrase" -Body $body2 -TestName "AI Rephrase (Professional)"

# Test 3: AI Chat (General)
$body3 = @{
    message = "Explain time complexity in algorithms briefly"
    note_ids = @()
} | ConvertTo-Json

$result3 = Test-AIFeature -Endpoint "/api/v1/ai/chat" -Body $body3 -TestName "AI Chat (General)"

# Test 4: AI Chat (With Notes)
try {
    $notes = Invoke-RestMethod -Uri "$BaseUrl/api/v1/notes/" -Method GET -ErrorAction Stop
    $noteIds = @($notes | Select-Object -First 2 -ExpandProperty id)
}
catch {
    $noteIds = @()
}

$body4 = @{
    message = "What are the key concepts mentioned in these notes?"
    note_ids = $noteIds
} | ConvertTo-Json

$result4 = Test-AIFeature -Endpoint "/api/v1/ai/chat" -Body $body4 -TestName "AI Chat (With Notes)"

# Test 5: AI Note Cleanup
$body5 = @{
    note_id = 1
    instructions = "Improve grammar and make it more professional"
} | ConvertTo-Json

$result5 = Test-AIFeature -Endpoint "/api/v1/ai/cleanup" -Body $body5 -TestName "AI Note Cleanup"

# Generate Report
Write-Host ""
Write-Host "📊 Testing Report" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

$allResults = @($result1, $result2, $result3, $result4, $result5)
$totalTests = $allResults.Count
$passedTests = ($allResults | Where-Object { $_.Success }).Count
$avgResponseTime = ($allResults | Measure-Object -Property ResponseTime -Average).Average

Write-Host "Summary:"
Write-Host "  Total Tests: $totalTests"
Write-Host "  Passed: $passedTests"
Write-Host "  Failed: $($totalTests - $passedTests)"
Write-Host "  Success Rate: $([Math]::Round(($passedTests/$totalTests)*100, 1))%"
Write-Host "  Average Response Time: $([Math]::Round($avgResponseTime, 2))s"

$models = $allResults | Where-Object { $_.Success } | Select-Object -ExpandProperty ModelUsed -Unique
if ($models) {
    Write-Host "  Models Used: $($models -join ', ')"
}

# Exit with appropriate code
$failedTests = $totalTests - $passedTests
if ($failedTests -eq 0) {
    Write-Host "`n🎉 All tests passed!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  $failedTests test(s) failed" -ForegroundColor Yellow
}

exit $failedTests