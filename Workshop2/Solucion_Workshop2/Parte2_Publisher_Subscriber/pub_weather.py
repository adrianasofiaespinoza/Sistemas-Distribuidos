"""
Publisher 1: Servicio de Clima / Weather (Puerto 15001)
Sistemas Distribuidos - Workshop 2 (Parte 2: Actividad 4)
"""

import zmq
import time
import random
import sys

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 15001
    host = sys.argv[2] if len(sys.argv) > 2 else "*"

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    bind_url = f"tcp://{host}:{port}"
    socket.bind(bind_url)

    print("=" * 60)
    print(f" PUBLISHER 1: SERVICIO DE CLIMA (WEATHER)")
    print(f" Escuchando en: {bind_url}")
    print("=" * 60)

    cities = ["Quito", "Ibarra", "Cuenca", "Guayaquil", "Manta", "Loja"]
    conditions = ["Soleado", "Lluvia ligera", "Nublado", "Tormenta eléctrica", "Despejado", "Viento fuerte"]
    
    time.sleep(0.5)
    count = 0
    try:
        while True:
            time.sleep(2.5)
            count += 1
            city = random.choice(cities)
            temp = round(random.uniform(11.0, 29.0), 1)
            hum = random.randint(35, 95)
            cond = random.choice(conditions)
            
            # Formato de mensaje con tópico WEATHER
            msg = f"WEATHER [{time.strftime('%H:%M:%S')}] #{count} en {city}: {temp}°C, Humedad {hum}%, {cond}"
            socket.send_string(msg)
            print(f"[WEATHER PUB] Emitido: {msg}")
    except KeyboardInterrupt:
        print("\nPublisher Weather detenido.")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    main()
