import socket

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


listaNombres = s.recv(1024).decode()
