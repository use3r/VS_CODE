#Powershellscript für PRTG via Invoke-Command

Dieses Script besteht aus zwei Scripten.

Das erste Script erzeugt einen AES.key-Datei und und aus dem Passwort eine hash-Datei.

Das zweite Script nutzt diese Crendentials um eine Verbindung mit dem Remote Computer über das Invoke Kommando herzustellen.







Source 28.10.2019
https://www.pdq.com/blog/secure-password-with-powershell-encrypting-credentials-part-2/

In continuing with my previous post, Secure Password with PowerShell: Encrypting Credentials Part 1, I’d like to talk about sharing credentials between different machines/users/etc.

To recap my last blog, part 1 of Encrypting Credentials, when you use ConvertTo-SecureString and ConvertFrom-SecureString without a Key or SecureKey, Powershell will use Windows Data Protection API (DPAPI) to encrypt/decrypt your strings. This means that it will only work for the same user on the same computer.

When you use a Key/SecureKey, the Advanced Encryption Standard (AES – wiki link) encryption algorithm is used. You are able to use the stored credential from any machine with any user so long as you know the AES Key that was used.
Here’s a small snippet from my last blog post for easy reference for the two cmdlets (link to full post).

ConvertTo-SecureString and ConvertFrom-SecureString
Syntax:

ConvertTo-SecureString [-String] SomeString
 ConvertTo-SecureString [-String] SomeString [-SecureKey SecureString]
 ConvertTo-SecureString [-String] SomeString [-Key Byte[]]
 ConvertTo-SecureString [-String] SomeString [-AsPlainText] [-Force]

ConvertFrom-SecureString [-SecureString] SecureString [-SecureKey SecureString]
 ConvertFrom-SecureString [-SecureString] SecureString [-Key Byte[]]
–String String
The string to convert to a SecureString

–SecureKey SecureString
Encryption key as a SecureString.

–Key Byte[]
Encryption key as a byte array.

Using no Key/SecureKey

First, let’s show an example of what you will see if you try to create a credential from one machine (Machine 1) and then access it from another machine (Machine 2) without providing a key.

Encrypting a password without a key and saving it to file from Machine 1

This will create the file Password.txt with an encrypted standard string representing the password. It will use DPAPI.

$File = "\\Machine1\SharedPath\Password.txt"
$Password = "P@ssword1" | ConvertTo-SecureString -AsPlainText -Force
$Password | ConvertFrom-SecureString | Out-File $File

Accessing the encrypted password file from Machine 1

This will successfully get the encrypted standard string and convert it to a SecureString.

$File = "\\Machine1\SharedPath\Password.txt"
Get-Content $File | ConvertTo-SecureString
Secure password with powershell

 

Accessing the encrypted password file from Machine 2

This will fail with an error indicating that the key is invalid. Example below:

$File = "\\Machine1\SharedPath\Password.txt"
Get-Content $File | ConvertTo-SecureString
Admin: Windows PowerShell

 

Using Key/SecureKey
Now, let’s show a simple example of creating an encrypted standard string with the use of a key. AES encryption only supports 128-bit (16 bytes), 192-bit (24 bytes) or 256-bit key (32 bytes) lengths, so we’ll need to create or generate an appropriate key. For simplicity, let’s create a simple byte array of ascending numbers. We’ll use a 128-bit key, so we’ll need a 16-byte array.

Long way:

[Byte[]] $key = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
Short way:

[Byte[]] $key = (1..16)
Encrypting a password and saving it to file from Machine 1

This will create the file Password.txt with an encrypted standard string representing the password. It will use AES.

$File = "\\Machine1\SharedPath\Password.txt"
[Byte[]] $key = (1..16)
$Password = "P@ssword1" | ConvertTo-SecureString -AsPlainText -Force
$Password | ConvertFrom-SecureString -key $key | Out-File $File
Accessing the encrypted password file from Machine 1

This will successfully get the encrypted standard string and convert it to a SecureString. It will use the AES key that we provided earlier.

$File = "\\Machine1\SharedPath\Password.txt"
[Byte[]] $key = (1..16)
Get-Content $File | ConvertTo-SecureString -Key $key
convert to securestring

 

Accessing the encrypted password file from Machine 2

This will successfully get the encrypted standard string and convert it to a SecureString by using the AES key.

$File = "\\Machine1\SharedPath\Password.txt"
[Byte[]] $key = (1..16)
Get-Content $File | ConvertTo-SecureString -Key $key
encrypted password file

Putting it all together
Now that you know how to use an AES key to make SecureStrings created by different user accounts and workstations, you have to protect that key as best as you can since anybody who has that AES key can now decrypt the data protected.

In my previous example, I used a very simple 16-byte array that is stored in the body of the script itself. This is not a good practice and is essentially the same as if you were to write the password in clear text. Alternatively, you could create/generate a key beforehand in a separate script.

As an example, I have built a small script to generate a random 16-byte array. I have used the System.Security.Cryptography.RNGCryptoServiceProvider class to fill a byte array with randomly-generated data.

 

Creating AES key with random data and export to file

$KeyFile = "\\Machine1\SharedPath\AES.key"
$Key = New-Object Byte[] 16   # You can use 16, 24, or 32 for AES
[Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($Key)
$Key | out-file $KeyFile
Creating SecureString object

$PasswordFile = "\\Machine1\SharedPath\Password.txt"
$KeyFile = "\\Machine1\SharedPath\AES.key"
$Key = Get-Content $KeyFile
$Password = "P@ssword1" | ConvertTo-SecureString -AsPlainText -Force
$Password | ConvertFrom-SecureString -key $Key | Out-File $PasswordFile
Creating PSCredential object

$User = "MyUserName"
$PasswordFile = "\\Machine1\SharedPath\Password.txt"
$KeyFile = "\\Machine1\SharedPath\AES.key"
$key = Get-Content $KeyFile
$MyCredential = New-Object -TypeName System.Management.Automation.PSCredential `
 -ArgumentList $User, (Get-Content $PasswordFile | ConvertTo-SecureString -Key $key)
Final Notes
That’s it! You will be able to use the key file to decrypt the password file from any machine with any user.

Be sure to protect that AES key as if it were your password. Anybody who can read the AES key can decrypt anything that was encrypted with it.

At the very least, you should implement strict NTFS access controls for both your password and key files. This should keep out most prying eyes. Additionally, you may consider storing the data in a database with strict access controls or even implementing public-key (asymmetric) cryptography for additional control.

In any case, you should be good to use AES keys with your SecureStrings now.

Cheers!