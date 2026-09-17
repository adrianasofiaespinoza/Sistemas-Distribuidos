import zmq
import time
import random
import sys

NUM_PROCESSES = 3
BASE_PORT = 9000
HOSTNAME = "localhost"
NUM_ROUNDS = 5
CS_PROB = 0.6            # Probabilidad de querer entrar a seccion critica
CS_TIME = 2              # Tiempo maximo en seccion critica


class TokenRingProcess:
    def __init__(self, pid):
        self.pid = pid
        self.context = zmq.Context()
        self.my_port = BASE_PORT + pid
        self.next_port = BASE_PORT + ((pid + 1) % NUM_PROCESSES)
        self.cs_count = 0

    def run(self):
        # Socket para recibir el token
        pull = self.context.socket(zmq.PULL)
        pull.setsockopt(zmq.LINGER, 0)
        pull.bind(f"tcp://*:{self.my_port}")
        print(f"[P{self.pid}] Escuchando en {self.my_port}, siguiente: {self.next_port}")

        # Socket para enviar el token al siguiente
        push = self.context.socket(zmq.PUSH)
        push.setsockopt(zmq.LINGER, 1000)
        push.connect(f"tcp://{HOSTNAME}:{self.next_port}")

        # Proceso 0 crea el token
        if self.pid == 0:
            time.sleep(2)
            print(f"[P{self.pid}] Creando token...")
            tmp = self.context.socket(zmq.PUSH)
            tmp.setsockopt(zmq.LINGER, 1000)
            tmp.connect(f"tcp://{HOSTNAME}:{self.my_port}")
            time.sleep(0.5)
            tmp.send_string("TOKEN")
            tmp.close()

        try:
            while self.cs_count < NUM_ROUNDS:
                if not pull.poll(timeout=30000):
                    continue

                token = pull.recv_string()

                if token == "TOKEN":
                    quiere_cs = random.random() < CS_PROB

                    if quiere_cs and self.cs_count < NUM_ROUNDS:
                        self.cs_count += 1
                        print(f"[P{self.pid}] Entrando a seccion critica ({self.cs_count}/{NUM_ROUNDS})")
                        t = random.uniform(0.5, CS_TIME)
                        time.sleep(t)
                        print(f"[P{self.pid}] Saliendo de seccion critica")
                    else:
                        time.sleep(0.3)

                    # Pasar token al siguiente
                    push.send_string("TOKEN")

        except KeyboardInterrupt:
            pass
        finally:
            print(f"[P{self.pid}] Total accesos: {self.cs_count}")
            pull.close()
            push.close()
            self.context.term()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: python token_ring.py <process_id>  (0 a {NUM_PROCESSES-1})")
        print("  El proceso 0 crea el token")
        sys.exit(1)

    pid = int(sys.argv[1])
    TokenRingProcess(pid).run()
