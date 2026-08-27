# Parte 1: Distributed Matrix Manager (RMI / XML-RPC)

Esta aplicación implementa un gestor distribuido de matrices mediante **RMI (Remote Method Invocation / XML-RPC)** en Python. El cliente lee o genera matrices y solicita operaciones (suma, resta, producto matricial, transpuesta, determinante), y el servidor realiza el cómputo distribuido utilizando la biblioteca **NumPy** y retorna el resultado.

---

## Archivos
- `server_matrix.py`: Servidor XML-RPC que expone métodos para operaciones matriciales con NumPy (`add`, `sub`, `prod`, `transpose`, `det`).
- `client_matrix.py`: Cliente interactivo y automatizado que se comunica con el servidor.

---

## Cómo ejecutar

### 1. Ejecución en la misma máquina (Localhost)

**Terminal 1 (Servidor):**
```bash
python server_matrix.py localhost 12000
```
*(o simplemente `python server_matrix.py` y presionar Enter para valores por defecto)*

**Terminal 2 (Cliente interactivo):**
```bash
python client_matrix.py localhost 12000
```

**Terminal 2 (Modo Demo rápido):**
```bash
python client_matrix.py localhost 12000 --demo
```

---

### 2. Ejecución en dos máquinas diferentes

1. **En la Máquina Servidor (IP por ejemplo: `192.168.1.50`):**
   ```bash
   python server_matrix.py 0.0.0.0 12000
   ```
   *(Escuchará en todas las interfaces de red de la máquina)*

2. **En la Máquina Cliente:**
   ```bash
   python client_matrix.py 192.168.1.50 12000
   ```
