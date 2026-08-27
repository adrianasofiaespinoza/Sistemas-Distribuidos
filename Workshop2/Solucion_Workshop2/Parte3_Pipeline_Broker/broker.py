"""
Broker Intermediario para Pipeline (Source -> Broker -> Worker)
Sistemas Distribuidos - Workshop 2 (Parte 3: Actividad 6)
"""

import zmq
import pickle
import time
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Broker Central del Pipeline ZeroMQ")
    parser.add_argument("--frontend-port", type=int, default=13001, help="Puerto de entrada única para Sources (PULL)")
    parser.add_argument("--backend-port", type=int, default=13002, help="Puerto de salida única para Workers (PUSH)")
    parser.add_argument("--host", type=str, default="*", help="Host para bind (* para todas las interfaces)")
    args = parser.parse_args()

    context = zmq.Context()

    # 1. Frontend: Entrada única para recibir tareas de múltiples fuentes (PULL)
    frontend = context.socket(zmq.PULL)
    frontend_addr = f"tcp://{args.host}:{args.frontend_port}"
    frontend.bind(frontend_addr)

    # 2. Backend: Salida única para distribuir tareas a múltiples workers (PUSH)
    backend = context.socket(zmq.PUSH)
    backend_addr = f"tcp://{args.host}:{args.backend_port}"
    backend.bind(backend_addr)

    print("=" * 70)
    print(" BROKER INTERMEDIARIO DE PIPELINE INICIADO")
    print("=" * 70)
    print(f" [+] Entrada Frontend (PULL para Sources) : {frontend_addr}")
    print(f" [+] Salida Backend    (PUSH para Workers) : {backend_addr}")
    print("-" * 70)
    print(" Enrutando tareas desde múltiples fuentes hacia múltiples workers...")
    print(" Presione Ctrl+C para detener el broker.\n")

    total_relayed = 0
    try:
        while True:
            # Recibir mensaje de cualquier fuente conectada
            msg_bytes = frontend.recv()
            task = pickle.loads(msg_bytes)
            total_relayed += 1

            source_id = task.get("source_id", "Desconocida")
            task_id = task.get("task_id", total_relayed)
            workload = task.get("workload", 0)

            print(f"[BROKER] Tarea #{total_relayed} recibida de [{source_id}] (TaskID: {task_id}, Carga: {workload} ms) -> Reenviando a Workers...")

            # Reenviar mensaje al backend para que el worker disponible lo procese
            backend.send(msg_bytes)

    except KeyboardInterrupt:
        print(f"\n[BROKER] Detenido por el usuario. Total de tareas canalizadas: {total_relayed}")
    finally:
        frontend.close()
        backend.close()
        context.term()


if __name__ == "__main__":
    main()
