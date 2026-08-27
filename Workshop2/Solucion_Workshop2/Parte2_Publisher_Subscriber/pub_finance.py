"""
Publisher 2: Servicio Financiero / Finance (Puerto 15002)
Sistemas Distribuidos - Workshop 2 (Parte 2: Actividad 4)
"""

import zmq
import time
import random
import sys

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 15002
    host = sys.argv[2] if len(sys.argv) > 2 else "*"

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    bind_url = f"tcp://{host}:{port}"
    socket.bind(bind_url)

    print("=" * 60)
    print(f" PUBLISHER 2: SERVICIO FINANCIERO (FINANCE)")
    print(f" Escuchando en: {bind_url}")
    print("=" * 60)

    symbols = [
        ("USD/EUR", 0.92, 0.005),
        ("BTC/USD", 64500.0, 350.0),
        ("ETH/USD", 3450.0, 25.0),
        ("AAPL", 225.0, 1.5),
        ("NVDA", 128.0, 2.0),
        ("TSLA", 215.0, 3.2),
        ("ORO/OZ", 2510.0, 8.0)
    ]
    
    time.sleep(0.5)
    count = 0
    try:
        while True:
            time.sleep(3.0)
            count += 1
            sym, base_val, delta = random.choice(symbols)
            var = round(random.uniform(-delta, delta), 2 if base_val > 10 else 4)
            current_val = round(base_val + var, 2 if base_val > 10 else 4)
            pct = round((var / base_val) * 100, 2)
            sign = "+" if pct >= 0 else ""
            
            # Formato de mensaje con tópico FINANCE
            msg = f"FINANCE [{time.strftime('%H:%M:%S')}] #{count} Cotización {sym}: ${current_val} ({sign}{pct}%)"
            socket.send_string(msg)
            print(f"[FINANCE PUB] Emitido: {msg}")
    except KeyboardInterrupt:
        print("\nPublisher Finance detenido.")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    main()
