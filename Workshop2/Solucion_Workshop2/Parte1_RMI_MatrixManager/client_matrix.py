"""
Cliente RMI (XML-RPC) - Distributed Matrix Manager
Sistemas Distribuidos - Workshop 2 (Parte 1: Actividad 2)
"""

import xmlrpc.client
import numpy as np
import sys


def print_matrix(name, mat):
    """Imprime una matriz con formato legible."""
    arr = np.array(mat)
    print(f"\n--- {name} (dimensiones {arr.shape}) ---")
    for row in arr:
        print("  [ " + "\t".join(f"{val:8.2f}" if isinstance(val, (int, float)) else str(val) for val in row) + " ]")
    print()


def input_matrix_manually(name):
    """Lee una matriz desde el teclado fila por fila."""
    print(f"\n>> Ingreso manual para {name}:")
    try:
        rows = int(input(f"  Número de filas para {name}: "))
        cols = int(input(f"  Número de columnas para {name}: "))
    except ValueError:
        print("  Dimensiones inválidas. Usando 2x2 por defecto.")
        rows, cols = 2, 2

    mat = []
    print(f"  Ingrese los elementos de cada fila separados por espacio:")
    for r in range(rows):
        while True:
            try:
                line = input(f"    Fila {r + 1} ({cols} valores): ").strip()
                vals = [float(x) for x in line.split()]
                if len(vals) != cols:
                    print(f"    Error: Debe ingresar exactamente {cols} números. Intente de nuevo.")
                    continue
                mat.append(vals)
                break
            except ValueError:
                print("    Error: Ingrese números válidos. Intente de nuevo.")
    return mat


def generate_random_matrix(name, rows=None, cols=None, min_val=-10, max_val=10):
    """Genera una matriz aleatoria."""
    if rows is None or cols is None:
        try:
            print(f"\n>> Generación aleatoria para {name}:")
            rows = int(input(f"  Número de filas para {name}: "))
            cols = int(input(f"  Número de columnas para {name}: "))
        except ValueError:
            print("  Dimensiones inválidas. Usando 2x2 por defecto.")
            rows, cols = 2, 2

    mat = np.random.randint(min_val, max_val + 1, size=(rows, cols)).tolist()
    return mat


def interactive_menu(proxy):
    """Menú interactivo para ejecutar operaciones sobre matrices."""
    while True:
        print("=" * 60)
        print(" DISTRIBUTED MATRIX MANAGER - CLIENTE RMI")
        print("=" * 60)
        print("1. Sumar dos matrices (A + B)")
        print("2. Restar dos matrices (A - B)")
        print("3. Multiplicar dos matrices (A @ B)")
        print("4. Transpuesta de una matriz (A^T)")
        print("5. Determinante de una matriz cuadrada det(A)")
        print("6. Ejecutar prueba rápida demostrativa (Quick Demo)")
        print("0. Salir")
        print("-" * 60)

        op = input("Seleccione una opción: ").strip()

        if op == "0":
            print("Saliendo del cliente.")
            break

        if op == "6":
            run_quick_demo(proxy)
            continue

        if op in ["1", "2", "3"]:
            print("\n¿Cómo desea obtener las matrices A y B?")
            print("  [g] Generar aleatoriamente")
            print("  [m] Ingresar manualmente")
            modo = input("Opción (g/m, default 'g'): ").strip().lower()

            if op in ["1", "2"]:
                # Suma o resta: deben tener mismas dimensiones
                if modo == "m":
                    mat_a = input_matrix_manually("Matriz A")
                    mat_b = input_matrix_manually("Matriz B")
                else:
                    try:
                        r = int(input("Número de filas (ambas): ") or "3")
                        c = int(input("Número de columnas (ambas): ") or "3")
                    except ValueError:
                        r, c = 3, 3
                    mat_a = generate_random_matrix("Matriz A", r, c)
                    mat_b = generate_random_matrix("Matriz B", r, c)

                print_matrix("Matriz A", mat_a)
                print_matrix("Matriz B", mat_b)

                if op == "1":
                    res = proxy.add(mat_a, mat_b)
                    if res.get("status") == "OK":
                        print_matrix("RESULTADO: A + B", res["result"])
                    else:
                        print("Error retornado por servidor:", res.get("message"))
                else:
                    res = proxy.sub(mat_a, mat_b)
                    if res.get("status") == "OK":
                        print_matrix("RESULTADO: A - B", res["result"])
                    else:
                        print("Error retornado por servidor:", res.get("message"))

            elif op == "3":
                # Multiplicación: A (n x k) y B (k x m)
                if modo == "m":
                    mat_a = input_matrix_manually("Matriz A")
                    mat_b = input_matrix_manually("Matriz B")
                else:
                    try:
                        n = int(input("Filas de A (n): ") or "2")
                        k = int(input("Columnas de A / Filas de B (k): ") or "3")
                        m = int(input("Columnas de B (m): ") or "2")
                    except ValueError:
                        n, k, m = 2, 3, 2
                    mat_a = generate_random_matrix("Matriz A", n, k)
                    mat_b = generate_random_matrix("Matriz B", k, m)

                print_matrix("Matriz A", mat_a)
                print_matrix("Matriz B", mat_b)

                res = proxy.prod(mat_a, mat_b)
                if res.get("status") == "OK":
                    print_matrix("RESULTADO: A @ B", res["result"])
                else:
                    print("Error retornado por servidor:", res.get("message"))

        elif op in ["4", "5"]:
            print("\n¿Cómo desea obtener la matriz A?")
            print("  [g] Generar aleatoriamente")
            print("  [m] Ingresar manualmente")
            modo = input("Opción (g/m, default 'g'): ").strip().lower()

            if op == "4":
                if modo == "m":
                    mat_a = input_matrix_manually("Matriz A")
                else:
                    try:
                        r = int(input("Filas: ") or "2")
                        c = int(input("Columnas: ") or "3")
                    except ValueError:
                        r, c = 2, 3
                    mat_a = generate_random_matrix("Matriz A", r, c)

                print_matrix("Matriz A", mat_a)
                res = proxy.transpose(mat_a)
                if res.get("status") == "OK":
                    print_matrix("RESULTADO: Transpuesta A^T", res["result"])
                else:
                    print("Error retornado por servidor:", res.get("message"))

            elif op == "5":
                if modo == "m":
                    mat_a = input_matrix_manually("Matriz A (cuadrada)")
                else:
                    try:
                        n = int(input("Dimensión de matriz cuadrada n: ") or "3")
                    except ValueError:
                        n = 3
                    mat_a = generate_random_matrix("Matriz A", n, n)

                print_matrix("Matriz A", mat_a)
                res = proxy.det(mat_a)
                if res.get("status") == "OK":
                    print(f"\n>> RESULTADO: det(A) = {res['result']:.4f}\n")
                else:
                    print("Error retornado por servidor:", res.get("message"))

        input("Presione ENTER para continuar...")


