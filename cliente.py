import socket, os, random, usuario

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.10.1.245", 9003))

opcion = "2"
while(opcion != "1"):
    print("---- Menú ----")
    print("1. Iniciar sesión")
    print("2. Registrar")
    opcion = input("Introduce la opción que desea realizar: ")
    s.send(opcion.encode())
    if(opcion == "2"):
        email = input("Introduce un correo electrónico: ")
        password = input("Introduce una contraseña: ")
        s.send(email.encode())
        s.send(password.encode())
        existe = s.recv(1024).decode()
        if(existe == "t"):
            print("El correo electrónico ya está escogido, pruebe de nuevo...\n")
        else:
            if(existe == "f"):
                with open("usuarios.txt","a") as fichero:
                    fichero.write(email + ";" + password + ";")
                    fichero.write("\n")
                    fichero.close()
                print("El usuario se ha registrado correctamente.\n")
    if(opcion > "2" or opcion < "0"):
        print("No existe una opción para esa variable, pruebe de nuevo...\n")
if(opcion == "1"):
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
    usuarioInicial = usuario(email,password,nombre)
    s.send(str(usuarioInicial))
    print("Bienvenido " + usuarioInicial.nick + ", tiene que esperar a que se unan el resto de jugadores...")

    print("Los jugadores que jugarán esta partida son:")

    print("Jugador 1: " + str(s.recv(1024).decode()))
    print("Jugador 2: " + str(s.recv(1024).decode()))
    print("Jugador 3: " + str(s.recv(1024).decode()))
    print("Jugador 4: " + str(s.recv(1024).decode()))
