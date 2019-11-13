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

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
 

""" % """
'''
Der Funktion werden Anfangsadresse und Ende-Adresse als String übergeben.
Die Funktion zerlegt den String anhand des Punktes "." in Blöcke und berechnet die Größe der Blöcke.
Ein Block kann von 1 - 255 sein.
 
Der Retrun- Wert enthält die Größe eines Blocks. Sind Blöcke in einer IP-Adresse Identisch, werden diese nicht zurückgegeben.
'''


StatIP="10.108.65.0"
EndIP="10.108.67.255"
ipset1 = list( StatIP.split(".")) #Entsprcht StartIP'
ipset2 = list( EndIP.split("."))   # Entsprecht EndIP
IP_Block_range = list() # Diese Liste nimmt auf wieviele Blöcke sich unterscheiden. Das heißt wie groß die IP-Range ist. 
IPrange = 1

var_for_Windows = ".;C:\\bin"
#print(var_for_Windows)
# Berechnen der IP Range
# Der übergebene String wird umgewandetlt 
# Maximal dürfen sich nur die letzten 2 Blöcke unterscheiden, da der Scan sonst zu lange dauern würde.
#ps Das Ergebnis wird in der Liste IP_Block_Range gespeichert.
try:
    for block in range (len(ipset1)):
        if not ipset1[block] == ipset2[block]:
            if ipset1[0] != ipset2[0]:
                print("IP Range to high - Scan will take to long! \nReduce the IP Range !")
                exit(0)
            
            if ipset1[1] != ipset2[1]:
                print("IP Range to high - Scan would take to long! \n Reduce the IP Range !")
                exit(0)

            if int(ipset1[block]) > 255 or int(ipset2[block]) > 255:  ### Check if Block higher then 255, If it is,  then Exit the the Programm
                print("Ckeck IP Range")
                break

            if int(ipset1[block]) < int(ipset2[block]):
                IP_Block_range.append((int(ipset2[block]) - int(ipset1[block]))) #
                #print(IP_Block_range)
            else:
                print("Ckeck IP Range")
                break
except Exception as e:
    print("Check IP Range")

# Wenn die Länge von IP_Block-range = 1 ist dann ist unterscheidet sich die Adresse bloß im letzten Block
# Wenn die Länge von IP_Block-range = 2 ist dann ist unterscheidet sich die Adresse bloß im  vorletzten  Block



procList = [] # proclist ist eine Liste mit der Anzahl prozessen, die gestartet werden. 
IPsreplied = [] # Diese Variable nimmt die Antwort des processes an in einer Lieste an.

SubprocessStack_Init = 100 # Variable für Anzahl wieviele Pring Prozesse prallel laufen dürfen.
# Wenn der Block sich an der vorletzten Stelle unterscheidet. So muss erst der vorletzte Block abgearbeitet werden.
# Das heißt der vorletzte Block wird hoch von Anfang bis Ende hochgezählt und in jeder Interation, jedes mal noch mal von 0 - 255.



if len(IP_Block_range) == 2:
    IPinLastBlock = 0
    SubprocessStack = 0 # Varaible ist für die Anzahl, wieviele Pings gleichzeit ausgeführt werden können.

    for ip in range(int(ipset1[3]), 256):
        IPasString = ipset1[0]+"."+ipset1[1]+"."+ipset1[2]+"."+str(int(ipset1[3])+IPinLastBlock)
        if not str(os.defpath).find(":/bin") == -1:
            procList.append(subprocess.Popen(["ping", IPasString, "-c", "1"], stdout=subprocess.PIPE))
        elif not str(os.defpath).find(var_for_Windows) == -1:
            procList.append(subprocess.Popen(["ping", IPasString, "-n", "2"], stdout=subprocess.PIPE))
        else:
            print("OS not supported!")
            exit(0)
        IPinLastBlock += 1


# Defines how many Ping Processes are started in parallel
        SubprocessStack += 1
        if SubprocessStack == SubprocessStack_Init:
            for item in procList:
                ping_reply = item.stdout.read()
                if not str(os.defpath).find(":/bin") == -1:
                    if str(ping_reply).find("ttl") != -1:
                        ping_reply_as_list = str(ping_reply).split(" ")
                        IPsreplied.append(ping_reply_as_list[1])
                elif not str(os.defpath).find(var_for_Windows) == -1:
                    if str(ping_reply).find("ms TTL=") != -1:
                        ping_reply_as_list = str(ping_reply).split(" ")
                        IPsreplied.append(ping_reply_as_list[4])
                else:
                    print("OS not supported!")
                    exit(0)

            procList = []
            SubprocessStack = 0
    
    
