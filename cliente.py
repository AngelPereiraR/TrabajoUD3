import socket, random, re

# Metodo para seleccionar las 5 preguntas de forma aleatoria.
    
def selector():
    archivo = open("preguntas.txt")
    listaPreguntas = archivo.readlines()
    listaPreguntadas = []
    for i in range(5):
        pregunta = random.choice(listaPreguntas)
        listaPreguntadas.append(pregunta)
        listaPreguntas.remove(pregunta)
    return listaPreguntadas

# Metodo para mostrar al usuario las 5 preguntas correspondientes y comprobar si la respuesta indicada es correcta devolviendo el numero de aciertos.

def preguntas(listaPreguntadas):
    res = 0
    for i in range (len(listaPreguntadas)):
        pregunta = listaPreguntadas[i]
        preguntaSeparada = pregunta.split(";")
        print(preguntaSeparada[0] + ". " + preguntaSeparada[1] + " " + preguntaSeparada[2] + " " + preguntaSeparada[3] + " " + preguntaSeparada[4] + " " + preguntaSeparada[5])
        option = input("Introduce la opción correcta (1, 2, 3, 4) -> ")
        if(comprobarRespuesta(option,pregunta)):
            print("Has introducido la respuesta correcta.")
            res += 1
        else:
            print("La respuesta proporcionada no es correcta.")
    print("La cantidad de aciertos que has obtenido es de: " + str(res))
    return res

# Metodo para comprobar que la respuesta proporcionada es la correcta.

def comprobarRespuesta(option, pregunta):
    listaPregunta = pregunta.split(";")
    if(listaPregunta[6]==option):
        return True
    else:
        return False
    
# Metodo para comprobar que el correo es válido.

def verificadorCorreo(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo)

class usuario:
    # Constructor
    def __init__(self, email, password, nick):
        # instance attributes
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
    
    # Registro.
    
    if(opcion == "2"):
        email = input("Introduce un correo electrónico: ")
        password = input("Introduce una contraseña: ")
        if(verificadorCorreo(email)):
            s.send(email.encode())
            s.send(password.encode())
            existe = s.recv(1024).decode()
            if(existe == "t"):
                print("El correo electrónico ya está escogido, pruebe de nuevo...\n")
            else:
                if(existe == "f"):
                   print("El usuario se ha registrado correctamente.\n")
        else:
            s.send("a".encode())
            s.send("a".encode())
            print("El email introducido no es válido.\n")
    if(opcion > "2" or opcion < "0"):
        print("No existe una opción para esa variable, pruebe de nuevo...\n")
        
# Login.
        
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
        
    # Insertando nombre de usuario para la partida.

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
        
    # Esperando a los 4 jugadores.

    while(len(jugadores) < 4):
        fichero = open("usuariosConectados.txt", "r")
        for linea in fichero:
            datos = linea.split(";")
            e = datos[0]
            p = datos[1]
            n = datos[2]
            u = usuario(e, p, n)
            jugadores.append(u)
        if(len(jugadores) < 4):
            jugadores = []
            
    # Mostrando los jugadores loggeados.

    for i in range(len(jugadores)):
        print("Jugador " + str(i + 1) + ": " + str(jugadores[i].nick))

    # Consiguiendo los puntos de la partida.
    
    listaPreguntadas = selector()
    
    res = preguntas(listaPreguntadas)

    # Mostrando los puntos de todos los jugadores.

    with open("puntuaciones.txt", "a") as fichero:
        fichero.write(email + ";" + str(res) + ";\n")
        fichero.close()

    puntuaciones = []
    while(len(puntuaciones) < 4):
        fichero = open("puntuaciones.txt", "r")
        for linea in fichero:
            datos = linea.split(";")
            e = datos[0]
            p = datos[1]
            puntuaciones.append([e,p])
        if(len(puntuaciones) < 4):
            puntuaciones = []
    
    # Mostrando las puntuaciones de todos los jugadores y calculando al ganador.

    max = "0"
    emailGanador = ""
    for i in range(len(puntuaciones)):
        print("Jugador " + str(i + 1) + ": " + str(puntuaciones[i][1]))
        if(max < puntuaciones[i][1]):
            max = puntuaciones[i][1]
            emailGanador = puntuaciones[i][0]
    
    ganador = "False"
    for i in range(len(puntuaciones)):
        if(email == emailGanador):
            ganador = "True"
    
    # Mostrando si ha ganado o perdido la partida y sumando al fichero de las puntuaciones generales la partida ganada.

    puntuaciones = []
    existe = "False"
    if(ganador == "True"):
        print("¡¡¡Has sido el ganador de la partida!!!")
        fichero = open("puntuacionesGenerales.txt", "r")
        for linea in fichero:
            datos = linea.split(";")
            e = datos[0]
            g = datos[1]
            puntuaciones.append([e,g])
        if(len(puntuaciones) == 0):
            puntuaciones.append([email, 1])
        else:
            for i in range(len(puntuaciones)):
                if(puntuaciones[i][0] == email):
                    puntuacion = int(puntuaciones[i][1])
                    puntuacion += 1
                    puntuaciones[i][1] = str(puntuacion)
                    existe = "True"
            if(existe == "False"):
                puntuaciones.append([email, 1])
        with open("puntuacionesGenerales.txt", "w") as fichero:
            for i in range(len(puntuaciones)):
                fichero.write(str(puntuaciones[i][0]) + ";" + str(puntuaciones[i][1]) + ";\n")
    else:
        print("Lo sentimos. Has perdido esta partida")

    # Enviando los datos del fichero de las puntuaciones generales al servidor

    fichero = open("puntuacionesGenerales.txt", "r")

    longitud = 0

    for linea in fichero:
        longitud += 1

    s.send(str(longitud).encode())

    fichero2 = open("puntuacionesGenerales.txt", "r")

    for linea in fichero2:
        datos = linea
        s.send(datos.encode())