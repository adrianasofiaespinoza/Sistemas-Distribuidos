# Parte 3: Pipeline con Broker Intermediario (Source -> Broker -> Worker)

Esta solución implementa un patrón **Pipeline / Ventilador-Colector con Broker intermediario** utilizando **PyZMQ (ZeroMQ)**. El sistema cuenta con:
1. **Entrada única en el Broker (Frontend PULL):** Capaz de recibir tareas de múltiples fuentes generadoras (`Sources`).
2. **Salida única en el Broker (Backend PUSH):** Capaz de distribuir y balancear la carga de trabajo entre múltiples trabajadores (`Workers`).

---

## Archivos
- `broker.py`: Intermediario central que enlaza la entrada de tareas (puerto `13001`) y la salida hacia los workers (puerto `13002`).
- `source_pipeline.py`: Generador de tareas (PUSH) que se conecta al frontend del broker.
- `worker_pipeline.py`: Consumidor de tareas (PULL) que se conecta al backend del broker y procesa el trabajo.

---

## Cómo ejecutar

### Escenario demostrativo: 1 Broker, 2 Sources y 3 Workers

#### 1. Iniciar el Broker:
```bash
python broker.py --frontend-port 13001 --backend-port 13002
```

#### 2. Iniciar Múltiples Workers (en terminales separadas):
```bash
# Terminal Worker 1
python worker_pipeline.py --id "Worker-Alpha"

# Terminal Worker 2
python worker_pipeline.py --id "Worker-Beta"

# Terminal Worker 3
python worker_pipeline.py --id "Worker-Gamma"
```

#### 3. Iniciar Múltiples Sources (en terminales separadas):
```bash
# Terminal Source 1 (Envía 15 tareas)
python source_pipeline.py --id "Sensor-Camara" --tasks 15 --delay 0.4

# Terminal Source 2 (Envía 15 tareas)
python source_pipeline.py --id "Sensor-Radar" --tasks 15 --delay 0.3
```

---

### Observación del Comportamiento Distribuido
- El **Broker** recibe intercaladamente las tareas de `Sensor-Camara` y `Sensor-Radar`.
- El **Broker** distribuye automáticamente las tareas entre `Worker-Alpha`, `Worker-Beta` y `Worker-Gamma` siguiendo un esquema de balanceo equitativo (*Fair Queueing / Round Robin*).
