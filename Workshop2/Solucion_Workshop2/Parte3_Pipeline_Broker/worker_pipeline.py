"""
Trabajador / Worker para Pipeline (ZeroMQ PULL)
Sistemas Distribuidos - Workshop 2 (Parte 3: Actividad 6)
"""

import zmq
import time
import pickle
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Worker para Pipeline ZeroMQ")
    parser.add_argument("--id", type=str, default="Worker-1", help="Identificador único del worker")
    parser.add_argument("--broker-host", type=str, default="localhost", help="Host del Broker intermediario")
    parser.add_argument("--broker-port", type=int, default=13002, help="Puerto backend del Broker")
    parser.add_argument("--speed-factor", type=float, default=0.01, help="Factor de escala para simular tiempo de cómputo (segundos por unidad de carga)")
    args = parser.parse_args()

    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    broker_addr = f"tcp://{args.broker_host}:{args.broker_port}"
    receiver.connect(broker_addr)

    print("=" * 65)
    print(f" WORKER INICIADO: [{args.id}]")
    print("=" * 65)
    print(f" Conectado al backend del broker: {broker_addr}")
    print(" Esperando asignación de tareas distribuidas...")
    print(" Presione Ctrl+C para detener el worker.\n")

    processed_count = 0
    total_workload = 0

    try:
        while True:
            msg_bytes = receiver.recv()
            task = pickle.loads(msg_bytes)
            processed_count += 1

            source_id = task.get("source_id", "Desconocida")
            task_id = task.get("task_id", processed_count)
            workload = task.get("workload", 10)
            total_workload += workload

            print(f"[{args.id}] RECIBIDO: Tarea #{task_id} de [{source_id}] | Carga: {workload} u")

            # Simular tiempo de procesamiento
            sleep_duration = workload * args.speed_factor
            time.sleep(sleep_duration)

            print(f"[{args.id}] COMPLETADO: Tarea #{task_id} de [{source_id}] (Procesadas totales: {processed_count})")
            print("-" * 50)

    except KeyboardInterrupt:
        print(f"\nWorker [{args.id}] detenido. Tareas procesadas: {processed_count}, Carga acumulada: {total_workload}")
    finally:
        receiver.close()
        context.term()


if __name__ == "__main__":
    main()
