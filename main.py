import conf
import requests
from netmiko import ConnectHandler
import time

#Variables que utilizaremos para hacer la consulta utilizando el protocolo restconf.
url = "https://"
auth = (conf.user, conf.pwd)
headers = {'Accept': 'application/yang-data+json'}


#Funcion con la que importaremos listado de ip que necesitamos realizar el respaldo
def leer_archivo():
    f = open('hosts.txt', 'r')
    lista = list(f)
    f.close()
    return lista

#Funcion con la que exportaremos cada respaldo realizado
def crear_respaldo():
    backup = open(hostname + '.txt', 'w')
    backup.write(netmiko_test())
    backup.close()

#Funcion donde utilizaremos funciones gracias a la libreria netmiko, esta nos permitira conectarnos por ssh a los equipos y lanzar comandos de IOS Cisco.
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


for i in leer_archivo(): # Con este bucle leeremos el archivo hosts donde estan las ip
    host = i.rstrip('\n') # variable donde guardaremos cada ip, le quitamos el salto de linea.
    try:
        salida = requests.get(url + host +"/restconf/data/Cisco-IOS-XE-native:native/", verify=False, headers=headers, auth=auth) # hacemos una consulta get gracias al protocolo restconf conf en los equipos cisco
        hostname = salida.json()["Cisco-IOS-XE-native:native"]["hostname"] #a la respuesta le filtramos el hostname que es lo que nos interesa
        netmiko_test() #llamamos a la funcion netmiko para conectarnos al host y lanzar el comando show running config
        crear_respaldo() # llamamos a la funcion crear respaldo donde creamos un archivo con el nombre del host y guardamos el show run.
        time.sleep(1) # generamos un tiempo de espera de 1 segundo porque se me hizo bonito.
        print("Respaldo de equipo "+ hostname + " realizado de forma exitosa.") # Informamos por un mensaje de consola que la tarea fue realizada de forma exitosa.
    except:
        print("El dispositivo con ip " + host + " no fue encontrado.")

