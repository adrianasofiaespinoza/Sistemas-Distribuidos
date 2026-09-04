
M = 5
RING_SIZE = 2 ** M

nodes = [1, 4, 9, 11, 14, 18, 20, 21, 28]


def successor(key):
    key %= RING_SIZE

    for node in nodes:
        if node >= key:
            return node

    return nodes[0]


def finger_table(node):
    table = []

    for i in range(M):
        start = (node + 2**i) % RING_SIZE
        target = successor(start)
        table.append((i + 1, start, target))

    return table


def lookup(start_node, key):
    current = start_node
    path = [current]

    while True:

        # Ya encontramos al sucesor
        if current == successor(key):
            break

        fingers = finger_table(current)

        # Buscar la finger más cercana a key sin pasarnos
        candidates = []

        for i, start, target in fingers:
            if target == current:
                continue

            # Consideramos el recorrido circular
            distance_to_target = (target - current) % RING_SIZE
            distance_to_key = (key - current) % RING_SIZE

            if 0 < distance_to_target < distance_to_key:
                candidates.append(target)

        if candidates:
            next_node = candidates[-1]
        else:
            next_node = successor(key)

        current = next_node
        path.append(current)

    return path


# Lookup 26 starting at 1
print("Lookup key 26")

path = lookup(1, 26)

for i, node in enumerate(path):
    if i == 0:
        print(node)
    else:
        print("->", node)

print("Total hops =", len(path) - 1)


# Lookup 12 starting at 28
print("\nLookup key 12")

path = lookup(28, 12)

for i, node in enumerate(path):
    if i == 0:
        print(node)
    else:
        print("->", node)

print("Total hops =", len(path) - 1)