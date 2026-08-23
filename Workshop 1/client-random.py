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


num_messages = random.randint(3, 8)
print(f"\n[CLIENT] Generated random number of messages to send: {num_messages}\n")

for i in range(num_messages):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect((serverName, serverPort))
    except Exception as e:
        print(f"Connection error on message {i+1}:", e)
        break 
        
    msg_length = random.randint(5, 15)
    random_sentence = ''.join(random.choices(string.ascii_lowercase, k=msg_length))
    
    print(f"--- Sending message {i+1}/{num_messages} ---")
    print(f"Input lowercase sentence: {random_sentence}")
    
    clientSocket.send(random_sentence.encode())
    
    # Recibir la respuesta del servidor
    modifiedSentence = clientSocket.recv(1024)
    print("From Server:", modifiedSentence.decode())
    

    clientSocket.close()

print("\n[CLIENT] All messages sent. Communication terminated.")
