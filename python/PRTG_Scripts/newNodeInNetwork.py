'''
Unterscheiden sich die Teilnehmer des neuen Scans zu den Teilnehmner im der vorhärigen Datei, so wird ein Alarm gesetzt und die neun Teilnemer werden aussgegeben.
'''

'init'
'Diese Sets weden für den Vergleiche benötigt, ob neue IP vorhanden sind'
'subprocess.check_call([r"C:\pathToYourProgram\yourProgram.exe", "your", "arguments", "comma", "separated"])'
'ipscan-win32-3.5.2.exe -f:range 10.108.65.2 10.108.65.137 -o ipscan.csv -s -q'

'subprocess.check_call([r"ipscan-win32-3.5.2.exe", "-f:range", StatIP, EndIP, "-o", PreScanOutputFile, "-s", "-q"])'


import subprocess
import os

def CalcIPRange(StartIP:str, EndIP:str):
    print("In Function")

    return "Hello, I am a Function "

print(CalcIPRange("test","test"))


StatIP="192.168.1.0"
EndIP="192.168.1.255"
ipset1 = list( StatIP.split("."))
ipset2 = list( EndIP.split("."))
IP_Block_range = list()
IPrange = 1

#Berechnen der IP Range
# Der übergebene String wird umgewandetlt

for block in range (len(ipset1)):
    if not ipset1[block] == ipset2[block]:
        if int(ipset1[block]) > 255 or int(ipset2[block]) > 255:  ### Check if Block higher then 255, I then Exit the the Programm
            print("Ckeck IP Range")
            break

        if int(ipset1[block]) < int(ipset2[block]):
            IP_Block_range.append((int(ipset2[block]) - int(ipset1[block])))
            #print(IP_Block_range)
        else:
            print("Ckeck IP Range")
            break

if len(IP_Block_range) == 2:
    for block in IP_Block_range:
        IPrange = ( int(block) + (255 * IP_Block_range[0])) 
        #print(IPrange)
else:
    IPrange = IP_Block_range[0] # IPRange enthält die Anzhal der IP Adressen

procList = []
IPsreplyed = []










### startet Ping -Processe -> Maximal 9255 Prcesse
for ip in range(0, IPrange):
    IPasString = str(ipset1[0]+"."+str(ipset1[1]+"."+ipset1[2]+"."+str(ip)))
    procList.append(subprocess.Popen(["ping", IPasString, "-n", "1"], stdout=subprocess.PIPE))

"""  ((str(procList[ip].stdout.read()).find("Antwort von "+ IPasString) != -1) and """

###Wertet die Ping Antwort aus und gibt die IP-Adressen zurück, die geantwortet haben.
for ip in range(0,IPrange):
    IPasString = str(ipset1[0]+"."+str(ipset1[1]+"."+ipset1[2]+"."+str(ip)))
    if str(procList[ip].stdout.read()).find("TTL") != -1:
        IPsreplyed.append(IPasString)



try:
    with open("IPsreplyed.txt","r") as f:
       IPsImported = f.readlines()
       IPsImported = [x.strip() for x in IPsImported] 
    #print(IPsImported)

except Exception as e:
    print("Crreate File first!")

diff = set(IPsreplyed).difference(set(IPsImported))
print(diff)

try:
    with open("IPsreplyed.txt", "w") as f:
        for line in IPsreplyed:
            f.writelines(line)
            f.writelines("\n")
            

except Exception as e:
    print("Something went wrong while creating a file!")



#procList[ip].stdout.read())




""" ipset2 = EndIP.split(".").sort
iprange = ipset1. """




""" proc = subprocess.Popen(["ping", StatIP, "-n", "1"], stdout=subprocess.PIPE)
output = proc.stdout.read()

str1 = str(output)

if (str1.find('Antwort von '+ StatIP)) != -1:
    print(StatIP) """


####### 
""" try:
    with open(PreScanOutputFile) as f:
        csv_python = csv.reader(f)
        for row in csv_python:
            print(row[0])
            ip2.add(row[0])

except Exception as e:
    print("Some File not found!") """
