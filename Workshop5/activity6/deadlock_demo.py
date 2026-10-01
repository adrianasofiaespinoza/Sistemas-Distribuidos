import mysql.connector
import threading
import time

cfg = dict(host="127.0.0.1", user="root", password="root", database="lab")
results = {}

def session_a():
    try:
        conn = mysql.connector.connect(**cfg, port=3306)
        conn.autocommit = False
        cur = conn.cursor()
        cur.execute("START TRANSACTION")
        cur.execute("UPDATE accounts SET balance = balance + 10 WHERE id = 1")
        print("[A] Locked row 1, waiting 2s before locking row 2...")
        time.sleep(2)
        cur.execute("UPDATE accounts SET balance = balance - 10 WHERE id = 2")
        conn.commit()
        results["A"] = "COMMITTED"
        print("[A] COMMITTED")
        cur.close(); conn.close()
    except mysql.connector.Error as e:
        results["A"] = f"ERROR {e.errno}: {e.msg}"
        print(f"[A] {results['A']}")

def session_b():
    time.sleep(0.5)  # let A lock row 1 first
    try:
        conn = mysql.connector.connect(**cfg, port=3306)
        conn.autocommit = False
        cur = conn.cursor()
        cur.execute("START TRANSACTION")
        cur.execute("UPDATE accounts SET balance = balance - 10 WHERE id = 2")
        print("[B] Locked row 2, waiting 2s before locking row 1...")
        time.sleep(2)
        cur.execute("UPDATE accounts SET balance = balance + 10 WHERE id = 1")
        conn.commit()
        results["B"] = "COMMITTED"
        print("[B] COMMITTED")
        cur.close(); conn.close()
    except mysql.connector.Error as e:
        results["B"] = f"ERROR {e.errno}: {e.msg}"
        print(f"[B] {results['B']}")

print("=== 6.1 Deadlock Demo ===")
t1 = threading.Thread(target=session_a)
t2 = threading.Thread(target=session_b)
t1.start(); t2.start()
t1.join(); t2.join()
print(f"\nSession A result: {results.get('A')}")
print(f"Session B result: {results.get('B')}")
