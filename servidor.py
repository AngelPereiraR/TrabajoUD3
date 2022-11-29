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
        print("La cantidad de aciertos que has obtenido es de: " + res)
        return res
    #Metodo para comprobar que la respuesta proporcionada es la correcta.
    
    def comprobarRespuesta(option, pregunta):
        listaPregunta = pregunta.split(";")
        if(listaPregunta[len(listaPregunta)-1]==option):
            return True
        else:
            return False
