import socket, os, random


#Metodo para seleccionar las 5 preguntas de forma aleatoria.
    
def selector():
    archivo = open("preguntas.txt")
    listaPreguntas = archivo.readlines()
    listaPreguntadas = []
    for i in range(5):
        pregunta = random.choice(listaPreguntas)
        listaPreguntadas.append(pregunta)
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
    if(listaPregunta[6]==option):
        return True
    else:
        return False

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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9003))

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
    s.send(str(usuarioInicial).encode())
    print("Bienvenido " + usuarioInicial.nick + ", tiene que esperar a que se unan el resto de jugadores...")

    print("Los jugadores que jugarán esta partida son:")

    jugadores = []
    with open("usuariosConectados.txt", "a") as fichero:
        fichero.write(str(usuarioInicial))
        fichero.write("\n")
        fichero.close()

    while(len(jugadores) < 2):
        fichero = open("usuariosConectados.txt", "r")
        for linea in fichero:
            datos = linea.split(";")
            e = datos[0]
            p = datos[1]
            n = datos[2]
            u = usuario(e, p, n)
            jugadores.append(u)
        if(len(jugadores) < 2):
            jugadores = []

    for i in range(len(jugadores)):
        print("Jugador " + str(i + 1) + ": " + str(jugadores[i].nick))

    listaPreguntadas = selector()
    
    res = preguntas(listaPreguntadas)