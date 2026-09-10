locations = {
    "A": "B",
    "B": "C",
    "C": "D",
    "D": "192.168.1.50:5000"
}


def resolve(location):
    hops = 0

    while location in locations:
        print("Following:", location, "->", locations[location])

        location = locations[location]
        hops += 1

    return location, hops


print("=== Initial chain resolution ===")
address, hops = resolve("A")

print("Final address:", address)
print("Number of hops:", hops)

locations["A"] = address

print("\n=== After shortcut optimization ===")

address, hops = resolve("A")

print("Final address:", address)
print("Number of hops:", hops)

del locations["C"]

print("\n=== Simulating failure: del locations['C'] ===")
print("1. Running resolution via shortcut (from A):")
address, hops = resolve("A")
print("Final address:", address)
print("Number of hops:", hops)

print("\n2. Running original chain again (restoring A -> B):")
locations["A"] = "B"
address, hops = resolve("A")
print("Final address:", address)
print("Number of hops:", hops)
if address != "192.168.1.50:5000":
    print("Observation: Chain broken at missing node C! Target unreached.")

