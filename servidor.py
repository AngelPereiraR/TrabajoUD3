import socket
import random
import os, os.path
from time import sleep

class usuario:
    #Constructor
    def __init__(self, email, password, nick):
        #instance attributes
        self.email = email
        self.password = password
        self.nick = nick
    def __str__(self):
        return self.email + ";" + self.password + ";" + self.nick + ";"
    
    # getter method
    def get_email(self):
        return self.email
      
    # setter method
    def set_email(self, email):
        self._email = email
        # getter method
    def get_password(self):
        return self.password
    
    # setter method
    def set_password(self, password):
        self._age = password
    
    # getter method
    def get_nick(self):
        return self._age
      
    # setter method
    def set_nick(self, nick):
        self.nick = nick

#Metodo para seleccionar las 5 preguntas de forma aleatoria.
    
def selector():
    archivo = open("preguntas.txt")
    listaPreguntas = archivo.readlines()
    listaPreguntadas = []
    for i in range(5):
        pregunta = random.choice(listaPreguntas)
        listaPreguntadas.append(pregunta[0:(len(pregunta)-2)])
        listaPreguntas.remove(pregunta)
    return listaPreguntadas

#Método para mostrar al usuario las 5 preguntas correspondientes y comprobar si la respuesta indicada es correcta devolviendo el numero de aciertos.

def preguntas(listaPreguntadas):
    res = 0
    for i in range (len(listaPreguntadas)):
        pregunta = listaPreguntadas[i]
        print(pregunta[0:(len(pregunta)-2)])
        option = input("Introducir la opción correcta (1, 2, 3, 4) -> ")
        if(comprobarRespuesta(option,pregunta)):
            print("Has introducido la respuesta correcta.")
            res += 1
        else:
            print("La respuesta proporcionada no es correcta.")
    print("La cantidad de aciertos que has obtenido es de: " + str(res))
    return res

#Metodo para comprobar que la respuesta proporcionada es la correcta.

def comprobarRespuesta(option, pregunta):
    listaPregunta = pregunta.split(";")
    if(listaPregunta[len(listaPregunta)-1]==option):
        return True
    else:
        return False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("10.10.1.245", 9003))
server.listen(1)
nombres = []
cant = 0

# Eliminamos el fichero de ranking

if(os.path.isfile("puntuaciones.txt")):
    os.remove("puntuaciones.txt")

# Bucle para atender clientes

while True:
    
    # Se espera a un cliente
    
    socket_cliente, datos_cliente = server.accept()
    
    # Se escribe su informacion
    
    opcion = socket_cliente.recv(1024).decode()
    
    #Registro
    
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
    # Login
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
        
        # Recibimos los datos.
        
        datos = (socket_cliente.recv(1024).decode()).split(";")
        u = usuario(datos[0],datos[1],datos[2])
        print(u.nick)
        datos = (socket_cliente.recv(1024).decode()).split(";")
        u1 = usuario(datos[0],datos[1],datos[2])
        print(u1.nick)
        datos = (socket_cliente.recv(1024).decode()).split(";")
        u2 = usuario(datos[0],datos[1],datos[2])
        print(u2.nick)
        datos = (socket_cliente.recv(1024).decode()).split(";")
        u3 = usuario(datos[0],datos[1],datos[2])
        print(u3nick)
        
        # Enviamos los datos.
        
        for i in range(len(dicc_jug)):
            socket_cliente.send(dicc_jug[i][2].encode())