import zmq
import time
import sys

port = "5000"

def utc_time_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # Socket de respuesta
    socket.bind("tcp://*:" + port)

    print("Servidor UTC corriendo...")

    try:
        while True:
            if socket.poll(timeout=1000):
                message = socket.recv()
                print(f"Peticion recibida: {message.decode()}")

                # Obtener hora UTC
                utc_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                socket.send_string(utc_time)
                print(f"Hora UTC enviada: {utc_time}")
    except KeyboardInterrupt:
        print("Servidor detenido")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    utc_time_server()