def run_quick_demo(proxy):
    """Ejecuta una prueba automática de todas las operaciones disponibles."""
    print("\n" + "=" * 50)
    print(">>> EJECUTANDO QUICK DEMO AUTOMÁTICO <<<")
    print("=" * 50)

    # 1. Suma
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[7, 8, 9], [1, 2, 3]]
    print_matrix("A (Suma)", a)
    print_matrix("B (Suma)", b)
    res_add = proxy.add(a, b)
    print_matrix("Resultado A + B:", res_add["result"])

    # 2. Resta
    res_sub = proxy.sub(a, b)
    print_matrix("Resultado A - B:", res_sub["result"])

    # 3. Producto
    c = [[1, 2, 3], [4, 5, 6]] # 2x3
    d = [[7, 8], [9, 1], [2, 3]] # 3x2
    print_matrix("C (2x3)", c)
    print_matrix("D (3x2)", d)
    res_prod = proxy.prod(c, d)
    print_matrix("Resultado C @ D (2x2):", res_prod["result"])

    # 4. Transpuesta
    res_trans = proxy.transpose(c)
    print_matrix("Resultado C^T (3x2):", res_trans["result"])

    # 5. Determinante
    sq = [[4, 7], [2, 6]]
    print_matrix("Matriz Cuadrada (2x2)", sq)
    res_det = proxy.det(sq)
    print(f"Resultado det: {res_det['result']}\n")
    print(">>> DEMO COMPLETADO CON ÉXITO <<<\n")


def main():
    serverName = sys.argv[1] if len(sys.argv) > 1 else None
    serverPort = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if not serverName:
        serverName = input("Enter server hostname or IP address (default 'localhost'): ").strip()
        if not serverName:
            serverName = "localhost"

    if not serverPort:
        try:
            port_in = input("Enter server port number (default 12000): ").strip()
            serverPort = int(port_in) if port_in else 12000
        except ValueError:
            print("Entrada inválida. Usando puerto por defecto 12000.")
            serverPort = 12000

    if serverPort <= 0 or serverPort > 65535:
        serverPort = 12000

    endpoint = f"http://{serverName}:{serverPort}/RPC2"
    print(f"\nConectando al servidor RMI en {endpoint} ...")
    
    proxy = xmlrpc.client.ServerProxy(endpoint, allow_none=True)

    # Si se pasó argumento --demo o -d en argv
    if len(sys.argv) > 3 and sys.argv[3] in ["--demo", "-d"]:
        run_quick_demo(proxy)
        return

    interactive_menu(proxy)


if __name__ == "__main__":
    main()
