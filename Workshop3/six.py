from dataclasses import dataclass


@dataclass
class File:
    inode: int
    content: str


# Simulated filesystem
files = {
    1001: File(1001, "Distributed Systems")
}

# Namespace: name -> inode
hard_namespace = {
    "data/original.txt": 1001,
    "hardlink.txt": 1001
}

# Soft links: name -> target name
soft_links = {
    "softlink.txt": "data/original.txt"
}


def read_path(path):
    """
    Resolve a path in the simulated filesystem.
    """

    # Direct/hard-link lookup
    if path in hard_namespace:
        inode = hard_namespace[path]
        return files[inode].content

    # Symbolic-link lookup
    if path in soft_links:
        target = soft_links[path]

        if target not in hard_namespace:
            raise FileNotFoundError(
                f"Broken symbolic link: {path} -> {target}"
            )

        inode = hard_namespace[target]
        return files[inode].content

    raise FileNotFoundError(f"File not found: {path}")


def show_filesystem():
    print("\n=== Namespace ===")

    for path, inode in hard_namespace.items():
        print(f"{path} -> inode {inode}")

    for path, target in soft_links.items():
        print(f"{path} -> '{target}'")


def rename_original():
    """
    Simulates:
        mv data/original.txt data/renamed.txt
    """

    inode = hard_namespace["data/original.txt"]

    del hard_namespace["data/original.txt"]

    hard_namespace["data/renamed.txt"] = inode


def delete_renamed():
    """
    Simulates:
        rm data/renamed.txt
    """

    del hard_namespace["data/renamed.txt"]


print("=== INITIAL STATE ===")

show_filesystem()

print("\nReading hardlink:")
print(read_path("hardlink.txt"))

print("\nReading softlink:")
print(read_path("softlink.txt"))


print("\n=== RENAME ORIGINAL ===")

rename_original()

show_filesystem()

print("\nReading hardlink after rename:")
print(read_path("hardlink.txt"))

print("\nReading softlink after rename:")

try:
    print(read_path("softlink.txt"))
except FileNotFoundError as e:
    print("ERROR:", e)


print("\n=== DELETE RENAMED FILE ===")

delete_renamed()

show_filesystem()

print("\nReading hardlink after deletion:")
print(read_path("hardlink.txt"))

print("\nReading softlink after deletion:")

try:
    print(read_path("softlink.txt"))
except FileNotFoundError as e:
    print("ERROR:", e)