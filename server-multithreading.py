from socket import *
import time
import threading

try:
    serverPort = int(input("Enter server port number: "))
except:
    print("Invalid input. Using default port 12000.")
    serverPort = 12000

if serverPort <= 0 or serverPort > 65535:
    serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", serverPort))

# Permitir varias conexiones pendientes
serverSocket.listen(5)

print("The server is ready to receive")


def handle_client(connectionSocket, addr):
    print("From Client:", addr)

    try:
        sentence = connectionSocket.recv(1024).decode()

        print("I received from", addr, ":", sentence)

        capitalizedSentence = sentence.upper()

        # Simula procesamiento del servidor
        time.sleep(3)

        connectionSocket.send(capitalizedSentence.encode())

    except Exception as e:
        print("Error:", e)

    finally:
        connectionSocket.close()
        print("Connection closed:", addr)


while True:
    try:
        connectionSocket, addr = serverSocket.accept()

        # Crear un thread para este cliente
        client_thread = threading.Thread(
            target=handle_client,
            args=(connectionSocket, addr)
        )

        client_thread.start()

        print("Active threads:", threading.active_count() - 1)

    except KeyboardInterrupt:
        print("\nServer is shutting down.")
        break

serverSocket.close()
