import sys

# Ensure UTF-8 output even on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Hierarchical Location Service Tree Structure
tree = {
    "ROOT": {
        "AMERICA": {
            "ECUADOR": {
                "IBARRA": {},
                "QUITO": {}
            },
            "USA": {}
        },
        "EUROPE": {}
    }
}

# Leaf entities database
entities = {
    "IBARRA": {
        "server01": "10.0.1.20"
    },
    "QUITO": {
        "server02": "10.0.2.30"
    }
}

# Downward pointers table for directory nodes: node -> {entity: child_domain}
downward_pointers = {
    "ROOT": {},
    "AMERICA": {},
    "EUROPE": {},
    "ECUADOR": {},
    "USA": {},
    "IBARRA": {},
    "QUITO": {}
}

# Helper to find parent of each node in the tree
parents = {}

def build_parents(node_dict, parent=None):
    for name, children in node_dict.items():
        parents[name] = parent
        build_parents(children, name)

build_parents(tree)

def register_entity(entity, domain, address):
    """Registers an entity at a leaf domain and updates downward pointers along the path to ROOT."""
    if domain not in entities:
        entities[domain] = {}
    entities[domain][entity] = address

    # Update downward pointers upward to ROOT
    curr = domain
    while parents.get(curr) is not None:
        p = parents[curr]
        if p not in downward_pointers:
            downward_pointers[p] = {}
        downward_pointers[p][entity] = curr
        curr = p

def unregister_entity(entity, domain):
    """Removes an entity from a leaf domain and cleans upward pointers."""
    if domain in entities and entity in entities[domain]:
        del entities[domain][entity]

    curr = domain
    while parents.get(curr) is not None:
        p = parents[curr]
        if p in downward_pointers and entity in downward_pointers[p]:
            if downward_pointers[p][entity] == curr:
                del downward_pointers[p][entity]
        curr = p

def move_entity(entity, from_domain, to_domain, new_address=None):
    """Moves an entity from one leaf domain to another and updates directory pointers."""
    old_addr = entities.get(from_domain, {}).get(entity)
    unregister_entity(entity, from_domain)
    addr = new_address if new_address is not None else old_addr
    register_entity(entity, to_domain, addr)

# Initialize downward pointers for starting entities
for dom, ents in entities.items():
    for ent, addr in ents.items():
        register_entity(ent, dom, addr)


def lookup(entity, starting_domain):
    """
    Performs hierarchical lookup:
    1. Search locally in starting leaf domain.
    2. Move upward until a node has a downward pointer to the subtree containing entity.
    3. Follow downward pointers to the target leaf node.
    """
    curr = starting_domain
    path = [curr]

    # Search locally or move upward
    found_downward = False
    while curr is not None:
        # Check local leaf entities
        if curr in entities and entity in entities[curr]:
            path.append(entity)
            for i, p in enumerate(path):
                if i == 0:
                    print(p)
                else:
                    print("->", p)
            return entities[curr][entity]

        # Check downward pointer at this directory node
        if curr in downward_pointers and entity in downward_pointers[curr]:
            found_downward = True
            break

        # Move upward
        parent = parents.get(curr)
        if parent is None:
            # Reached ROOT and not found
            break
        curr = parent
        path.append(curr)

    if not found_downward:
        for i, p in enumerate(path):
            if i == 0:
                print(p)
            else:
                print("->", p)
        print("Entity not found")
        return None

    # Follow downward pointers to the leaf
    while curr not in entities or entity not in entities[curr]:
        next_domain = downward_pointers[curr][entity]
        curr = next_domain
        path.append(curr)

    path.append(entity)

    for i, p in enumerate(path):
        if i == 0:
            print(p)
        else:
            print("->", p)

    return entities[curr][entity]


if __name__ == "__main__":
    print("=== Initial Lookups ===")
    print("Lookup server01 from IBARRA:")
    addr1 = lookup("server01", "IBARRA")
    print("Address:", addr1)

    print("\nLookup server02 from IBARRA:")
    addr2 = lookup("server02", "IBARRA")
    print("Address:", addr2)

    print("\nLookup server99 from IBARRA:")
    addr99 = lookup("server99", "IBARRA")
    print("Address:", addr99)

    print("\n=== Moving server01 from IBARRA to QUITO ===")
    move_entity("server01", "IBARRA", "QUITO", "10.0.2.25")
    print("server01 moved to QUITO (new address: 10.0.2.25)")

    print("\nLookup server01 from IBARRA after move:")
    addr1_moved = lookup("server01", "IBARRA")
    print("Address:", addr1_moved)