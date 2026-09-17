import zmq
import time
import random
import sys
from collections import deque

SERVER_PORT = 8000
HOSTNAME = "localhost"
NUM_REQUESTS = 3        # Peticiones por cliente
CS_TIME = 2             # Tiempo maximo en seccion critica


class CentralCoordinator:
    def __init__(self):
        self.context = zmq.Context()
        self.queue = deque()       # Cola de espera
        self.holder = None         # Quien tiene el recurso

    def run(self):
        socket = self.context.socket(zmq.ROUTER)
        socket.setsockopt(zmq.LINGER, 0)
        socket.bind(f"tcp://*:{SERVER_PORT}")
        print(f"Coordinador corriendo en puerto {SERVER_PORT}")

        try:
            while True:
                if not socket.poll(timeout=1000):
                    continue

                frames = socket.recv_multipart()
                client_id = frames[0]
                msg = frames[2].decode('utf-8')
                name = client_id.decode('utf-8', errors='replace')

                if msg == "LOCK_REQUEST":
                    if self.holder is None:
                        # Recurso libre, conceder
                        self.holder = client_id
                        socket.send_multipart([client_id, b"", b"LOCK_GRANTED"])
                        print(f"  LOCK_GRANTED a {name}")
                    else:
                        # Recurso ocupado, encolar
                        self.queue.append(client_id)
                        socket.send_multipart([client_id, b"", b"LOCK_QUEUED"])
                        print(f"  LOCK_QUEUED {name} (cola: {len(self.queue)})")

                elif msg == "RELEASE":
                    socket.send_multipart([client_id, b"", b"RELEASE_ACK"])
                    if client_id == self.holder:
                        self.holder = None
                        if self.queue:
                            # Dar acceso al siguiente en la cola
                            nxt = self.queue.popleft()
                            self.holder = nxt
                            socket.send_multipart([nxt, b"", b"LOCK_GRANTED"])
                            print(f"  LOCK_GRANTED a {nxt.decode('utf-8', errors='replace')}")
                        else:
                            print("  Recurso libre")

        except KeyboardInterrupt:
            print("Coordinador detenido")
        finally:
            socket.close()
            self.context.term()


class ResourceClient:
    def __init__(self, client_id):
        self.name = f"Cliente-{client_id}"
        self.context = zmq.Context()

    def run(self):
        socket = self.context.socket(zmq.DEALER)
        socket.setsockopt_string(zmq.IDENTITY, self.name)
        socket.setsockopt(zmq.RCVTIMEO, 30000)
        socket.setsockopt(zmq.LINGER, 0)
        socket.connect(f"tcp://{HOSTNAME}:{SERVER_PORT}")

        try:
            for i in range(NUM_REQUESTS):
                time.sleep(random.uniform(0.5, 2))

                # Pedir acceso
                socket.send_multipart([b"", b"LOCK_REQUEST"])

                while True:
                    resp = socket.recv_multipart()
                    r = resp[1].decode('utf-8')
                    if r == "LOCK_GRANTED":
                        print(f"[{self.name}] Acceso concedido - entrando a seccion critica")
                        break
                    elif r == "LOCK_QUEUED":
                        print(f"[{self.name}] En cola...")

                # Seccion critica
                t = random.uniform(1, CS_TIME)
                time.sleep(t)
                print(f"[{self.name}] Saliendo de seccion critica")

                # Liberar
                socket.send_multipart([b"", b"RELEASE"])
                socket.recv_multipart()

        except zmq.Again:
            print(f"[{self.name}] Timeout")
        except KeyboardInterrupt:
            pass
        finally:
            socket.close()
            self.context.term()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python central_server.py server")
        print("  python central_server.py client <id>")
        sys.exit(1)

    role = sys.argv[1].lower()

    if role == "server":
        CentralCoordinator().run()
    elif role == "client":
        cid = int(sys.argv[2])
        ResourceClient(cid).run()
    else:
        print(f"Rol desconocido: {role}")
