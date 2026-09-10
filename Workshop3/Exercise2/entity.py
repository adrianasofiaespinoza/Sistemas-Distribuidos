import socket

ENTITY_ID = "studentA-Name"
PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(("", PORT))

print(f"Entity waiting for location requests on UDP port {PORT}...", flush=True)

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()
    print(f"Request from {addr[0]}:{addr[1]} -> {message}", flush=True)

    if message == ENTITY_ID:
        response = f"{ENTITY_ID}:{socket.gethostbyname(socket.gethostname())}"
        sock.sendto(response.encode(), addr)
        print(f"Response sent -> {response}", flush=True)
