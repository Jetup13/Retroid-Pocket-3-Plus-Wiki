
$md5     = [Security.Cryptography.HashAlgorithm]::Create('MD5')
$hashes  = @{}
$files   = ls "*.zip"
$logfile = "collisions.log"

Write-Host "Computing MD5 of files ... " -NoNewLine
$files | %{
    $file = [IO.File]::OpenRead($_)
    $bytes = [IO.BinaryReader]::new($file).ReadBytes(4MB)
    $file.Close()
    $hash = ($md5.ComputeHash($bytes)|% ToString X2) -join ''
    if (!$hashes.Contains($hash)) { $hashes[$hash] = [Collections.ArrayList]::new() }
    [void]$hashes[$hash].Add($_.Name)
}
Write-Host "Done"


Set-Content $logfile "$(pwd)"
Add-Content $logfile "Files:  $($files.length)"
Add-Content $logfile "Hashes: $(@($hashes.Keys).length)"

$hashes.Keys | %{
    if (@($hashes[$_]).length -gt 1) {
        Add-Content $logfile  ("$_ COLLISIONS: "+($hashes[$_] -join ', '))
    }
}
