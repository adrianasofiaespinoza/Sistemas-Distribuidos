# Parte 2: Multi-Publisher y Multi-Subscriber (ZeroMQ PUB-SUB)

Esta solución implementa una arquitectura **Publisher-Subscriber** distribuida utilizando la biblioteca **PyZMQ (ZeroMQ)**. Soporta múltiples publicadores ofreciendo diferentes servicios/tópicos independientes y múltiples suscriptores capaces de suscribirse a uno o más publicadores y filtrar tópicos específicos.

---

## Archivos
- `pub_weather.py`: Publicador del servicio de Clima (puerto `15001`, tópico `WEATHER`).
- `pub_finance.py`: Publicador del servicio Financiero (puerto `15002`, tópico `FINANCE`).
- `pub_sports.py`: Publicador del servicio Deportivo (puerto `15003`, tópico `SPORTS`).
- `publisher_service.py`: Publicador genérico y configurable por línea de comandos.
- `subscriber_multi.py`: Suscriptor que se conecta a múltiples endpoints y filtra por uno o varios tópicos.

---

## Cómo ejecutar

### Escenario demostrativo: 3 Publishers y 2 Suscriptores con diferentes intereses

#### 1. Iniciar los Publishers (en terminales separadas o máquinas distintas):
```bash
# Terminal 1 (Servicio de Clima)
python pub_weather.py

# Terminal 2 (Servicio Financiero)
python pub_finance.py

# Terminal 3 (Servicio de Deportes)
python pub_sports.py
```

#### 2. Iniciar los Suscriptores:

- **Suscriptor A (Interesado solo en Clima y Deportes):**
  ```bash
  python subscriber_multi.py --name "Sub-Clima-Deportes" --endpoints tcp://localhost:15001 tcp://localhost:15003 --topics WEATHER SPORTS
  ```

- **Suscriptor B (Interesado solo en Finanzas):**
  ```bash
  python subscriber_multi.py --name "Sub-Trader" --endpoints tcp://localhost:15002 --topics FINANCE
  ```

- **Suscriptor C (Suscrito a todos los servicios y tópicos):**
  ```bash
  python subscriber_multi.py --name "Sub-General" --endpoints tcp://localhost:15001 tcp://localhost:15002 tcp://localhost:15003 --topics ALL
  ```

---

### Ejecución en diferentes máquinas de la red

1. En la máquina donde corren los publishers (ej: IP `192.168.1.100`), los sockets se enlazan con `*` (todas las interfaces).
2. En las máquinas suscriptoras, reemplazar `localhost` por la IP del publisher:
   ```bash
   python subscriber_multi.py --name "Sub-Remoto" --endpoints tcp://192.168.1.100:15001 tcp://192.168.1.100:15002 --topics WEATHER FINANCE
   ```
