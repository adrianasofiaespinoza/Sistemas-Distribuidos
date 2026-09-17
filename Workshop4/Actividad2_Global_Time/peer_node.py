import zmq
import threading
import time
import random
import sys

NUM_PEERS = 3
BASE_PORT = 6000
SYNC_INTERVAL = 3
DRIFT_EVERY_K = 2       # Cada cuantos ciclos se agrega drift
MAX_DRIFT = 5            # Drift maximo en segundos
NUM_ROUNDS = 10
HOSTNAME = "localhost"


class PeerNode:
    def __init__(self, peer_id):
        self.peer_id = peer_id
        self.port = BASE_PORT + peer_id
        self.clock_offset = random.uniform(-3, 3)  # Offset inicial aleatorio
        self.lock = threading.Lock()
        self.context = zmq.Context()
        self.running = True

    def get_local_time(self):
        return time.time() + self.clock_offset

    def get_local_time_str(self):
        ts = self.get_local_time()
        return time.strftime('%H:%M:%S', time.localtime(ts))

    def server_thread(self):
        # Hilo que responde peticiones de tiempo de otros peers
        socket = self.context.socket(zmq.REP)
        socket.setsockopt(zmq.LINGER, 0)
        socket.bind(f"tcp://*:{self.port}")
        print(f"[Peer {self.peer_id}] Escuchando en puerto {self.port}")

        while self.running:
            try:
                if socket.poll(timeout=1000):
                    msg = socket.recv_string()
                    if msg == "TIME_REQUEST":
                        socket.send_string(str(self.get_local_time()))
                    else:
                        socket.send_string("ERROR")
            except zmq.ZMQError:
                break
        socket.close()

    def request_time(self, peer_port):
        # Pedir el tiempo a otro peer
        socket = self.context.socket(zmq.REQ)
        socket.setsockopt(zmq.RCVTIMEO, 3000)
        socket.setsockopt(zmq.LINGER, 0)
        try:
            socket.connect(f"tcp://{HOSTNAME}:{peer_port}")
            socket.send_string("TIME_REQUEST")
            resp = socket.recv_string()
            return float(resp)
        except:
            return None
        finally:
            socket.close()

    def synchronize(self, ronda):
        print(f"\n[Peer {self.peer_id}] Ronda {ronda+1} - Tiempo antes: {self.get_local_time_str()} (offset: {self.clock_offset:+.3f}s)")

        times = [self.get_local_time()]

        for i in range(NUM_PEERS):
            if i == self.peer_id:
                continue
            t = self.request_time(BASE_PORT + i)
            if t is not None:
                times.append(t)

        if len(times) > 1:
            promedio = sum(times) / len(times)
            with self.lock:
                old = self.clock_offset
                self.clock_offset = promedio - time.time()
                print(f"[Peer {self.peer_id}] Promedio de {len(times)} peers. Ajuste: {self.clock_offset - old:+.3f}s")
        else:
            print(f"[Peer {self.peer_id}] Sin respuesta de otros peers")

        print(f"[Peer {self.peer_id}] Tiempo despues: {self.get_local_time_str()} (offset: {self.clock_offset:+.3f}s)")

    def run(self):
        srv = threading.Thread(target=self.server_thread, daemon=True)
        srv.start()
        time.sleep(1)

        try:
            for r in range(NUM_ROUNDS):
                self.synchronize(r)
                # Agregar drift cada k ciclos
                if (r + 1) % DRIFT_EVERY_K == 0:
                    drift = random.uniform(-MAX_DRIFT, MAX_DRIFT)
                    with self.lock:
                        self.clock_offset += drift
                    print(f"[Peer {self.peer_id}] Drift aplicado: {drift:+.3f}s")
                time.sleep(SYNC_INTERVAL)
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            self.context.term()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: python peer_node.py <peer_id>  (0 a {NUM_PEERS-1})")
        sys.exit(1)

    pid = int(sys.argv[1])
    peer = PeerNode(pid)
    peer.run()
