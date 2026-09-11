# Workshop 4: Domain Name System (DNS) and Lightweight Directory Access Protocol (LDAP)

**Course:** Distributed Systems (Sistemas Distribuidos)  
**Author:** Dario Pomasqui  
**Institution:** Universidad Yachay Tech  
**Date:** September 2026  

---

## Overview

This repository contains the complete implementation and technical documentation for **Workshop 4** of the Distributed Systems course. The workshop explores name resolution and centralized directory services in distributed environments through four main parts:

1. **Part A: DNS Diagnostic Queries (`nslookup` CLI)**  
   Querying and analyzing A, PTR, MX, NS, SOA, and CNAME records, examining packet headers in debug mode, and handling non-existent domains (`NXDOMAIN`).
2. **Part B: Programmatic DNS Resolutions (`dnspython`)**  
   Automating DNS resolution routines in Python using custom resolvers, low-level UDP wire message inspection (`dns.message`), reverse lookups (`dns.reversename`), and exception handling (`dns.resolver.NXDOMAIN`).
3. **Part C: OpenLDAP Directory Service Administration**  
   Designing and emulating the Directory Information Tree (DIT), provisioning structural entries using LDIF files (`base.ldif` and `user.ldif`), performing subtree searches (`ldapsearch`), and executing user identity authentication in Python via `ldap3`.
4. **Part D: Special Activity — Publisher-Subscriber System with LDAP Service Discovery**  
   Extending the ZeroMQ Pub/Sub architecture from Workshop 2 by replacing static IP/Port configurations with a dynamic LDAP-based service registry (`ou=Services,dc=example,dc=com`). Publishers automatically register active endpoints (`ipHostNumber`, `ipServicePort`), while Subscribers dynamically discover endpoints at runtime.

---

## Directory Structure

```
Workshop4/
│── README.md                        # Workshop 4 documentation & execution guide
│── informe.tex                      # Complete LaTeX report source file (English)
│── informe.pdf                      # Compiled PDF report
│── report.tex                       # Backup LaTeX source
│── deber.pdf                        # Assignment instructions document
│── imagenes/                        # Real terminal execution screenshots
│   ├── logo1.png, logo2.png
│   ├── salida1.png ... salida9.png  # Part A nslookup captures
│   ├── salida10.png, salida10_parte2.png # Part B dnspython execution
│   ├── salida11.png                 # Part C LDAP search & auth execution
│   └── salida12.png, salida12_parte2.png # Part D Pub/Sub + LDAP execution
│
├── Parte_A_DNS_CLI/                 # Part A: DNS Diagnostic Queries
│   ├── run_nslookup_tests.py        # Automation script for nslookup execution
│   └── nslookup_results.json        # Structured JSON logs of CLI query outputs
│
├── Parte_B_DNS_Python/              # Part B: Automated DNS via dnspython
│   ├── dns_part_b.py                # Python script for exercises A1-A9 using dnspython
│   └── dnspython_results.json       # JSON output results of dnspython queries
│
├── Parte_C_OpenLDAP/                # Part C: Directory Service & Authentication
│   ├── base.ldif                    # LDIF definitions for People & Groups OUs
│   ├── user.ldif                    # LDIF definition for user Francisco Hidrobo
│   ├── ldap_part_c.py               # Python script for LDAP binding, search & auth
│   └── ldap_results.json            # JSON output of directory search operations
│
└── Parte_D_PubSub_LDAP/             # Part D: Special Activity - Pub/Sub Service Registry
    ├── pubsub_ldap.py               # Integrated ZeroMQ Pub/Sub with LDAP Discovery
    └── pubsub_ldap_results.json     # Execution logs of publishers & subscribers
```

---

## Component Details & Execution

### Part A: DNS Queries (`nslookup`)
Interactive network diagnostic queries executed against target domains (`yachaytech.edu.ec`, `8.8.8.8`, `hpc.cedia.edu.ec`, `www.microsoft.com`):
* **A Record:** Resolves IPv4 host address (`190.103.191.42`).
* **PTR Record:** Performs reverse lookup (`8.8.8.8` $\rightarrow$ `dns.google`).
* **MX Record:** Obtains mail server (`yachaytech-edu-ec.mail.protection.outlook.com`).
* **NS Record:** Obtains authoritative name servers (`dominiosecuador.ec`, `cloudns.net`).
* **SOA Record:** Inspects primary NS (`mname`), contact email (`rname`), and zone serial (`2026082103`).
* **CNAME Record:** Identifies canonical aliases (`www.microsoft.com-c-3.edgekey.net`).
* **Debug Mode:** Inspects header transaction ID, query flags (`QR`, `RD`, `RA`), and TTL.

### Part B: Python DNS Resolutions (`dns_part_b.py`)
To run the automated Python DNS suite:
```bash
cd Parte_B_DNS_Python
python dns_part_b.py
```
Key features:
* Overrides local default resolvers (`dns.resolver.Resolver(configure=False)`).
* Builds raw wire-format query messages (`dns.query.udp`).
* Catches non-existent domain exceptions (`dns.resolver.NXDOMAIN`).

### Part C: OpenLDAP Administration (`ldap_part_c.py`)
To provision the directory structures and execute LDAP operations:
```bash
cd Parte_C_OpenLDAP

# Provision OUs and User Entry (Linux/OpenLDAP environment)
sudo ldapadd -x -D cn=admin,dc=example,dc=com -W -f base.ldif
sudo ldapadd -x -D cn=admin,dc=example,dc=com -W -f user.ldif

# Run Python search and authentication
python ldap_part_c.py
```

### Part D: Pub/Sub System with LDAP Service Discovery (`pubsub_ldap.py`)
To run the integrated distributed Pub/Sub system:
```bash
cd Parte_D_PubSub_LDAP
python pubsub_ldap.py
```
Workflow:
1. **Publisher Initialization:** Connects to LDAP and registers service endpoints under `ou=Services,dc=example,dc=com` with attributes `ipHostNumber` and `ipServicePort`.
2. **Subscriber Discovery:** Queries LDAP for service target names (`WEATHER`, `FINANCE`, `SPORTS`), dynamically retrieves IP and port, and connects via ZeroMQ (`zmq.SUB`).

---

## Report & Verification

The formal LaTeX document is available in [informe.tex](informe.tex) and has been compiled into [informe.pdf](informe.pdf).

To recompile the PDF report using MiKTeX / TeX Live:
```bash
pdflatex -interaction=nonstopmode informe.tex
```

---

**Author:** Dario Pomasqui  
**Course:** Distributed Systems — Universidad Yachay Tech  
