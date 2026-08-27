import zmq
import time
import sys

context = zmq.Context()
s = context.socket(zmq.PUB)

try:
    serverName = input("Enter server hostname or IP address (default: localhost): ").strip()
    if not serverName:
        serverName = "localhost"

    port_input = input("Enter server port number (default: 15000): ").strip()
    if not port_input:
        serverPort = 15000
    else:
        try:
            serverPort = int(port_input)
            if serverPort <= 0 or serverPort > 65535:
                print("Puerto fuera de rango (1-65535). Usando puerto por defecto: 15000.")
                serverPort = 15000
        except ValueError:
            print("Entrada no válida. Usando puerto por defecto: 15000.")
            serverPort = 15000

    p = f"tcp://{serverName}:{serverPort}"
    
    try:
        s.bind(p)
    except zmq.ZMQError as e:
        print(f"\n[ERROR] No se pudo enlazar el socket en '{p}': {e}")
        if serverPort < 1024:
            print("-> Sugerencia: Los puertos menores a 1024 requieren permisos de administrador o están reservados. Usa un puerto como 15000 o 5555.")
        else:
            print("-> Sugerencia: Verifica que el puerto no esté en uso por otra aplicación.")
        sys.exit(1)

    print(f"\n[+] Publicador iniciado exitosamente en {p}")
    print("[*] Publicando mensajes cada 5 segundos... (Presiona Ctrl+C para detener)\n")

    cont = 0
    while True:
        time.sleep(5)
        cont += 1
        msg = f"TIME {time.asctime()} - Message #{cont}"
        s.send(msg.encode("utf-8"))
        print(f"[>] Publicado #{cont}: {msg}")

except KeyboardInterrupt:
    print("\n[!] Publicador detenido por el usuario.")
finally:
    s.close()
    context.term()

