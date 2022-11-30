import socket, os, random

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

    puntos = preguntas(selector())
    print("Has conseguido " + str(puntos) + " puntos")