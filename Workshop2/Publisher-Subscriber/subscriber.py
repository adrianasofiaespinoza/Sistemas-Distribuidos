import zmq
import sys

context = zmq.Context()
s = context.socket(zmq.SUB)

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
        s.connect(p)
    except zmq.ZMQError as e:
        print(f"\n[ERROR] No se pudo conectar a '{p}': {e}")
        sys.exit(1)

    # Suscribirse al tópico "TIME"
    s.setsockopt_string(zmq.SUBSCRIBE, "TIME")

    print(f"\n[+] Suscriptor conectado a {p}")
    print("[*] Esperando mensajes con tópico 'TIME'... (Presiona Ctrl+C para salir)\n")

    msg_count = 0
    while True:
        data = s.recv().decode("utf-8")
        msg_count += 1
        print(f"[<] Recibido ({msg_count}): {data}")

except KeyboardInterrupt:
    print("\n[!] Suscriptor detenido por el usuario.")
finally:
    s.close()
    context.term()

