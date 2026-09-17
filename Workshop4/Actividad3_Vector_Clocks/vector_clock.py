import zmq
import threading
import time
import random
import sys
import json

NUM_PROCESSES = 3
BASE_PULL_PORT = 7100     # Puertos para recibir mensajes
HOSTNAME = "localhost"
NUM_EVENTS = 8
EVENT_INTERVAL = 2


class VectorClock:
    def __init__(self, pid, n):
        self.pid = pid
        self.n = n
        self.clock = [0] * n
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.clock[self.pid] += 1

    def get(self):
        with self.lock:
            return list(self.clock)

    def on_send(self):
        with self.lock:
            self.clock[self.pid] += 1
            return list(self.clock)

    def on_receive(self, other_clock):
        # Tomar el maximo elemento a elemento y luego incrementar
        with self.lock:
            for i in range(self.n):
                self.clock[i] = max(self.clock[i], other_clock[i])
            self.clock[self.pid] += 1

    def __str__(self):
        return str(self.clock)


class ProcessNode:
    def __init__(self, pid):
        self.pid = pid
        self.vc = VectorClock(pid, NUM_PROCESSES)
        self.context = zmq.Context()
        self.running = True
        self.events = []

    def receiver_thread(self):
        # Hilo que escucha mensajes entrantes
        socket = self.context.socket(zmq.PULL)
        socket.setsockopt(zmq.LINGER, 0)
        port = BASE_PULL_PORT + self.pid
        socket.bind(f"tcp://*:{port}")
        print(f"[P{self.pid}] Receptor en puerto {port}")

        while self.running:
            try:
                if socket.poll(timeout=1000):
                    raw = socket.recv_string()
                    msg = json.loads(raw)
                    self.vc.on_receive(msg["clock"])
                    print(f"[P{self.pid}] RECIBIR de P{msg['sender']} -> VC={self.vc}")
                    self.events.append(("RECIBIR", self.vc.get(), f"de P{msg['sender']}"))
            except zmq.ZMQError:
                break
        socket.close()

    def send_message(self, target):
        socket = self.context.socket(zmq.PUSH)
        socket.setsockopt(zmq.SNDTIMEO, 3000)
        socket.setsockopt(zmq.LINGER, 0)

        try:
            socket.connect(f"tcp://{HOSTNAME}:{BASE_PULL_PORT + target}")
            clock = self.vc.on_send()
            msg = json.dumps({"sender": self.pid, "clock": clock})
            time.sleep(0.1)
            socket.send_string(msg)
            print(f"[P{self.pid}] ENVIAR a P{target} -> VC={self.vc}")
            self.events.append(("ENVIAR", self.vc.get(), f"a P{target}"))
        except zmq.ZMQError as e:
            print(f"[P{self.pid}] Error enviando a P{target}: {e}")
        finally:
            socket.close()

    def internal_event(self):
        self.vc.increment()
        print(f"[P{self.pid}] INTERNO -> VC={self.vc}")
        self.events.append(("INTERNO", self.vc.get(), ""))

    def run(self):
        recv = threading.Thread(target=self.receiver_thread, daemon=True)
        recv.start()
        time.sleep(1)

        print(f"[P{self.pid}] Iniciado. VC={self.vc}")

        try:
            for i in range(NUM_EVENTS):
                tipo = random.choice(["internal", "send", "send"])
                if tipo == "internal":
                    self.internal_event()
                else:
                    targets = [j for j in range(NUM_PROCESSES) if j != self.pid]
                    self.send_message(random.choice(targets))
                time.sleep(EVENT_INTERVAL + random.uniform(0, 1))
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            time.sleep(0.5)
            # Resumen
            print(f"\n[P{self.pid}] === Resumen ===")
            for i, (tipo, vc, det) in enumerate(self.events):
                print(f"  {i+1}. {tipo:8s} VC={vc} {det}")
            self.context.term()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: python vector_clock.py <process_id>  (0 a {NUM_PROCESSES-1})")
        sys.exit(1)

    pid = int(sys.argv[1])
    node = ProcessNode(pid)
    node.run()