# Arbeitet die letzen offenen Prozesse ab  
    for item in procList:
        ping_reply = item.stdout.read()
        if not str(os.defpath).find(":/bin") == -1:
            if str(ping_reply).find("ttl") != -1:
                ping_reply_as_list = str(ping_reply).split(" ")
                IPsreplied.append(ping_reply_as_list[1])
        elif not str(os.defpath).find(var_for_Windows) == -1:
            if str(ping_reply).find("ms TTL=") != -1:
                ping_reply_as_list = str(ping_reply).split(" ")
                IPsreplied.append(ping_reply_as_list[4])
        else:
            print("OS not supported!")
            exit(0)
            procList = []
            SubprocessStack = 0


    
    for ip in range(int(ipset1[2]), int(ipset2[2])):
        
         
        int_ip = int(ip)+1
        if int_ip == int(ipset2[2]):
            break
            
        for i in range(255):
            IPasString = ipset1[0]+"."+ipset1[1]+"."+str(int_ip)+"."+str(i)
            if not str(os.defpath).find(":/bin") == -1:
                procList.append(subprocess.Popen(["ping", IPasString, "-c", "1"], stdout=subprocess.PIPE))
            elif not str(os.defpath).find(var_for_Windows) == -1:
                procList.append(subprocess.Popen(["ping", IPasString, "-n", "2"], stdout=subprocess.PIPE))
            else:
                print("OS not supported!")
                exit(0)
    
    #####
    # Defines how many Ping Processes are started in parallel
        SubprocessStack += 1
        if SubprocessStack == SubprocessStack_Init:
            for item in procList:
                ping_reply = item.stdout.read()
                if not str(os.defpath).find(":/bin") == -1:
                    if str(ping_reply).find("ttl") != -1:
                        ping_reply_as_list = str(ping_reply).split(" ")
                        IPsreplied.append(ping_reply_as_list[1])
                elif not str(os.defpath).find(var_for_Windows) == -1:
                    if str(ping_reply).find("ms TTL=") != -1:
                        ping_reply_as_list = str(ping_reply).split(" ")
                        IPsreplied.append(ping_reply_as_list[4])
                else:
                    print("OS not supported!")
                    exit(0)
            procList = []
            SubprocessStack = 0
    
    
# Arbeitet die letzen offenen Prozesse ab  
    for item in procList:
        ping_reply = item.stdout.read()

        if not str(os.defpath).find(":/bin") == -1:
            if str(ping_reply).find("ttl") != -1:
                ping_reply_as_list = str(ping_reply).split(" ")
                IPsreplied.append(ping_reply_as_list[1])
        elif not str(os.defpath).find(var_for_Windows) == -1:
            if str(ping_reply).find("ms TTL=") != -1:
                ping_reply_as_list = str(ping_reply).split(" ")
                IPsreplied.append(ping_reply_as_list[4])
        else:
            print("OS not supported!")
            exit(0)
        procList = []
        SubprocessStack = 0



    IPinLastBlock = 0
    for ip in range(0, int(ipset2[3])):
        IPasString = ipset1[0]+"."+ipset1[1]+"."+ipset2[2]+"."+str(int(IPinLastBlock))
        if not str(os.defpath).find(":/bin") == -1:
            procList.append(subprocess.Popen(["ping", IPasString, "-c", "1"], stdout=subprocess.PIPE))
        elif not str(os.defpath).find(var_for_Windows) == -1:
            procList.append(subprocess.Popen(["ping", IPasString, "-n", "2"], stdout=subprocess.PIPE))
        else:
            print("OS not supported!")
            exit(0)     
                
        IPinLastBlock += 1


    # Defines how many Ping Processes are started in parallel
        SubprocessStack += 1
        if SubprocessStack == SubprocessStack_Init:
            for item in procList:
                ping_reply = item.stdout.read()
                if not str(os.defpath).find(":/bin") == -1:
                    if str(ping_reply).find("ttl") != -1:
                        ping_reply_as_list = str(ping_reply).split(" ")
                        IPsreplied.append(ping_reply_as_list[1])
                elif not str(os.defpath).find(var_for_Windows) == -1:
                    if str(ping_reply).find("ms TTL=") != -1:
                        ping_reply_as_list = str(ping_reply).split(" ")
                        IPsreplied.append(ping_reply_as_list[4])
                else:
                    print("OS not supported!")
                    exit(0)
            procList = []
            SubprocessStack = 0
    
    
# Arbeitet die letzen offenen Prozesse ab  
    for item in procList:
        ping_reply = item.stdout.read()
        if not str(os.defpath).find(":/bin") == -1:
            if str(ping_reply).find("ttl") != -1:
                ping_reply_as_list = str(ping_reply).split(" ")
                IPsreplied.append(ping_reply_as_list[1])
        elif not str(os.defpath).find(var_for_Windows) == -1:
            if str(ping_reply).find("ms TTL=") != -1:
                ping_reply_as_list = str(ping_reply).split(" ")
                IPsreplied.append(ping_reply_as_list[4])
        else:
            print("OS not supported!")
            exit(0)            
            
        procList = []
        SubprocessStack = 0
      
