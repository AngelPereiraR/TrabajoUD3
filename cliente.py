import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect("localhost", 9999)

email = input("Introduce tu correo electrónico: ")
password = input("Introduce tu contraseña: ")
s.send(email.encode)
s.send(password.encode)