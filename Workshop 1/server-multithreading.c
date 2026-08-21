#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <signal.h>

#define BUFSZ 1024

int serverSocket;
int active_threads = 0;
pthread_mutex_t count_mutex = PTHREAD_MUTEX_INITIALIZER;

typedef struct {
    int connectionSocket;
    struct sockaddr_in addr;
} client_args;

/* Equivalente a handle_client(connectionSocket, addr) */
void *handle_client(void *arg) {
    client_args *cargs = (client_args *)arg;
    int connectionSocket = cargs->connectionSocket;
    struct sockaddr_in addr = cargs->addr;
    free(cargs);

    char ip_str[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &addr.sin_addr, ip_str, sizeof(ip_str));
    printf("From Client: %s:%d\n", ip_str, ntohs(addr.sin_port));

    char buffer[BUFSZ];
    int n = recv(connectionSocket, buffer, BUFSZ - 1, 0);

    if (n <= 0) {
        printf("Error: connection closed or recv failed\n");
    } else {
        buffer[n] = '\0';
        printf("I received from %s:%d : %s\n", ip_str, ntohs(addr.sin_port), buffer);

        /* capitalizedSentence = sentence.upper() */
        for (int i = 0; buffer[i]; i++) {
            buffer[i] = toupper((unsigned char)buffer[i]);
        }

        /* Simula procesamiento del servidor */
        sleep(3);

        send(connectionSocket, buffer, strlen(buffer), 0);
    }

    close(connectionSocket);
    printf("Connection closed: %s:%d\n", ip_str, ntohs(addr.sin_port));

    pthread_mutex_lock(&count_mutex);
    active_threads--;
    pthread_mutex_unlock(&count_mutex);

    return NULL;
}

/* Maneja Ctrl+C igual que el KeyboardInterrupt de Python */
void handle_sigint(int sig) {
    printf("\nServer is shutting down.\n");
    close(serverSocket);
    exit(0);
}

int main() {
    int serverPort;
    char input[16];

    printf("Enter server port number: ");
    if (fgets(input, sizeof(input), stdin) == NULL || sscanf(input, "%d", &serverPort) != 1) {
        printf("Invalid input. Using default port 12000.\n");
        serverPort = 12000;
    }

    if (serverPort <= 0 || serverPort > 65535) {
        serverPort = 12000;
    }

    signal(SIGINT, handle_sigint);

    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) {
        perror("socket");
        exit(1);
    }

    int opt = 1;
    setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(serverPort);

    if (bind(serverSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("bind");
        exit(1);
    }

    /* Permitir varias conexiones pendientes */
    listen(serverSocket, 5);

    printf("The server is ready to receive\n");

    while (1) {
        struct sockaddr_in clientAddr;
        socklen_t clientLen = sizeof(clientAddr);

        int connectionSocket = accept(serverSocket, (struct sockaddr *)&clientAddr, &clientLen);
        if (connectionSocket < 0) {
            perror("accept");
            continue;
        }

        client_args *cargs = malloc(sizeof(client_args));
        cargs->connectionSocket = connectionSocket;
        cargs->addr = clientAddr;

        pthread_t client_thread;
        pthread_create(&client_thread, NULL, handle_client, cargs);
        pthread_detach(client_thread);  /* equivalente a no hacer join, como en el hilo de Python */

        pthread_mutex_lock(&count_mutex);
        active_threads++;
        printf("Active threads: %d\n", active_threads);
        pthread_mutex_unlock(&count_mutex);
    }

    close(serverSocket);
    return 0;
}

/*
Compilar:  gcc server.c -o server -lpthread
Ejecutar:  ./server
*/
