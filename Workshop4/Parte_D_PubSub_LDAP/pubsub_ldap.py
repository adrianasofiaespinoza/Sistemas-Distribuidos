"""
Part D: Special Activity - Publisher-Subscriber with LDAP Service Registration & Discovery
Workshop 4 - Sistemas Distribuidos
"""

import zmq
import time
import random
import threading
import json
from ldap3 import Server, Connection, MOCK_SYNC, ALL, ALL_ATTRIBUTES

class LDAPServiceRegistry:
    def __init__(self):
        self.server = Server('ldap://localhost:389', get_info=ALL)
        self.conn = Connection(
            self.server,
            user='cn=admin,dc=example,dc=com',
            password='adminpassword',
            client_strategy=MOCK_SYNC
        )
        self.conn.bind()
        
        # Base setup
        self.conn.strategy.add_entry(
            'dc=example,dc=com',
            {'objectClass': ['top', 'organization'], 'o': 'Example Inc.', 'dc': 'example'}
        )
        self.conn.strategy.add_entry(
            'ou=Services,dc=example,dc=com',
            {'objectClass': ['top', 'organizationalUnit'], 'ou': 'Services'}
        )
        self.lock = threading.Lock()

    def register_service(self, service_name, ip, port, description="ZeroMQ Publisher Service"):
        dn = f"cn={service_name.upper()},ou=Services,dc=example,dc=com"
        attrs = {
            'objectClass': ['top', 'device', 'ipHost'],
            'cn': service_name.upper(),
            'ipHostNumber': str(ip),
            'ipServicePort': str(port),
            'description': description
        }
        with self.lock:
            # Add or update entry in LDAP
            if dn in self.conn.strategy.entries:
                del self.conn.strategy.entries[dn]
            self.conn.strategy.add_entry(dn, attrs)
            print(f"[LDAP REGISTRY] Registered service '{service_name.upper()}' -> Host: {ip}, Port: {port}")

    def lookup_service(self, service_name):
        with self.lock:
            search_ok = self.conn.search(
                search_base='ou=Services,dc=example,dc=com',
                search_filter=f'(cn={service_name.upper()})',
                attributes=['ipHostNumber', 'ipServicePort', 'description']
            )
            if search_ok and self.conn.entries:
                entry = self.conn.entries[0]
                ip = entry.ipHostNumber[0]
                port = entry.ipServicePort[0]
                desc = entry.description[0] if entry.description else ""
                print(f"[LDAP DISCOVERY] Resolved service '{service_name.upper()}' from LDAP -> {ip}:{port}")
                return ip, int(port), desc
            else:
                print(f"[LDAP DISCOVERY FAILED] Service '{service_name.upper()}' not found in LDAP directory.")
                return None, None, None


def run_publisher(service_name, port, registry, stop_event, logs):
    host = "127.0.0.1"
    registry.register_service(service_name, host, port, f"Publisher for {service_name}")
    
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://{host}:{port}")
    
    msg_count = 0
    time.sleep(0.2)
    
    topics_data = {
        "WEATHER": [("Quito", "18.5C, Lluvia"), ("Guayaquil", "28.0C, Soleado"), ("Cuenca", "15.2C, Nublado")],
        "FINANCE": [("USD/EUR", "0.92"), ("BTC/USD", "64500.0"), ("AAPL", "225.50")],
        "SPORTS": [("LigaPro", "LDU 2 - 1 BSC"), ("Champions", "Real Madrid 3 - 1 Bayern"), ("Premier", "Arsenal 1 - 0 City")]
    }

    data_list = topics_data.get(service_name.upper(), [("GENERIC", "Info")])

    while not stop_event.is_set():
        time.sleep(1.0)
        msg_count += 1
        item, val = random.choice(data_list)
        msg = f"{service_name.upper()} [{time.strftime('%H:%M:%S')}] #{msg_count} {item}: {val}"
        socket.send_string(msg)
        log_entry = f"[PUB-{service_name.upper()}] Sent: {msg}"
        logs.append(log_entry)
        print(log_entry)

    socket.close()
    context.term()
    print(f"[PUB-{service_name.upper()}] Stopped.")


def run_subscriber(sub_name, target_services, registry, stop_event, logs, received_msgs):
    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    
    print(f"\n--- [{sub_name}] QUERYING LDAP DIRECTORY FOR SERVICES: {target_services} ---")
    
    connected_endpoints = []
    for srv in target_services:
        ip, port, _ = registry.lookup_service(srv)
        if ip and port:
            endpoint = f"tcp://{ip}:{port}"
            sub_socket.connect(endpoint)
            connected_endpoints.append(endpoint)
            sub_socket.setsockopt_string(zmq.SUBSCRIBE, srv.upper())
            print(f"[{sub_name}] Subscribed to topic '{srv.upper()}' at {endpoint}")

    print(f"[{sub_name}] Listening for messages on endpoints: {connected_endpoints}\n")

    poller = zmq.Poller()
    poller.register(sub_socket, zmq.POLLIN)

    while not stop_event.is_set():
        socks = dict(poller.poll(500)) # poll timeout 500ms
        if sub_socket in socks and socks[sub_socket] == zmq.POLLIN:
            raw_msg = sub_socket.recv_string()
            log_entry = f"[{sub_name} RECIBIDO] {raw_msg}"
            logs.append(log_entry)
            received_msgs.append(raw_msg)
            print(log_entry)

    sub_socket.close()
    context.term()
    print(f"[{sub_name}] Stopped.")


def main():
    print("==========================================================")
    print(" PART D: SPECIAL ACTIVITY - PUB/SUB WITH LDAP DISCOVERY")
    print("==========================================================")

    registry = LDAPServiceRegistry()
    stop_event = threading.Event()
    logs = []
    received_msgs = []

    # Start Publishers
    pub_threads = []
    publishers_config = [
        ("WEATHER", 15001),
        ("FINANCE", 15002),
        ("SPORTS", 15003)
    ]

    print("\n1. Starting Publishers & Registering Services in LDAP...")
    for srv_name, port in publishers_config:
        t = threading.Thread(target=run_publisher, args=(srv_name, port, registry, stop_event, logs))
        t.start()
        pub_threads.append(t)

    time.sleep(1.0) # Wait for publishers to register and start

    # Start Subscriber querying LDAP
    print("\n2. Starting Subscriber with LDAP Dynamic Discovery...")
    sub_services = ["WEATHER", "FINANCE", "SPORTS"]
    sub_thread = threading.Thread(
        target=run_subscriber,
        args=("Subscriber-LDAP-Client", sub_services, registry, stop_event, logs, received_msgs)
    )
    sub_thread.start()

    # Let the system run for 6 seconds to demonstrate pub/sub over LDAP discovery
    time.sleep(6.0)

    print("\n3. Stopping Pub/Sub System...")
    stop_event.set()
    
    for t in pub_threads:
        t.join()
    sub_thread.join()

    print(f"\nSystem Execution Completed! Total Messages Received by Subscriber: {len(received_msgs)}")

    output_data = {
        "publishers": publishers_config,
        "subscribed_services": sub_services,
        "total_received": len(received_msgs),
        "received_messages": received_msgs,
        "logs": logs
    }

    with open(r"c:\Users\User\Desktop\8vo\Sistemas-Distribuidos\Sistemas-Distribuidos\Workshop4\pubsub_ldap_results.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print("Saved Pub/Sub LDAP execution results to pubsub_ldap_results.json")


if __name__ == "__main__":
    main()
