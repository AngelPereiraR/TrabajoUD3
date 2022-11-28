from threading import Thread, Semaphore, Lock
import socket
import random
import os, os.path
from time import sleep

class Cliente(Thread):
    def __init__(self, socket_cliente, datos_cliente, nombre_cliente, palabra):
        Thread.__init__(self)
        self.socket = socket_cliente
        self.datos = datos_cliente
        self.nombre=nombre_cliente
        self.intentos=6
        self.escogida=palabra
        self.encontrada=False
      
    def run(self):
        global turnos, mutex
        print(self.nombre+" espera turno para jugar.")
        turnos.acquire()
        print(self.nombre+" ha comenzado a jugar.")
        adivina=['*']*len(self.escogida)
        while(self.intentos>0 and self.encontrada==False):
            letra=self.socket.recv(1024).decode()
            if(letra in self.escogida):
                self.socket.send("s".encode())
                for i in range(len(self.escogida)):
                    if (self.escogida[i]==letra):
                        adivina[i]=letra
            else:
                self.intentos-=1
                self.socket.send("n".encode())
            pal="".join(adivina)
            cadena=pal+";"+str(self.intentos)+";"
            if(self.escogida==pal):
                self.encontrada=True
                cadena+="G;"
                cadena+=self.escogida
            else:
                cadena+="P;"
                cadena+=self.escogida
            sleep(2)
            self.socket.send(cadena.encode())
        if(self.encontrada):
            print(self.nombre+" ha ganado la partida. Puntos: "+str(self.intentos))
            mutex.acquire()
            fichero=open("puntuaciones.txt","a")
            fichero.write(self.nombre+";"+str(self.intentos))
            fichero.write("\n")
            fichero.close()
            mutex.release()
        else:
            print(self.nombre+" ha perdido la partida. Puntos: "+str(self.intentos))
        turnos.release()
        self.socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9003))
server.listen(4)
nombres = []

#eliminamos el fichero de ranking
if(os.path.isfile("puntuaciones.txt")):
    os.remove("puntuaciones.txt")    
# bucle para atender clientes
while True:
    # Se espera a un cliente
    socket_cliente, datos_cliente = server.accept()
    # Se escribe su informacion
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
    cant = 0
    while(cant != 3):
        print(nombre)
        nombres.append(nombre)
        cant += 1
        
    for n in nombres:
        socket_cliente.send(str(n).encode())
    