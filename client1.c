#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Librerías de Linux para sockets
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 12000
#define BUFFER_SIZE 1024

int main() {
    int client_socket;
    struct sockaddr_in server_addr;

    char buffer[BUFFER_SIZE] = {0};
    char message[BUFFER_SIZE];
    char ip_address[50];

    // 1. Crear el socket del cliente
    client_socket = socket(AF_INET, SOCK_STREAM, 0);

    if (client_socket < 0) {
        perror("Fallo al crear el socket");
        return 1;
    }

    // Pedir la IP del servidor al usuario
    printf("Enter server IP address (press Enter for localhost): ");

    fgets(ip_address, sizeof(ip_address), stdin);

    // Quitar el salto de línea
    ip_address[strcspn(ip_address, "\n")] = '\0';

    // Si no se introduce una IP, utilizar localhost
    if (strlen(ip_address) == 0) {
        strcpy(ip_address, "127.0.0.1");
    }

    // 2. Configurar la dirección del servidor
    memset(&server_addr, 0, sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);

    // Convertir la IP de texto a formato de red
    if (inet_pton(AF_INET, ip_address, &server_addr.sin_addr) <= 0) {
        printf("Invalid server IP address.\n");
        close(client_socket);
        return 1;
    }

    // 3. Conectar al servidor
    if (connect(
            client_socket,
            (struct sockaddr *)&server_addr,
            sizeof(server_addr)) < 0) {

        perror("Failed to connect to server");
        close(client_socket);
        return 1;
    }

    printf("Connected successfully to server %s on port %d\n",
           ip_address, PORT);

    // 4. Pedir el mensaje al usuario
    printf("Input lowercase sentence: ");

    fgets(message, sizeof(message), stdin);

    // Quitar el salto de línea
    message[strcspn(message, "\n")] = '\0';

    // 5. Enviar el mensaje al servidor
    if (send(
            client_socket,
            message,
            strlen(message),
            0) < 0) {

        perror("Error sending message");
        close(client_socket);
        return 1;
    }

    // 6. Recibir la respuesta del servidor
    int valread = recv(
        client_socket,
        buffer,
        BUFFER_SIZE - 1,
        0
    );

    if (valread > 0) {

        // Asegurar que el mensaje termine en '\0'
        buffer[valread] = '\0';

        printf("From Server: %s\n", buffer);

    } else if (valread == 0) {

        printf("Server closed the connection.\n");

    } else {

        perror("Error receiving response");
    }

    // 7. Cerrar el socket
    close(client_socket);

    return 0;
}

/*
Compilar:  gcc client_aleatorio.c -o client_aleatorio
Ejecutar:  ./client_aleatorio
*/