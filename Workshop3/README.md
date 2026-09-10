# Taller 3: Nombrado y Localización en Sistemas Distribuidos (Workshop 3: Naming)

**Universidad Yachay Tech**  
**Escuela de Ciencias Matemáticas y Computacionales**  
**Asignatura:** Sistemas Distribuidos  
**Docente:** Francisco Hidrobo, Ph.D.  
**Fecha:** 3 de Septiembre de 2026  
**Autores:** Dario Pomasqui & Adriana Sofia Espinoza Chicaiza  
**Repositorio GitHub:** [adrianasofiaespinoza/Sistemas-Distribuidos/Workshop3](https://github.com/adrianasofiaespinoza/Sistemas-Distribuidos/tree/main/Workshop3)

---

## 📋 Descripción General

Este taller aborda los conceptos fundamentales y paradigmas de **Nombrado (Naming)** y **Servicios de Localización (Location Services)** en Sistemas Distribuidos. Se analizan, implementan y evalúan mecanismos para mapear nombres simbólicos e identificadores independientes de la ubicación hacia direcciones de red concretas.

El proyecto abarca tanto **paradigmas planos (Flat Naming)** como **paradigmas estructurados/jerárquicos (Hierarchical/Structured Naming)**, cubriendo desde la resolución por broadcast en capa física/aplicación hasta Tablas Hash Distribuidas (Chord), punteros de reenvío, HLS (Hierarchical Location Services) y el sistema de nombres en inodos POSIX (enlaces rígidos vs. simbólicos).

---

## 📁 Estructura del Repositorio

```text
Workshop3/
├── Exercise1/
│   └── identifiers.py     # Ejercicio 1: Separación de Identificadores y Direcciones (UUID vs IP)
├── Exercise2/
│   ├── entity.py          # Ejercicio 2: Servidor UDP para respuesta a búsqueda por Broadcast
│   └── finder.py          # Ejercicio 2: Cliente UDP para descubrimiento por Broadcast
├── Exercise3/
│   └── forwarding.py      # Ejercicio 3: Punteros de reenvío, atajos y simulación de fallos
├── Exercise4/
│   ├── chord.py           # Ejercicio 4: Implementación completa del Anillo Chord (M=5) y lookups
│   └── finger.py          # Ejercicio 4: Script auxiliar de verificación de tablas finger y lookup
├── Exercise5/
│   └── hls.py             # Ejercicio 5: Servicio de Localización Jerárquico (HLS)
├── Exercise6/
│   └── six.py             # Ejercicio 6: Simulación de Inodos, Hard Links y Soft Links en POSIX
├── informe.pdf            # Informe técnico detallado en formato IEEE/LNCS
└── README.md              # Documentación técnica del taller y guía de ejecución
```

---

## 🛠️ Explicación Detallada de Soluciones por Ejercicio

### 🔹 Ejercicio 1: Identificadores vs. Direcciones (`Exercise1/identifiers.py`)

* **Objetivo:** Desacoplar la identidad de una entidad respecto a su ubicación física en la red y demostrar la invariancia del identificador ante reasignaciones de puerto/dirección.
* **Implementación:**
  * Se genera un **UUIDv5** determinista a partir de la cadena `"student-a"` en el espacio de nombres DNS (`uuid.uuid5(uuid.NAMESPACE_DNS, "student-a")`), resultando en la clave fija `fc1ce712-f56d-5831-be86-2b82ea445f5a`.
  * La dirección de red (IP y puerto) se obtiene dinámicamente mediante `socket.gethostbyname(socket.gethostname())`.
  * Se simula la migración de la entidad cambiando su puerto de escucha de `5000` a `6000`.
* **Resultado Obtenido:**
  ```text
  Entity ID : fc1ce712-f56d-5831-be86-2b82ea445f5a
  Hostname  : DESKTOP-MLJEOGD
  Address   : 192.168.1.14
  Initial entity state: {'id': 'fc1ce712-f56d-5831-be86-2b82ea445f5a', 'address': ('192.168.1.14', 5000)}
  Updated entity state: {'id': 'fc1ce712-f56d-5831-be86-2b82ea445f5a', 'address': ('192.168.1.14', 6000)}
  ```
* **Conclusión Teórica:** El UUID identifica *qué* es la entidad independientemente de *dónde* esté. Sin embargo, un UUID por sí solo no permite el enrutamiento directo (semántica de enrutamiento nula), requiriendo un servicio de resolución explícito $\text{UUID} \mapsto (\text{IP}, \text{Puerto})$.

---

### 🔹 Ejercicio 2: Localización de Entidades por Broadcast (`Exercise2/`)

* **Objetivo:** Analizar la resolución de nombres planos mediante difusión (Broadcast) en Capa de Enlace (ARP) y Capa de Aplicación (UDP Sockets).
* **Implementación:**
  * **[`entity.py`](file:///C:/Users/User/Desktop/8vo/Sistemas-Distribuidos/Sistemas-Distribuidos/Workshop3/Exercise2/entity.py):** Entidad (Estudiante A) que escucha en el puerto UDP `50000`. Al recibir un mensaje que coincide con su `ENTITY_ID` (`studentA-Name`), responde con su tupla `studentA-Name:IP`.
  * **[`finder.py`](file:///C:/Users/User/Desktop/8vo/Sistemas-Distribuidos/Sistemas-Distribuidos/Workshop3/Exercise2/finder.py):** Cliente de búsqueda que envía un paquete Broadcast a `255.255.255.255:50000` y espera respuesta con un timeout socket de 3 segundos.
* **Inspección ARP (Capa de Enlace):**
  * Se analizó la tabla ARP del sistema mediante `arp -a` y se verificó la resolución de direcciones IP a MAC tras hacer `ping 192.168.1.1`.
* **Resultados de Ejecución:**
  * **Búsqueda Exitosa (`studentA-Name`):**  
    `finder.py` recibe la respuesta `studentA-Name:192.168.1.14`.
  * **Búsqueda Fallida (`studentB-Name`):**  
    Tras transcurrir los 3 segundos de timeout, `finder.py` concluye con `Entity not found`.
* **Limitaciones de Escalabilidad:**
  1. *Tormentas de Interrupciones de CPU:* Cada nodo en la LAN debe procesar la trama a nivel de hardware y SO ($O(N)$ sobrecarga de red).
  2. *Límites de Enrutamiento:* Los routers no reenvían paquetes broadcast por diseño, limitando la resolución exclusivamente a la subred local.

---

### 🔹 Ejercicio 3: Punteros de Reenvío / Forwarding Pointers (`Exercise3/forwarding.py`)

* **Objetivo:** Evaluar el mecanismo de punteros de reenvío en migraciones, la optimización mediante atajos (shortcuts) y el efecto del fallo de un nodo intermedio.
* **Implementación:**
  * Se define una cadena de movilidad inicial: `A -> B -> C -> D -> 192.168.1.50:5000`.
  * **Resolución Inicial:** Requiere recorrer la cadena completa ($4$ saltos).
  * **Optimización por Atajo:** Se actualiza la puntería directa de `A` a la ubicación final (`locations["A"] = "192.168.1.50:5000"`), reduciendo el costo a $1$ solo salto (reducción de latencia del 75%).
  * **Simulación de Fallo:** Se elimina el registro del nodo intermedio `C` (`del locations["C"]`).
* **Resultados Obtenidos:**
  ```text
  === Initial chain resolution ===
  Following: A -> B
  Following: B -> C
  Following: C -> D
  Following: D -> 192.168.1.50:5000
  Final address: 192.168.1.50:5000
  Number of hops: 4

  === After shortcut optimization ===
  Following: A -> 192.168.1.50:5000
  Final address: 192.168.1.50:5000
  Number of hops: 1

  === Simulating failure: del locations['C'] ===
  1. Running resolution via shortcut (from A):
  Following: A -> 192.168.1.50:5000
  Final address: 192.168.1.50:5000
  Number of hops: 1

  2. Running original chain again (restoring A -> B):
  Following: A -> B
  Following: B -> C
  Final address: C
  Number of hops: 2
  Observation: Chain broken at missing node C! Target unreached.
  ```
* **Conclusión:** Aunque los punteros de reenvío ofrecen costo de actualización $O(1)$ durante la migración, las cadenas largas introducen latencia de RTT acumulada $O(k)$ y alta vulnerabilidad ante caídas de nodos intermedios.

---

### 🔹 Ejercicio 4: Anillo Chord - Tabla Hash Distribuida (`Exercise4/chord.py` & `finger.py`)

* **Objetivo:** Implementar la topología en anillo y tablas finger de Chord con hashing consistente de espacio $m=5$ ($2^5 = 32$ posiciones).
* **Configuración del Sistema:**
  * Nodos activos en el anillo: $\mathcal{N} = \{1, 4, 9, 11, 14, 18, 20, 21, 28\}$.
  * Regla del Sucesor: La clave $k$ se asigna al menor nodo $n \in \mathcal{N}$ tal que $n \ge k \pmod{32}$. Si $k > \max(\mathcal{N})$, da la vuelta circular al primer nodo ($1$).
  * Regla de Finger Table: Para un nodo $p$, la entrada $i$ ($1 \le i \le 5$) apunta a $\text{succ}((p + 2^{i-1}) \pmod{32})$.

* **Resultados Mapeo de Claves (Parte A):**
  | Clave ($k$) | Sucesor ($\text{succ}(k)$) | Justificación |
  | :---: | :---: | :--- |
  | **3** | **4** | Menor nodo $\ge 3$ |
  | **8** | **9** | Menor nodo $\ge 8$ |
  | **12** | **14** | Nodos 9, 11 son $< 12 \implies 14$ |
  | **19** | **20** | Menor nodo $\ge 19$ |
  | **26** | **28** | Menor nodo $\ge 26$ |
  | **30** | **1** | Da la vuelta al módulo 32 (wrap-around) |

* **Tablas Finger Calculadas (Parte B):**
  ```text
  Node  1: FT = [4, 4, 9, 9, 18]
  Node  4: FT = [9, 9, 9, 14, 20]
  Node  9: FT = [11, 11, 14, 18, 28]
  Node 11: FT = [14, 14, 18, 20, 28]
  Node 14: FT = [18, 18, 18, 28, 1]
  Node 18: FT = [20, 20, 28, 28, 4]
  Node 20: FT = [21, 28, 28, 28, 4]
  Node 21: FT = [28, 28, 28, 1, 9]
  Node 28: FT = [1, 1, 1, 4, 14]
  ```

* **Traza de Búsqueda y Rutas (Parte C):**
  * **Lookup Clave 26 desde Nodo 1:**
    $$\text{Ruta: } 1 \xrightarrow{FT_1[5]} 18 \xrightarrow{FT_{18}[2]} 20 \xrightarrow{FT_{20}[1]} 21 \xrightarrow{\text{succ}} 28 \quad \implies \mathbf{4 \text{ saltos}}$$
  * **Lookup Clave 12 desde Nodo 28:**
    $$\text{Ruta: } 28 \xrightarrow{FT_{28}[4]} 4 \xrightarrow{FT_4[3]} 9 \xrightarrow{FT_9[1]} 11 \xrightarrow{\text{succ}} 14 \quad \implies \mathbf{4 \text{ saltos}}$$
* **Complejidad:** La resolución de claves en Chord garantiza una complejidad de enrutamiento de $O(\log N)$ saltos.

---

### 🔹 Ejercicio 5: Servicio de Localización Jerárquico - HLS (`Exercise5/hls.py`)

* **Objetivo:** Simular un servicio de localización jerárquico que organiza el espacio de nombres en un árbol de dominios administrativos con punteros descendentes (downward pointers) y búsqueda con sentido de localidad.
* **Estructura del Árbol de Dominios:**
  ```text
                  ROOT
                 /    \
            AMERICA  EUROPE
            /     \
       ECUADOR    USA
       /     \
    IBARRA  QUITO
  ```
* **Mecanismo de Búsqueda:**
  1. Inspeccionar entidades registradas localmente en el nodo hoja.
  2. Si no se encuentra, ascender al nodo padre hasta encontrar un nodo directorio que posea un puntero descendente hacia el subárbol de la entidad (Ancestro Común Más Cercano - LCA).
  3. Seguir los punteros descendentes hasta la hoja destino.

* **Resultados de las Pruebas:**
  * **Lookup `server01` desde `IBARRA` (Local):** Encontrado directamente en `IBARRA` (`10.0.1.20`).
  * **Lookup `server02` desde `IBARRA` (Explotación de Localidad):**  
    Ruta: `IBARRA -> ECUADOR -> QUITO -> server02` (`10.0.2.30`).  
    *Observación Clave:* La búsqueda asciende únicamente hasta `ECUADOR` (el LCA) y desciende a `QUITO`. Nunca toca `AMERICA` ni `ROOT`, protegiendo la infraestructura global de tráfico regional.
  * **Lookup `server99` (Inexistente):**  
    Ruta: `IBARRA -> ECUADOR -> AMERICA -> ROOT` $\implies$ `Entity not found`. Asciende hasta la raíz antes de fallar.
  * **Migración de Entidad (`server01` de `IBARRA` a `QUITO` con IP `10.0.2.25`):**  
    Solo se actualizan los punteros en `IBARRA`, `QUITO` y `ECUADOR`. Los registros en `AMERICA` y `ROOT` permanecen intactos, demostrando un costo de actualización localizado.

---

### 🔹 Ejercicio 6: Espacio de Nombres e Inodos POSIX (`Exercise6/six.py`)

* **Objetivo:** Analizar la resolución de nombres en un grafo de sistema de archivos comparando Enlaces Rígidos (Hard Links) y Enlaces Simbólicos (Soft Links) ante renombrado y eliminación.
* **Estructura en Memoria Simbólica:**
  * Inodo `1001`: Archivo físico con contenido `"Distributed Systems"`.
  * `data/original.txt`: Apunta a Inodo `1001` (recuento de referencias = 2 al crear el hard link).
  * `hardlink.txt`: Apunta directamente al Inodo `1001`.
  * `softlink.txt`: Apunta al string de ruta `"data/original.txt"` (puntero indirecto).

* **Evaluación del Comportamiento:**
  ```text
  === INITIAL STATE ===
  Reading hardlink: Distributed Systems
  Reading softlink: Distributed Systems

  === RENAME ORIGINAL (mv data/original.txt data/renamed.txt) ===
  Reading hardlink after rename: Distributed Systems
  Reading softlink after rename:
  ERROR: Broken symbolic link: softlink.txt -> data/original.txt

  === DELETE RENAMED FILE (rm data/renamed.txt) ===
  Reading hardlink after deletion: Distributed Systems
  Reading softlink after deletion:
  ERROR: Broken symbolic link: softlink.txt -> data/original.txt
  ```

* **Conclusión:**
  * **Hard Links (Enlaces Rígidos):** Apuntan directamente al número de inodo. Renombrar o eliminar la entrada original solo decrementa el contador de referencias (`st_nlink`). Los datos persisten y siguen siendo accesibles a través de `hardlink.txt`.
  * **Soft Links (Enlaces Simbólicos):** Contienen únicamente la ruta como texto. Al renombrar o eliminar el destino original, el enlace se rompe y genera una referencia colgante (*dangling pointer* / error `ENOENT`).

---

## 📊 Matriz Comparativa de Esquemas de Nombrado

| Mecanismo | Latencia de Lookup | Costo de Actualización / Migración | Escalabilidad | Vulnerabilidad a Fallos |
| :--- | :---: | :---: | :---: | :--- |
| **Broadcast (ARP / UDP)** | $O(1)$ (LAN) | $O(1)$ (Sin tablas) | Baja (Limitado a subred local) | Resiliente a caídas; vulnerable a saturación por tormentas |
| **Forwarding Pointers** | $O(k)$ saltos | $O(1)$ en nodo previo | Baja (Las cadenas crecen con la movilidad) | Alta (Si un nodo intermedio cae, se rompe la cadena) |
| **Chord DHT** | $O(\log N)$ saltos | $O(\log^2 N)$ actualizaciones | Alta (Escala a millones de nodos) | Alta robustez gracias a tablas finger y listas de sucesores |
| **HLS (Jerárquico)** | $O(\text{altura del LCA})$ | Localizado en el LCA | Muy Alta (Exploita la localidad geográfica) | Fallos en nodos altos afectan lookups inter-dominio |
| **FS Hard Links** | $O(1)$ inodo directo | $O(1)$ refcount | Limitado a un solo sistema de archivos | Alta durabilidad (los datos se conservan si `refcount` $>0$) |
| **FS Soft Links** | $O(\text{longitud de ruta})$ | $O(1)$ cambio de texto | Alta (Funciona entre montajes/redes) | Frágil (Sensible al renombrado o borrado del destino) |

---

## 🚀 Guía de Ejecución de Código

Para verificar la ejecución de las soluciones de cada ejercicio, ejecuta los siguientes comandos desde la terminal en el directorio raíz `Workshop3`:

```bash
# Ejercicio 1: Identificadores y Direcciones
python Exercise1/identifiers.py

# Ejercicio 2: Búsqueda por Broadcast UDP (Abrir 2 terminales)
# Terminal 1 (Servidor Entidad):
python Exercise2/entity.py
# Terminal 2 (Cliente Finder - Búsqueda exitosa y fallida):
python Exercise2/finder.py studentA-Name
python Exercise2/finder.py studentB-Name

# Ejercicio 3: Punteros de Reenvío y Atajos
python Exercise3/forwarding.py

# Ejercicio 4: Anillo Chord y Tablas Finger
python Exercise4/chord.py

# Ejercicio 5: Servicio de Localización Jerárquico (HLS)
python Exercise5/hls.py

# Ejercicio 6: Inodos, Hard Links y Soft Links
python Exercise6/six.py
```

---

## 📌 Conclusiones Finales

1. **Identidad vs. Ubicación:** La distinción entre un identificador (opaco, invariante) y una dirección (topológica, mutable) es el pilar fundamental para construir sistemas distribuidos móviles e inmunes a cambios de infraestructura.
2. **Trade-offs de Escalabilidad:** Los métodos planos por broadcast son ideales para autodescubrimiento en redes locales cero-configuración, pero inviables en redes WAN. Las estructuras como Chord logran escalabilidad logarítmica $O(\log N)$ descentralizada mediante hashing consistente.
3. **Explotación de Localidad (HLS):** Los esquemas jerárquicos permiten aislar las consultas y actualizaciones en el dominio regional más cercano (LCA), evitando cuellos de botella en la raíz de la jerarquía.
4. **Persistencia en Espacios de Nombres (POSIX):** La indirección de rutas (soft links) aporta flexibilidad entre sistemas de archivos a costa de fragilidad por referencias colgantes, mientras que la referencia directa por inodo (hard links) ofrece alta tolerancia a fallos a nivel de nombrado.
