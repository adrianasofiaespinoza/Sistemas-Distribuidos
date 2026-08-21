import random
import string
from socket import *

serverName = input("Enter server hostname or IP address: ")
if not serverName:
    serverName = "localhost"

try:
    serverPort = int(input("Enter server port number: "))
except ValueError:
    print("Invalid input. Using default port 12000.")
    serverPort = 12000

if serverPort <= 0 or serverPort > 65535:
    serverPort = 12000

# 1. Generar un numero aleatorio de mensajes a enviar (ej. de 3 a 8)
num_messages = random.randint(3, 8)
print(f"\n[CLIENT] Generated random number of messages to send: {num_messages}\n")

# 2. Bucle para enviar esa cantidad exacta de mensajes
for i in range(num_messages):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect((serverName, serverPort))
    except Exception as e:
        print(f"Connection error on message {i+1}:", e)
        break # Si falla la conexion, terminamos
    
    # 3. Generar contenido aleatorio para el mensaje (letras minusculas, longitud de 5 a 15)
    msg_length = random.randint(5, 15)
    random_sentence = ''.join(random.choices(string.ascii_lowercase, k=msg_length))
    
    print(f"--- Sending message {i+1}/{num_messages} ---")
    print(f"Input lowercase sentence: {random_sentence}")
    
    clientSocket.send(random_sentence.encode())
    
    # Recibir la respuesta del servidor
    modifiedSentence = clientSocket.recv(1024)
    print("From Server:", modifiedSentence.decode())
    
    # Cerrar la conexion despues de cada mensaje (segun la arquitectura original)
    clientSocket.close()

print("\n[CLIENT] All messages sent. Communication terminated.")
