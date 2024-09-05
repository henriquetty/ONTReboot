import telnetlib
import time
import urllib.request
import os


ip_blackList = ["000", "002", "001", "192", "193"] #escreva o final dos IPs a serem colocados na blacklist sempre com 3 digitos.

#ONT Huawei Login testado nas HG
user = b'root\n'
password = b'admin\n'

 
def checkIP():
    cls()
    try: 
        print("Checando IP externo...")
        external_ip = urllib.request.urlopen('https://ident.me', timeout=10).read().decode('utf8')
    except:
        print("Ainda reiniciando...")
        time.sleep(2)
        cls()
        checkIP()
    else:
        print("Checando se IP está dentro de blacklist...")
        time.sleep(2)

        last_part = external_ip.split('.')[-1]
        last_three_digits = last_part.zfill(3)
        print("IP termina em: " + last_three_digits)

        if last_three_digits in ip_blackList:
            time.sleep(2)
            reboot(user, password, .500)
        else:      
            print("Feito! IP não consta na blacklist")

def reboot(user, password, delay):
    try:
        tn = telnetlib.Telnet("192.168.100.1", 23, timeout=5)
    except:
        print("Não consegui conectar a ONT... Tentando novamente")
        time.sleep(5)
        reboot(user, password, .500)

    tn.read_until(b'Login:')
    tn.write(user)
    
    time.sleep(delay)
    
    tn.read_until(b'Password:')
    tn.write(password)

    time.sleep(delay)

    command = b'reset\n'
    tn.write(command)

    time.sleep(delay)

    tn.close()

    print("ONT Reiniciada.")
    time.sleep(5)

    checkIP()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

checkIP()