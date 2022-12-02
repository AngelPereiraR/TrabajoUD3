import os, os.path, re, random, socket
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
            if(email==str(jug[0]) or email=="a"):
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
        
        # Enviamos los datos.
        
