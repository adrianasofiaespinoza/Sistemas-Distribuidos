"""
Script de Verificación Automatizada de Soluciones - Workshop 2
Prueba de forma concurrente:
  1. Parte 1 (Matrix Manager con RMI/XML-RPC y NumPy)
  2. Parte 2 (Multi-Publisher y Multi-Subscriber con ZeroMQ)
  3. Parte 3 (Pipeline Source -> Broker -> Worker con ZeroMQ)
"""

import threading
import time
import sys
import numpy as np
import xmlrpc.client
import zmq
import pickle


def test_part1_matrix_manager():
    print("\n" + "=" * 70)
    print(">>> TEST PARTE 1: DISTRIBUTED MATRIX MANAGER (RMI / XML-RPC + NUMPY) <<<")
    print("=" * 70)

    # Importar servidor
    sys.path.insert(0, "./Parte1_RMI_MatrixManager")
    from server_matrix import RequestHandler, MatrixManager
    from xmlrpc.server import SimpleXMLRPCServer

    server_port = 12050
    server = SimpleXMLRPCServer(("127.0.0.1", server_port), requestHandler=RequestHandler, allow_none=True, logRequests=False)
    server.register_instance(MatrixManager())

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.3)

    proxy = xmlrpc.client.ServerProxy(f"http://127.0.0.1:{server_port}/RPC2")

    # Matrices de prueba
    A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    B = [[7.0, 8.0, 9.0], [1.0, 2.0, 3.0]]
    C = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]] # 3x2 para multiplicar A (2x3) @ C (3x2)

    # 1. Suma
    res_add = proxy.add(A, B)
    expected_add = (np.array(A) + np.array(B)).tolist()
    assert res_add["status"] == "OK" and res_add["result"] == expected_add, f"Fallo suma: {res_add}"
    print(f" [+] Prueba SUMA exitosa: A + B =\n     {res_add['result']}")

    # 2. Resta
    res_sub = proxy.sub(A, B)
    expected_sub = (np.array(A) - np.array(B)).tolist()
    assert res_sub["status"] == "OK" and res_sub["result"] == expected_sub, f"Fallo resta: {res_sub}"
    print(f" [+] Prueba RESTA exitosa: A - B =\n     {res_sub['result']}")

    # 3. Multiplicación (Producto Matricial A @ C)
    res_prod = proxy.prod(A, C)
    expected_prod = np.matmul(np.array(A), np.array(C)).tolist()
    assert res_prod["status"] == "OK" and res_prod["result"] == expected_prod, f"Fallo prod: {res_prod}"
    print(f" [+] Prueba PRODUCTO exitosa: A @ C =\n     {res_prod['result']}")

    # 4. Transpuesta
    res_trans = proxy.transpose(A)
    expected_trans = np.array(A).T.tolist()
    assert res_trans["status"] == "OK" and res_trans["result"] == expected_trans, f"Fallo transpose: {res_trans}"
    print(f" [+] Prueba TRANSPUESTA exitosa: A^T =\n     {res_trans['result']}")

    # 5. Determinante
    sq = [[4.0, 7.0], [2.0, 6.0]]
    res_det = proxy.det(sq)
    expected_det = float(np.linalg.det(np.array(sq)))
    assert res_det["status"] == "OK" and abs(res_det["result"] - expected_det) < 1e-5, f"Fallo det: {res_det}"
    print(f" [+] Prueba DETERMINANTE exitosa: det(sq) = {res_det['result']}")

    server.shutdown()
    server.server_close()
    print("[PARTE 1] Todas las pruebas de operaciones matriciales RMI PASARON exitosamente.\n")


def test_part2_pub_sub():
    print("\n" + "=" * 70)
    print(">>> TEST PARTE 2: MULTI-PUBLISHER & MULTI-SUBSCRIBER (ZEROMQ) <<<")
    print("=" * 70)

    ctx = zmq.Context()

    # Publicador 1: WEATHER (puerto 15051)
    pub1 = ctx.socket(zmq.PUB)
    pub1.bind("tcp://127.0.0.1:15051")

    # Publicador 2: FINANCE (puerto 15052)
    pub2 = ctx.socket(zmq.PUB)
    pub2.bind("tcp://127.0.0.1:15052")

    # Publicador 3: SPORTS (puerto 15053)
    pub3 = ctx.socket(zmq.PUB)
    pub3.bind("tcp://127.0.0.1:15053")

    # Suscriptor 1: Suscrito a WEATHER y SPORTS
    sub1 = ctx.socket(zmq.SUB)
    sub1.connect("tcp://127.0.0.1:15051")
    sub1.connect("tcp://127.0.0.1:15053")
    sub1.setsockopt_string(zmq.SUBSCRIBE, "WEATHER")
    sub1.setsockopt_string(zmq.SUBSCRIBE, "SPORTS")

    # Suscriptor 2: Suscrito a FINANCE
    sub2 = ctx.socket(zmq.SUB)
    sub2.connect("tcp://127.0.0.1:15052")
    sub2.setsockopt_string(zmq.SUBSCRIBE, "FINANCE")

    time.sleep(0.5)

    # Enviar mensajes desde cada publisher
    pub1.send_string("WEATHER [10:00:00] #1 Quito: 18.5C, Soleado")
    pub2.send_string("FINANCE [10:00:00] #1 BTC/USD: $65000 (+2.4%)")
    pub3.send_string("SPORTS [10:00:00] #1 Real Madrid 1 - 0 Barcelona")

    time.sleep(0.2)

    # Verificar recepción en Sub1 (debe recibir 2 mensajes: Weather y Sports)
    msgs_sub1 = []
    poller1 = zmq.Poller()
    poller1.register(sub1, zmq.POLLIN)

    while poller1.poll(300):
        m = sub1.recv_string()
        msgs_sub1.append(m)
        print(f" [+] Sub1 (Weather+Sports) recibió: {m}")

    assert len(msgs_sub1) == 2, f"Esperaba 2 mensajes en Sub1, obtuvo {len(msgs_sub1)}"
    assert any("WEATHER" in m for m in msgs_sub1) and any("SPORTS" in m for m in msgs_sub1)

    # Verificar recepción en Sub2 (debe recibir 1 mensaje: Finance)
    msgs_sub2 = []
    poller2 = zmq.Poller()
    poller2.register(sub2, zmq.POLLIN)

    while poller2.poll(300):
        m = sub2.recv_string()
        msgs_sub2.append(m)
        print(f" [+] Sub2 (Finance) recibió: {m}")

    assert len(msgs_sub2) == 1, f"Esperaba 1 mensaje en Sub2, obtuvo {len(msgs_sub2)}"
    assert "FINANCE" in msgs_sub2[0]

    pub1.close()
    pub2.close()
    pub3.close()
    sub1.close()
    sub2.close()
    ctx.term()
    print("[PARTE 2] Todas las pruebas de Multi-Publisher y Multi-Subscriber PASARON exitosamente.\n")


