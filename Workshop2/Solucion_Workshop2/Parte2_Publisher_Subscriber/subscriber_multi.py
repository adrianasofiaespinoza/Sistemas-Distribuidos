"""
Suscriptor Multi-Servicio (ZeroMQ SUB)
Sistemas Distribuidos - Workshop 2 (Parte 2: Actividad 4)
"""

import zmq
import time
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Suscriptor Multi-Publisher ZeroMQ")
    parser.add_argument("--name", type=str, default="Suscriptor-1", help="Nombre o identificador del suscriptor")
    parser.add_argument("--endpoints", nargs="+", default=["tcp://localhost:15001", "tcp://localhost:15002", "tcp://localhost:15003"],
                        help="Lista de endpoints de los publishers (ej: tcp://localhost:15001 tcp://localhost:15002)")
    parser.add_argument("--topics", nargs="+", default=["WEATHER", "FINANCE", "SPORTS"],
                        help="Tópicos a los cuales suscribirse (ej: WEATHER, FINANCE, SPORTS, o ALL para todos)")
    parser.add_argument("--count", type=int, default=0, help="Número de mensajes a recibir antes de finalizar (0 = infinito)")
    args = parser.parse_args()

    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)

    print("=" * 65)
    print(f" SUSCRIPTOR INICIADO: [{args.name}]")
    print("=" * 65)

    # Conectar a cada uno de los endpoints de publishers especificados
    print("Conectando a endpoints de publishers:")
    for ep in args.endpoints:
        sub_socket.connect(ep)
        print(f" -> Conectado a: {ep}")

    # Configurar filtros de suscripción
    print("\nSuscrito a los tópicos:")
    for topic in args.topics:
        if topic.upper() == "ALL" or topic == "":
            sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
            print(" -> [TODOS LOS TÓPICOS] (Filtro vacío)")
            break
        else:
            t_upper = topic.upper()
            sub_socket.setsockopt_string(zmq.SUBSCRIBE, t_upper)
            print(f" -> Tópico: [{t_upper}]")

    print("-" * 65)
    print("Esperando mensajes de los publishers...")
    print("Presione Ctrl+C para detener el suscriptor.\n")

    received = 0
    try:
        while True:
            raw_msg = sub_socket.recv_string()
            received += 1
            
            # Formateo visual del mensaje recibido
            parts = raw_msg.split(" ", 1)
            topic_tag = parts[0] if len(parts) > 0 else "UNKNOWN"
            content = parts[1] if len(parts) > 1 else raw_msg

            print(f"[{args.name}] [RECIBIDO #{received}] ({topic_tag}) {content}")

            if args.count > 0 and received >= args.count:
                print(f"\nLímite de {args.count} mensajes alcanzado. Finalizando.")
                break

    except KeyboardInterrupt:
        print(f"\nSuscriptor [{args.name}] detenido por el usuario.")
    finally:
        sub_socket.close()
        context.term()


if __name__ == "__main__":
    main()
