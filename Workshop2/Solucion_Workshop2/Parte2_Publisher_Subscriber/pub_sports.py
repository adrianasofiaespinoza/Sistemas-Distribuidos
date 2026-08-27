"""
Publisher 3: Servicio de Deportes / Sports (Puerto 15003)
Sistemas Distribuidos - Workshop 2 (Parte 2: Actividad 4)
"""

import zmq
import time
import random
import sys

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 15003
    host = sys.argv[2] if len(sys.argv) > 2 else "*"

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    bind_url = f"tcp://{host}:{port}"
    socket.bind(bind_url)

    print("=" * 60)
    print(f" PUBLISHER 3: SERVICIO DE DEPORTES (SPORTS)")
    print(f" Escuchando en: {bind_url}")
    print("=" * 60)

    events = [
        ("LigaPro", "LDU Quito 1 - 0 Barcelona SC", "Gol de tiro libre min 34'"),
        ("Champions League", "Real Madrid 2 - 1 Bayern Munich", "Tarjeta roja min 78'"),
        ("Premier League", "Arsenal 2 - 2 Man City", "Empate agónico min 90+4'"),
        ("NBA", "Lakers 108 - 104 Warriors", "Triple sobre la chicharra"),
        ("Copa Libertadores", "Flamengo 0 - 0 Independiente del Valle", "Inicio segundo tiempo")
    ]
    
    time.sleep(0.5)
    count = 0
    try:
        while True:
            time.sleep(3.5)
            count += 1
            league, match, detail = random.choice(events)
            
            # Formato de mensaje con tópico SPORTS
            msg = f"SPORTS [{time.strftime('%H:%M:%S')}] #{count} [{league}] {match} | {detail}"
            socket.send_string(msg)
            print(f"[SPORTS PUB] Emitido: {msg}")
    except KeyboardInterrupt:
        print("\nPublisher Sports detenido.")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    main()