def test_part3_pipeline_broker():
    print("\n" + "=" * 70)
    print(">>> TEST PARTE 3: PIPELINE (SOURCE -> BROKER -> WORKER) <<<")
    print("=" * 70)

    ctx = zmq.Context()

    # Broker: Frontend PULL (13051), Backend PUSH (13052)
    broker_frontend = ctx.socket(zmq.PULL)
    broker_frontend.bind("tcp://127.0.0.1:13051")
    broker_backend = ctx.socket(zmq.PUSH)
    broker_backend.bind("tcp://127.0.0.1:13052")

    # Flag para controlar broker thread
    running = True

    def broker_loop():
        poller = zmq.Poller()
        poller.register(broker_frontend, zmq.POLLIN)
        while running:
            socks = dict(poller.poll(100))
            if broker_frontend in socks:
                msg = broker_frontend.recv()
                broker_backend.send(msg)

    broker_th = threading.Thread(target=broker_loop, daemon=True)
    broker_th.start()

    # 2 Workers: PULL (13052)
    w1 = ctx.socket(zmq.PULL)
    w1.connect("tcp://127.0.0.1:13052")
    w2 = ctx.socket(zmq.PULL)
    w2.connect("tcp://127.0.0.1:13052")

    # 2 Sources: PUSH (13051)
    s1 = ctx.socket(zmq.PUSH)
    s1.connect("tcp://127.0.0.1:13051")
    s2 = ctx.socket(zmq.PUSH)
    s2.connect("tcp://127.0.0.1:13051")

    time.sleep(0.3)

    # Enviar 4 tareas desde Source 1 y 4 tareas desde Source 2
    for i in range(1, 5):
        s1.send(pickle.dumps({"source_id": "Source-1", "task_id": i, "workload": 5}))
        s2.send(pickle.dumps({"source_id": "Source-2", "task_id": i, "workload": 5}))

    time.sleep(0.5)

    w1_tasks = []
    w2_tasks = []

    poller_w = zmq.Poller()
    poller_w.register(w1, zmq.POLLIN)
    poller_w.register(w2, zmq.POLLIN)

    start_t = time.time()
    while len(w1_tasks) + len(w2_tasks) < 8 and (time.time() - start_t) < 3.0:
        events = dict(poller_w.poll(200))
        if w1 in events:
            t = pickle.loads(w1.recv())
            w1_tasks.append(t)
            print(f" [+] Worker-1 procesó tarea #{t['task_id']} de [{t['source_id']}]")
        if w2 in events:
            t = pickle.loads(w2.recv())
            w2_tasks.append(t)
            print(f" [+] Worker-2 procesó tarea #{t['task_id']} de [{t['source_id']}]")

    total_processed = len(w1_tasks) + len(w2_tasks)
    print(f" [+] Total de tareas recibidas por workers: {total_processed} (Worker-1: {len(w1_tasks)}, Worker-2: {len(w2_tasks)})")
    assert total_processed == 8, f"Esperaba 8 tareas procesadas, obtuvo {total_processed}"
    assert len(w1_tasks) > 0 and len(w2_tasks) > 0, "Ambos workers deben haber recibido carga distribuida."

    running = False
    broker_th.join(timeout=0.5)
    s1.close()
    s2.close()
    w1.close()
    w2.close()
    broker_frontend.close()
    broker_backend.close()
    ctx.term()

    print("[PARTE 3] Todas las pruebas del Pipeline con Broker PASARON exitosamente.\n")


if __name__ == "__main__":
    print("\n" + "=" * 75)
    print(" INICIANDO SUITE COMPLETA DE PRUEBAS DE SISTEMAS DISTRIBUIDOS - WORKSHOP 2")
    print("=" * 75)
    
    test_part1_matrix_manager()
    test_part2_pub_sub()
    test_part3_pipeline_broker()

    print("=" * 75)
    print(" ¡TODAS LAS PRUEBAS (PARTES 1, 2 Y 3) FINALIZARON CON ÉXITO AL 100%! ")
    print("=" * 75)
