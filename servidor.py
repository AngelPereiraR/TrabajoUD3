import socket
import random
import os, os.path
from time import sleep

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9003))
server.listen(1)
nombres = []
cant = 0

if(os.path.isfile("usuariosConectados.txt")):
    os.remove("usuariosConectados.txt")

#eliminamos el fichero de ranking
if(os.path.isfile("puntuaciones.txt")):
    os.remove("puntuaciones.txt")
# bucle para atender clientes
while True:
    # Se espera a un cliente
    socket_cliente, datos_cliente = server.accept()
    # Se escribe su informacion
    opcion = socket_cliente.recv(1024).decode()
    while(opcion != "1"):
        email = socket_cliente.recv(1024).decode()
        password = socket_cliente.recv(1024).decode()
        fichero = open("usuarios.txt","r")
        dicc_jug=[]
        for linea in fichero:
            datos=linea.split(';')
            e=datos[0]
            p=datos[1]
            dicc_jug.append([e,p])
        fichero.close()
        for jug in dicc_jug:
            if(email==str(jug[0])):
                existe = "t"
                break
            else:
                existe = "f"
        socket_cliente.send(existe.encode())
        if(existe=="f"):
            with open("usuarios.txt","a") as fichero:
                fichero.write(email + ";" + password + ";")
                fichero.write("\n")
                fichero.close()
        opcion = socket_cliente.recv(1024).decode()
    if(opcion == "1"):
        existe = ""
        while(existe != "t"):
            email = socket_cliente.recv(1024).decode()
            password = socket_cliente.recv(1024).decode()
            fichero = open("usuarios.txt","r")
            dicc_jug=[]
            for linea in fichero:
                datos=linea.split(';')
                e=datos[0]
                p=datos[1]
                dicc_jug.append([e,p])
            fichero.close()
            for jug in dicc_jug:
                if(email==str(jug[0]) and password==str(jug[1])):
                    existe = "t"
                    break
                else:
                    existe = "f"
            socket_cliente.send(existe.encode())
        nombre = socket_cliente.recv(1024).decode()
        print(nombre)