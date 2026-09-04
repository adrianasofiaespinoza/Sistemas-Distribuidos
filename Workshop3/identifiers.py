import uuid
import socket

# Unique entity identifier.
entity_id = uuid.uuid5(uuid.NAMESPACE_DNS, "student-a")

hostname = socket.gethostname()

ip = socket.gethostbyname(hostname)

print("Entity ID :", entity_id)
print("Hostname  :", hostname)
print("Address   :", ip)

entity = {
    "id": str(entity_id),
    "address": (ip, 5000)
}

print("Initial entity state:", entity)

entity["address"] = (ip, 6000)

print("Updated entity state:", entity)
