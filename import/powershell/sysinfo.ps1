$computerSystem = Get-WmiObject -Class Win32_ComputerSystem
$operatingSystem = Get-CimInstance Win32_OperatingSystem
$biosInfo = Get-WmiObject -Class Win32_BIOS

$uptime = (Get-Date) - $operatingSystem.LastBootUpTime

$computerSystem.Name
$operatingSystem.Caption
$operatingSystem.BuildNumber
"{0:D1}:{1:D2}:{2:D2}:{3:D2}" -f $uptime.Days, $uptime.Hours, $uptime.Minutes, $uptime.Seconds
$computerSystem.PrimaryOwnerName
$computerSystem.Workgroup
$computerSystem.Manufacturer
$computerSystem.Model
wmic cpu get name
$biosInfo.Name
$biosInfo.Version
(Get-TimeZone).DisplayName
(Get-Culture).Name
(Get-CimInstance -ClassName Win32_VideoController).Name
