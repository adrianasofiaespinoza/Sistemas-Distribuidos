"""
Publisher Genérico de Servicios (ZeroMQ PUB)
Sistemas Distribuidos - Workshop 2 (Parte 2: Actividad 4)
"""

import zmq
import time
import random
import sys
import argparse


# Generadores de mensajes según el tipo de servicio
def get_service_message(service_name, count):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    if service_name.upper() == "WEATHER":
        cities = ["Quito", "Ibarra", "Cuenca", "Guayaquil", "Ambato"]
        conditions = ["Soleado", "Lluvia ligera", "Nublado", "Tormenta", "Despejado"]
        city = random.choice(cities)
        temp = round(random.uniform(12.0, 28.5), 1)
        hum = random.randint(40, 95)
        cond = random.choice(conditions)
        payload = f"[{city}] Temp: {temp}°C | Humedad: {hum}% | Estado: {cond}"

    elif service_name.upper() == "FINANCE":
        assets = [
            ("USD/EUR", round(random.uniform(0.90, 0.96), 4)),
            ("BTC/USD", round(random.uniform(60000, 70000), 2)),
            ("AAPL", round(random.uniform(180, 230), 2)),
            ("NVDA", round(random.uniform(115, 140), 2)),
            ("PETROLEO_WTI", round(random.uniform(70, 85), 2))
        ]
        asset, price = random.choice(assets)
        change = round(random.uniform(-3.5, 3.5), 2)
        sign = "+" if change > 0 else ""
        payload = f"[{asset}] Precio: ${price} ({sign}{change}%)"

    elif service_name.upper() == "SPORTS":
        matches = [
            "Real Madrid vs Barcelona",
            "LDU Quito vs Independiente del Valle",
            "Man City vs Arsenal",
            "PSG vs Bayern Munich"
        ]
        events = ["¡GOL!", "Tarjeta Amarilla", "Tiro de esquina", "Fin del Primer Tiempo", "Penal sancionado"]
        match = random.choice(matches)
        event = random.choice(events)
        minute = random.randint(1, 90)
        payload = f"[{match}] Min {minute}': {event}"

    elif service_name.upper() == "TRAFFIC":
        avenues = ["Av. Simón Bolívar", "Av. Occidental", "Panamericana Norte", "Av. 10 de Agosto"]
        status = ["Tráfico fluido", "Congestión moderada", "Vía cerrada por mantenimiento", "Tráfico pesado"]
        payload = f"[{random.choice(avenues)}] Estado: {random.choice(status)}"

    else:
        payload = f"Mensaje de datos generales #{count} generado aleatoriamente (ID: {random.randint(1000, 9999)})"

    # Estructura del mensaje: TOPIC TIMESTAMP - PAYLOAD
    topic = service_name.upper()
    message = f"{topic} [{timestamp}] Msg #{count} -> {payload}"
    return message


def main():
    parser = argparse.ArgumentParser(description="Publisher de Servicios ZeroMQ")
    parser.add_argument("--service", type=str, default="WEATHER", help="Nombre del servicio/tópico (ej: WEATHER, FINANCE, SPORTS, TRAFFIC)")
    parser.add_argument("--port", type=int, default=15001, help="Puerto de escucha del publisher")
    parser.add_argument("--host", type=str, default="*", help="Host para bind (usar * para todas las interfaces o IP específica)")
    parser.add_argument("--interval", type=float, default=2.0, help="Intervalo de publicación en segundos")
    args = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    bind_address = f"tcp://{args.host}:{args.port}"
    socket.bind(bind_address)

    print("=" * 65)
    print(f" PUBLISHER INICIADO - SERVICIO: [{args.service.upper()}]")
    print("=" * 65)
    print(f"Dirección de publicación: {bind_address}")
    print(f"Intervalo de envío: {args.interval} segundos")
    print("Esperando suscriptores y transmitiendo eventos...")
    print("Presione Ctrl+C para detener el publisher.\n")

    # Breve pausa para permitir que conexiones iniciales se sincronicen
    time.sleep(0.5)

    count = 0
    try:
        while True:
            count += 1
            msg = get_service_message(args.service, count)
            socket.send_string(msg)
            print(f"[ENVIADO] {msg}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print(f"\nPublisher [{args.service}] detenido.")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
