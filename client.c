#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>

#define BUFSZ 1024

/* Genera una cadena aleatoria de letras minúsculas, tamaño [minLen, maxLen] */
void generar_mensaje(char *buf, int longitud) {
    const char letras[] = "abcdefghijklmnopqrstuvwxyz";
    for (int i = 0; i < longitud; i++) {
        buf[i] = letras[rand() % (sizeof(letras) - 1)];
    }
    buf[longitud] = '\0';
}

int main() {
    srand(time(NULL));

    char serverName[256];
    char input[16];
    int serverPort;

    printf("Enter server hostname or IP address: ");
    fgets(serverName, sizeof(serverName), stdin);
    serverName[strcspn(serverName, "\n")] = '\0';
    if (strlen(serverName) == 0) {
        strcpy(serverName, "localhost");
    }

    printf("Enter server port number: ");
    if (fgets(input, sizeof(input), stdin) == NULL || sscanf(input, "%d", &serverPort) != 1) {
        printf("Invalid input. Using default port 12000.\n");
        serverPort = 12000;
    }

    if (serverPort <= 0 || serverPort > 65535) {
        serverPort = 12000;
    }

    struct hostent *host = gethostbyname(serverName);
    if (host == NULL) {
        fprintf(stderr, "Connection error: could not resolve host '%s'\n", serverName);
        return 1;
    }

    /* 1. Generar un numero aleatorio de mensajes a enviar (ej. de 3 a 8) */
    int num_messages = 3 + rand() % 6;  /* 3..8 */
    printf("\n[CLIENT] Generated random number of messages to send: %d\n\n", num_messages);

    char msg[64];
    char buffer[BUFSZ];

    /* 2. Bucle para enviar esa cantidad exacta de mensajes */
    for (int i = 0; i < num_messages; i++) {
        int clientSocket = socket(AF_INET, SOCK_STREAM, 0);

        struct sockaddr_in serverAddr;
        memset(&serverAddr, 0, sizeof(serverAddr));
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(serverPort);
        memcpy(&serverAddr.sin_addr, host->h_addr_list[0], host->h_length);

        if (connect(clientSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
            printf("Connection error on message %d: ", i + 1);
            perror("");
            close(clientSocket);
            break;  /* Si falla la conexion, terminamos */
        }

        /* 3. Generar contenido aleatorio (letras minusculas, longitud 5 a 15) */
        int msg_length = 5 + rand() % 11;  /* 5..15 */
        generar_mensaje(msg, msg_length);

        printf("--- Sending message %d/%d ---\n", i + 1, num_messages);
        printf("Input lowercase sentence: %s\n", msg);

        send(clientSocket, msg, strlen(msg), 0);

        int n = recv(clientSocket, buffer, BUFSZ - 1, 0);
        if (n > 0) {
            buffer[n] = '\0';
            printf("From Server: %s\n", buffer);
        }

        /* Cerrar la conexion despues de cada mensaje */
        close(clientSocket);
    }

    printf("\n[CLIENT] All messages sent. Communication terminated.\n");
    return 0;
}

/*
Compilar:  gcc client_aleatorio.c -o client_aleatorio
Ejecutar:  ./client_aleatorio
*/