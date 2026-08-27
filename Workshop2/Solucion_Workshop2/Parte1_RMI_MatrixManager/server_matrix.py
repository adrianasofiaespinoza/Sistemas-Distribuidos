"""
Servidor RMI (XML-RPC) - Distributed Matrix Manager
Sistemas Distribuidos - Workshop 2 (Parte 1: Actividad 2)
"""

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import numpy as np
import sys

# Restricción al path RPC2
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class MatrixManager:
    """Clase que implementa las operaciones sobre matrices usando NumPy."""

    def add(self, matrix_a, matrix_b):
        """Suma de dos matrices: A + B"""
        try:
            arr_a = np.array(matrix_a, dtype=float)
            arr_b = np.array(matrix_b, dtype=float)
            print(f"[SERVIDOR] Operación SUMA solicitada.")
            print(f" Matriz A (forma {arr_a.shape}):\n{arr_a}")
            print(f" Matriz B (forma {arr_b.shape}):\n{arr_b}")
            
            result = np.add(arr_a, arr_b)
            print(f" Resultado SUMA:\n{result}\n")
            return {
                "status": "OK",
                "operation": "add",
                "result": result.tolist(),
                "shape": list(result.shape)
            }
        except Exception as e:
            print(f"[ERROR SUMA]: {e}")
            return {"status": "ERROR", "message": str(e)}

    def sub(self, matrix_a, matrix_b):
        """Resta de dos matrices: A - B"""
        try:
            arr_a = np.array(matrix_a, dtype=float)
            arr_b = np.array(matrix_b, dtype=float)
            print(f"[SERVIDOR] Operación RESTA solicitada.")
            print(f" Matriz A (forma {arr_a.shape}):\n{arr_a}")
            print(f" Matriz B (forma {arr_b.shape}):\n{arr_b}")
            
            result = np.subtract(arr_a, arr_b)
            print(f" Resultado RESTA:\n{result}\n")
            return {
                "status": "OK",
                "operation": "sub",
                "result": result.tolist(),
                "shape": list(result.shape)
            }
        except Exception as e:
            print(f"[ERROR RESTA]: {e}")
            return {"status": "ERROR", "message": str(e)}

    def prod(self, matrix_a, matrix_b):
        """Multiplicación de dos matrices (Producto matricial dot/matmul): A @ B"""
        try:
            arr_a = np.array(matrix_a, dtype=float)
            arr_b = np.array(matrix_b, dtype=float)
            print(f"[SERVIDOR] Operación PRODUCTO solicitada.")
            print(f" Matriz A (forma {arr_a.shape}):\n{arr_a}")
            print(f" Matriz B (forma {arr_b.shape}):\n{arr_b}")
            
            result = np.matmul(arr_a, arr_b)
            print(f" Resultado PRODUCTO:\n{result}\n")
            return {
                "status": "OK",
                "operation": "prod",
                "result": result.tolist(),
                "shape": list(result.shape)
            }
        except Exception as e:
            print(f"[ERROR PRODUCTO]: {e}")
            return {"status": "ERROR", "message": str(e)}

    def transpose(self, matrix_a):
        """Transpuesta de una matriz: A^T"""
        try:
            arr_a = np.array(matrix_a, dtype=float)
            result = arr_a.T
            print(f"[SERVIDOR] Operación TRANSPUESTA:\n{result}\n")
            return {
                "status": "OK",
                "operation": "transpose",
                "result": result.tolist(),
                "shape": list(result.shape)
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def det(self, matrix_a):
        """Determinante de una matriz cuadrada: det(A)"""
        try:
            arr_a = np.array(matrix_a, dtype=float)
            result = float(np.linalg.det(arr_a))
            print(f"[SERVIDOR] Operación DETERMINANTE: {result}\n")
            return {
                "status": "OK",
                "operation": "det",
                "result": result
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}


def start_server(host=None, port=None):
    if host is None:
        user_host = input("Enter server hostname or IP address (default '0.0.0.0'): ").strip()
        host = user_host if user_host else "0.0.0.0"
        
    if port is None:
        user_port = input("Enter server port number (default 12000): ").strip()
        try:
            port = int(user_port) if user_port else 12000
        except ValueError:
            print("Entrada inválida. Usando puerto por defecto 12000.")
            port = 12000

    if port <= 0 or port > 65535:
        port = 12000

    # Permitir enlace en 0.0.0.0 para aceptar conexiones de diferentes hosts
    with SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()
        
        # Registrar instancia del gestor de matrices
        matrix_manager = MatrixManager()
        server.register_instance(matrix_manager)
        
        print("=" * 60)
        print(" SERVIDOR RMI - DISTRIBUTED MATRIX MANAGER (NUMPY)")
        print("=" * 60)
        print(f"Servidor escuchando en {host}:{port} ...")
        print("Métodos disponibles: add, sub, prod, transpose, det")
        print("Presione Ctrl+C para detener el servidor.\n")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario.")


if __name__ == "__main__":
    cli_host = sys.argv[1] if len(sys.argv) > 1 else None
    cli_port = int(sys.argv[2]) if len(sys.argv) > 2 else None
    start_server(cli_host, cli_port)
