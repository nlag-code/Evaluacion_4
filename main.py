import conf
import requests
from netmiko import ConnectHandler
import time

url = "https://"
auth = (conf.user, conf.pwd)
headers = {'Accept': 'application/yang-data+json'}


def leer_archivo():
    f = open('hosts.txt', 'r')
    lista = list(f)
    f.close()
    return lista

def crear_respaldo():
    backup = open(hostname + '.txt', 'w')
    backup.write(netmiko_test())
    backup.close()

def netmiko_test():
    credenciales = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': conf.user,
        'password': conf.pwd,
        'port': 22,  # optional, defaults to 22
        'secret': 'secret',  # optional, defaults to ''
    }
    net_connect = ConnectHandler(**credenciales)
    output = net_connect.send_command('show run')
    return output



requests.packages.urllib3.disable_warnings()


for i in leer_archivo():
    host = i.rstrip('\n')
    salida = requests.get(url + host +"/restconf/data/Cisco-IOS-XE-native:native/", verify=False, headers=headers, auth=auth)
    hostname = salida.json()["Cisco-IOS-XE-native:native"]["hostname"]
    netmiko_test()
    crear_respaldo()
    time.sleep(1)
    print("Respaldo de equipo "+ hostname + " realizado de forma exitosa")


