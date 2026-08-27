"""
Fuente de Tareas / Source para Pipeline (ZeroMQ PUSH)
Sistemas Distribuidos - Workshop 2 (Parte 3: Actividad 6)
"""

import zmq
import time
import pickle
import random
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Fuente (Source) para Pipeline ZeroMQ")
    parser.add_argument("--id", type=str, default="Source-1", help="Identificador único de la fuente")
    parser.add_argument("--broker-host", type=str, default="localhost", help="Host del Broker intermediario")
    parser.add_argument("--broker-port", type=int, default=13001, help="Puerto frontend del Broker")
    parser.add_argument("--tasks", type=int, default=10, help="Número de tareas a enviar (0 para infinito)")
    parser.add_argument("--delay", type=float, default=0.5, help="Pausa entre envíos en segundos")
    parser.add_argument("--min-work", type=int, default=10, help="Carga de trabajo mínima")
    parser.add_argument("--max-work", type=int, default=100, help="Carga de trabajo máxima")
    args = parser.parse_args()

    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    broker_addr = f"tcp://{args.broker_host}:{args.broker_port}"
    sender.connect(broker_addr)

    print("=" * 65)
    print(f" FUENTE INICIADA: [{args.id}]")
    print("=" * 65)
    print(f" Conectada al frontend del broker: {broker_addr}")
    print(f" Total de tareas a generar: {args.tasks if args.tasks > 0 else 'Infinito'}")
    print(f" Intervalo de envío: {args.delay} s")
    print("-" * 65)

    # Pausa corta para conexión
    time.sleep(0.3)

    count = 0
    try:
        while True:
            count += 1
            workload = random.randint(args.min_work, args.max_work)
            
            task_payload = {
                "source_id": args.id,
                "task_id": count,
                "workload": workload,
                "description": f"Cálculo/Procesamiento #{count}",
                "timestamp": time.time(),
                "time_str": time.strftime("%H:%M:%S")
            }

            sender.send(pickle.dumps(task_payload))
            print(f"[{args.id}] -> Tarea #{count} enviada al Broker (Carga: {workload} ms)")

            if args.tasks > 0 and count >= args.tasks:
                print(f"\n[OK] Fuente [{args.id}] completó el envío de sus {args.tasks} tareas.")
                break

            time.sleep(args.delay)

    except KeyboardInterrupt:
        print(f"\nFuente [{args.id}] detenida por el usuario.")
    finally:
        sender.close()
        context.term()


if __name__ == "__main__":
    main()
