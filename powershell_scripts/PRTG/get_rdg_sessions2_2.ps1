

$User = "Administrator"
$PasswordFile = "$PSScriptRoot\Password.txt"
$KeyFile = "$PSScriptRoot\AES.key"
$key = Get-Content $KeyFile
$MyCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, (Get-Content $PasswordFile | ConvertTo-SecureString -Key $key)



#$encrypted = Get-Content $PSScriptRoot\crendentials.txt | ConvertTo-SecureString $pass -AsPlainText -Force

#$secpasswd = ConvertTo-SecureString $pass -AsPlainText -Force#
#$credential = New-Object System.Management.Automation.PsCredential($user, $pass)



$test = Invoke-Command -ComputerName rdg.pasics.lev -ScriptBlock { Get-WmiObject -class "Win32_TSGatewayConnection" -namespace "root\cimv2\TerminalServices" -ComputerName rdg.pasics.lev | Select Username, ClientAddress, ConnectedResource } -credential $MyCredential | select "Username","ClientAddress","ConnectedResource"


$test.Count/2 # Es werden immer 2 Verbindungen aufgebaut eine via UDP und eine https deswegen muss hier durch 2 geteilt werden.

###### Entspricht der XML - Fomratierung für PRTG
write-host "<?xml version="1.0" encoding="Windows-1252" ?>"


write-host "<prtg>"

write-host    "<result>"
write-host        "<channel>" "Anzahl Verbindungen" "</channel>"
write-host        "<value>" ($test.Count/2) "</value>"
write-host    "</result>"


#write-host    "<result>"
#write-host        "<channel>" $test[0].Username $test[0].ClientAddress $test[0].ConnectedResource "</channel>"
#write-host        "<value>" [int]$test[0].ClientAddres "</value>"
#write-host    "</result>"


write-host "</prtg>"
