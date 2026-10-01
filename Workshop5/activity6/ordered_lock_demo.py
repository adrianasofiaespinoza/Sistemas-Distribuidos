import mysql.connector
import threading
import time

cfg = dict(host="127.0.0.1", user="root", password="root", database="lab")
results = {}

def session_a():
    conn = mysql.connector.connect(**cfg, port=3306)
    conn.autocommit = False
    cur = conn.cursor()
    cur.execute("START TRANSACTION")
    # Always lock BOTH rows in id order first
    cur.execute("SELECT * FROM accounts WHERE id IN (1,2) ORDER BY id FOR UPDATE")
    rows = cur.fetchall()
    print(f"[A] Acquired locks on rows 1,2. Rows: {rows}")
    time.sleep(1)
    cur.execute("UPDATE accounts SET balance = balance + 10 WHERE id = 1")
    cur.execute("UPDATE accounts SET balance = balance - 10 WHERE id = 2")
    conn.commit()
    results["A"] = "COMMITTED"
    print("[A] COMMITTED")
    cur.close(); conn.close()

def session_b():
    time.sleep(0.3)
    conn = mysql.connector.connect(**cfg, port=3306)
    conn.autocommit = False
    cur = conn.cursor()
    cur.execute("START TRANSACTION")
    print("[B] Attempting to lock rows 1,2 in order (will block until A releases)...")
    cur.execute("SELECT * FROM accounts WHERE id IN (1,2) ORDER BY id FOR UPDATE")
    rows = cur.fetchall()
    print(f"[B] Acquired locks. Rows: {rows}")
    cur.execute("UPDATE accounts SET balance = balance - 10 WHERE id = 2")
    cur.execute("UPDATE accounts SET balance = balance + 10 WHERE id = 1")
    conn.commit()
    results["B"] = "COMMITTED"
    print("[B] COMMITTED")
    cur.close(); conn.close()

print("=== 6.2 Ordered Locking - No Deadlock ===")
t1 = threading.Thread(target=session_a)
t2 = threading.Thread(target=session_b)
t1.start(); t2.start()
t1.join(); t2.join()
print(f"\nSession A result: {results.get('A')}")
print(f"Session B result: {results.get('B')}")
