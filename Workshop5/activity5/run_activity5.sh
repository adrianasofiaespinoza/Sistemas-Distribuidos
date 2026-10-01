#!/bin/bash
# Activity 5 - Read-after-write consistency

echo "=== Activity 5: Read-after-write consistency ==="

echo "Step 1: Write on primary, read immediately from replica..."
echo "--- PRIMARY write ---"
docker exec mysql-primary mysql -uroot -proot lab -e "
UPDATE accounts SET balance=balance+1 WHERE id=1;
SELECT id,balance,updated_at FROM accounts WHERE id=1;"

echo ""
echo "--- REPLICA read (may be stale) ---"
docker exec mysql-replica mysql -uroot -proot lab -e "SELECT id,balance,updated_at FROM accounts WHERE id=1;"

echo ""
echo "Step 2: Getting primary GTID set..."
GTID=
echo "GTID: "

echo ""
echo "Step 3: Waiting for replica to catch up..."
docker exec mysql-replica mysql -uroot -proot -e "SELECT WAIT_FOR_EXECUTED_GTID_SET('',5);"

echo ""
echo "Step 4: Reading from replica after GTID wait..."
docker exec mysql-replica mysql -uroot -proot lab -e "SELECT id,balance,updated_at FROM accounts WHERE id=1;"

echo "=== Activity 5 complete ==="
