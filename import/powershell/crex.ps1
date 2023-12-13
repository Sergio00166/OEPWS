param ([string]$pythonExecutable,[string]$scriptPath,[string]$shortcutPath)
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $pythonExecutable
$shortcut.Arguments = $scriptPath
$shortcut.Save()
