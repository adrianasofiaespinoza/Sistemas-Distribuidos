import sys

# Ensure UTF-8 output even on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

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
        # Si el nodo actual ya es el sucesor o si la clave le pertenece
        if current == successor(key):
            break

        fingers = finger_table(current)
        candidates = []

        for i, start, target in fingers:
            if target == current:
                continue

            # Distancia circular
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


if __name__ == "__main__":
    print("=== Part A - Chord definition ===")
    test_keys = [3, 8, 12, 19, 26, 30]
    for key in test_keys:
        print(f"Key: {key} -> node: {successor(key)}")

    print("\n=== Part B - Finger tables ===")
    print("Node 1 Finger Table:")
    print("i\tstart\tsuccessor")
    for i, start, target in finger_table(1):
        print(f"{i}\t{start}\t{target}")

    print("\nFinger tables for all nodes:")
    for n in nodes:
        ft_targets = [target for _, _, target in finger_table(n)]
        print(f"Node {n:2d}: FT = {ft_targets}")

    print("\n=== Part C - Lookup ===")
    print("Lookup key 26 starting at 1")
    path26 = lookup(1, 26)
    for idx, node in enumerate(path26):
        if idx == 0:
            print(node)
        else:
            print("->", node)
    print("Total hops =", len(path26) - 1)

    print("\nLookup key 12 starting at 28")
    path12 = lookup(28, 12)
    for idx, node in enumerate(path12):
        if idx == 0:
            print(node)
        else:
            print("->", node)
    print("Total hops =", len(path12) - 1)
