import zmq
import threading
import time

hostname = "localhost"
port = "5000"

def utc_time_client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)  # Socket de peticion
    socket.setsockopt(zmq.RCVTIMEO, 5000)  # Timeout de 5 segundos
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect("tcp://" + hostname + ":" + port)

    try:
        socket.send_string("Time request")
        utc_time = socket.recv().decode('utf-8')
        print(f"Hora UTC recibida: {utc_time}")
    except zmq.Again:
        print("Error: no se recibio respuesta del servidor")
    except zmq.ZMQError as e:
        print(f"Error de conexion: {e}")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    threads = []
    for i in range(3):
        # target=utc_time_client sin parentesis para que no se ejecute al momento
        t = threading.Thread(target=utc_time_client, args=())
        threads.append(t)
        t.start()
        time.sleep(2)
        t.join()
    print('Done')