#################### Wenn Subnet = /24
###########################################################################################
elif len(IP_Block_range) == 1:
    SubprocessStack = 0
    for ip in range(int(ipset1[3]), int(ipset2[3])):
        IPasString = ipset1[0]+"."+ipset1[1]+"."+ipset1[2]+"."+str(ip)
        if not str(os.defpath).find(":/bin") == -1:
            procList.append(subprocess.Popen(["ping", IPasString, "-c", "1"], stdout=subprocess.PIPE))
        elif not str(os.defpath).find(var_for_Windows) == -1:
            procList.append(subprocess.Popen(["ping", IPasString, "-n", "2"], stdout=subprocess.PIPE))
        else:
            print("OS not supported!")
            exit(0)     


    # Defines how many Ping Processes are started in parallel
        SubprocessStack += 1
        if SubprocessStack == SubprocessStack_Init: 
            for item in procList:
                ping_reply = item.stdout.read()
                if not str(os.defpath).find(":/bin") == -1:
                    if str(ping_reply).find("ttl") != -1:
                        ping_reply_as_list = str(ping_reply).split(" ")
                        IPsreplied.append(ping_reply_as_list[1])
                elif not str(os.defpath).find(var_for_Windows) == -1:
                    if str(ping_reply).find("ms TTL=") != -1:
                        ping_reply_as_list = str(ping_reply).split(" ")
                        IPsreplied.append(ping_reply_as_list[4])
                else:
                    print("OS not supported!")
                    exit(0)
            
            procList = []
            SubprocessStack = 0
            print("Warten auf proclist Reset")
    
    
# Arbeitet die letzen offenen Prozesse ab  
    for item in procList:
        ping_reply = item.stdout.read()
        if not str(os.defpath).find(":/bin") == -1: #Prüfung, ob Linux/Mac
            if str(ping_reply).find("ttl") != -1:
                ping_reply_as_list = str(ping_reply).split(" ")
                IPsreplied.append(ping_reply_as_list[1])
        elif not str(os.defpath).find(var_for_Windows) == -1: #Prüfung, ob Windows
            if str(ping_reply).find("ms TTL=") != -1:
                ping_reply_as_list = str(ping_reply).split(" ")
                IPsreplied.append(ping_reply_as_list[4])
        else:
            print("OS not supported!")
            exit(0)

        procList = []
        SubprocessStack = 0


        
else:
    print("Somethin went wrong!")
      
    
        
########## Import IPs from files - File needs to be tested for checked plausibility 

try:
    if not str(os.defpath).find(":/bin") == -1: #Prüfung, ob Linux/Mac
        with open(__location__+"/IPsreplied.txt","r") as f:
            IPsImported = f.readlines()
            IPsImported = [x.strip() for x in IPsImported] 
    elif not str(os.defpath).find(var_for_Windows) == -1: #Prüfung, ob Windows
        with open(__location__+"\IPsreplied.txt","r") as f:
            IPsImported = f.readlines()
            IPsImported = [x.strip() for x in IPsImported] 
    
    #print(IPsImported)

except Exception as e:
    print("first replies generated! Run Script again, to see differences!")

######## Show differences ###################

try:
    diff = set(IPsreplied).difference(set(IPsImported))
    print(diff)
except Exception as e:
    print("Something went wrong in reading the text file!")

######### write replyed IPs to File ################


try:
    if not str(os.defpath).find(":/bin") == -1: #Prüfung, ob Linux/Mac
        with open(__location__+"/IPsreplied.txt", "w") as f:
            for line in IPsreplied:
                f.writelines(line)
                f.writelines("\n")
    elif not str(os.defpath).find(var_for_Windows) == -1: #Prüfung, ob Windows
        with open(__location__+"\IPsreplied.txt", "w") as f:
            for line in IPsreplied:
                f.writelines(line)
                f.writelines("\n")
except Exception as e:
    print("Something went wrong while creating a file!/nIf the file did not exist, run the script one again!")



#procList[ip].stdout.read())



""" 
You can still use Popen which takes the same input parameters as subprocess.call but is more flexible.

subprocess.call: The full function signature is the same as that of the Popen constructor - this functions passes all supplied arguments directly through to that interface.

One difference is that subprocess.call blocks and waits for the subprocess to complete (it is built on top of Popen), whereas Popen doesn't block and consequently allows you to launch other processes in parallel.

Try the following:

from subprocess import Popen
commands = ['command1', 'command2']
procs = [ Popen(i) for i in command ]
for p in procs:
   p.wait()  """