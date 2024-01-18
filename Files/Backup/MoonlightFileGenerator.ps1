# Add this file to the same folder as the Moonlight.ini
# eg C:\Users\yourusername\Downloads\MoonlightPortable-x64-5.0.1\Moonlight Game Streaming Project

# Ini path
$iniPath = ".\Moonlight.ini"

# Read the contents of the ini file
$iniContent = Get-Content $iniPath

# Create the new directory
$newDirPath = ".\Daijishou-launchers-temp"
New-Item -Path $newDirPath -ItemType Directory -Force

# Parse the ini file and create .moonlight files
$creating = $false
$appName = $null
foreach ($line in $iniContent) {
    if ($line -match "^\[hosts\]") {
        $creating = $true
    }
    elseif ($creating -and $line -match "1\\apps\\(\d+)\\name=(.*)") {
        $appName = $Matches[2]
    }
    elseif ($appName -and $line -match "1\\apps\\(\d+)\\id=(\d+)") {
        $appId = $Matches[2]
        $moonlightContent = "# Daijishou Player Template`r`n[moonlight_id] $appId"
        $fileName = "$appName.moonlight"
        $fileName = $fileName -replace '[\\\/:*?"<>|]', '' # Remove illegal characters for file names
        $filePath = Join-Path $newDirPath $fileName
        $moonlightContent | Out-File -FilePath $filePath
        $appName = $null # Reset app name for next entry
    }
    elseif ($line -match "^\[") {
        $creating = $false
    }
}

# Output message
Write-Host "Moonlight files created in $newDirPath"