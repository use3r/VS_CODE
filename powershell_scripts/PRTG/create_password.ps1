

######## Erstellt einen AES Key in dem Pfad, an dem auch das Script liegt
$KeyFile = "$PSScriptRoot\AES.key"
$Key = New-Object Byte[] 32   # You can use 16, 24, or 32 for AES
[Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($Key)
$Key | out-file $KeyFile


######### Erstellt eine AES verschlüsselte Passwort Datei, an dem auch das Script liegt
$PasswordFile = "$PSScriptRoot\Password.txt"
$KeyFile = "$PSScriptRoot\AES.key"
$Key = Get-Content $KeyFile
$Password = "geheimes Passort" | ConvertTo-SecureString -AsPlainText -Force
$Password | ConvertFrom-SecureString -key $Key | Out-File $PasswordFile


############# Erzeugt ein Credentials Objekt, welches dann für ein Invoke-Command genutz werden kann
############# Achtung! Das AES.Key-Datai und Password.txt müssen in dem selben Ordner liegen wie, das Script, welches diese nutzen soll.

$User = "Administrator"
$PasswordFile = "$PSScriptRoot\Password.txt"
$KeyFile = "$PSScriptRoot\AES.key"
$key = Get-Content $KeyFile
$MyCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, (Get-Content $PasswordFile | ConvertTo-SecureString -Key $key)



