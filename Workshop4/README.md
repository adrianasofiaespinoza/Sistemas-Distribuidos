# Workshop 4 - Sistemas Distribuidos

Este repositorio contiene la implementación y documentación del Workshop 4 de la materia de Sistemas Distribuidos. El taller se centra en la sincronización de tiempo, uso de relojes lógicos y físicos, y algoritmos de exclusión mutua en entornos distribuidos.

## Estructura del Proyecto

El proyecto está dividido en varias carpetas, cada una correspondiente a una actividad específica del taller, junto con una carpeta que contiene el informe detallado en formato LaTeX.

### 1. [Actividad 1: Servidor UTC](./Actividad1_UTC_Server/)
Implementación de un cliente y un servidor para la obtención de la hora UTC, simulando un servicio de tiempo básico.
- `client-UTC.py`: Script del cliente para solicitar la hora al servidor.
- `server-UTC.py`: Script del servidor que proporciona la hora UTC actual.

### 2. [Actividad 2: Tiempo Global](./Actividad2_Global_Time/)
Implementación de algoritmos de sincronización de tiempo en un entorno de red entre diferentes nodos.
- `peer_node.py`: Código fuente de la simulación de un nodo (peer) para la sincronización de tiempo global.

### 3. [Actividad 3: Relojes Vectoriales](./Actividad3_Vector_Clocks/)
Implementación del algoritmo de relojes vectoriales (Vector Clocks) para capturar y mantener la causalidad de los eventos concurrentes en un sistema distribuido.
- `vector_clock.py`: Implementación de los procesos que intercambian mensajes utilizando relojes vectoriales.

### 4. [Actividad 4: Exclusión Mutua](./Actividad4_Mutual_Exclusion/)
Implementación de distintos algoritmos de exclusión mutua para coordinar el acceso a recursos compartidos entre procesos.
- `central_server.py`: Algoritmo de exclusión mutua utilizando el enfoque de un Servidor Centralizado.
- `token_ring.py`: Algoritmo de exclusión mutua basado en un Anillo de Tokens (Token Ring).

### 5. [Informe](./informe/)
Contiene el documento técnico detallado del taller, desarrollado en formato LaTeX.
- `informe.tex`: Archivo principal con el código fuente del informe.
- `informe.pdf`: Documento final compilado que incluye la explicación de la teoría, análisis del código y capturas de los resultados de cada actividad.
- Además de otros archivos auxiliares generados durante la compilación de LaTeX.

## Notas de Ejecución

Los scripts correspondientes a cada actividad están desarrollados en Python. Pueden ejecutarse de forma independiente a través de la terminal o línea de comandos. 

Por ejemplo, para probar la Actividad 1:
```bash
# Iniciar primero el servidor en una terminal:
python Actividad1_UTC_Server/server-UTC.py

# En otra terminal, ejecutar el cliente:
python Actividad1_UTC_Server/client-UTC.py
```
(Para las demás actividades, se recomienda revisar los comentarios en el código interno de cada archivo `.py`).
