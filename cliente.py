import socket, os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9003))

existe = ""
while(existe != "t"):
    email = input("Introduce tu correo electrónico: ")
    password = input("Introduce tu contraseña: ")
    s.send(email.encode())
    s.send(password.encode())
    existe = s.recv(1024).decode()
    if(existe == "f"):
        print("El usuario no está registrado, pruebe de nuevo...")

if(existe == "t"):
    print("El usuario está registrado")

nombre = input("Introduce tu nombre: ")
s.send(nombre.encode())
print("Bienvenido " + str(nombre) + ", tiene que esperar a que se unan el resto de jugadores...")

print("Los jugadores que jugarán esta partida son:")

with open("usuariosConectados.txt", "a") as fichero:
    fichero.write(email + ";" + password + ";" + nombre + ";")
    fichero.write("\n")
    fichero.close()

dicc_jug=[]
while(len(dicc_jug) < 4):
    fichero = open("usuariosConectados.txt", "r")
    for linea in fichero:
        datos=linea.split(';')
        e=datos[0]
        p=datos[1]
        n=datos[2]
        dicc_jug.append([e,p,n])
    if(len(dicc_jug) != 4):
        dicc_jug = []
    fichero.close()

print("Jugador 1: " + str(dicc_jug[0][2]))
print("Jugador 2: " + str(dicc_jug[1][2]))
print("Jugador 3: " + str(dicc_jug[2][2]))
print("Jugador 4: " + str(dicc_jug[3][2]))