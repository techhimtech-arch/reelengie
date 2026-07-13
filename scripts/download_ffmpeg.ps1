$Url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
$ZipPath = "backend\ffmpeg.zip"
$ExtractPath = "backend\ffmpeg_temp"
$BinPath = "backend\bin"

Write-Host "Downloading FFmpeg from $Url ..."
Invoke-WebRequest -Uri $Url -OutFile $ZipPath

Write-Host "Extracting FFmpeg..."
Expand-Archive -Path $ZipPath -DestinationPath $ExtractPath -Force

Write-Host "Moving binaries to $BinPath ..."
New-Item -ItemType Directory -Force -Path $BinPath | Out-Null
Copy-Item -Path "$ExtractPath\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" -Destination "$BinPath\ffmpeg.exe" -Force
Copy-Item -Path "$ExtractPath\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe" -Destination "$BinPath\ffprobe.exe" -Force

Write-Host "Cleaning up temporary files..."
Remove-Item -Path $ZipPath -Force
Remove-Item -Path $ExtractPath -Recurse -Force

Write-Host "FFmpeg download complete!"
