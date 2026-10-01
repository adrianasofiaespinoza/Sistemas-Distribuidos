#!/bin/bash
# Activity 2 - Primary-Replica Replication

echo "=== Activity 2: Primary-Replica Replication ==="

echo "Step 1: Creating replication user on primary..."
docker exec mysql-primary mysql -uroot -proot -e "
CREATE USER IF NOT EXISTS 'repl'@'%' IDENTIFIED BY 'repl';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;"

echo "Step 2: Configuring replica..."
docker exec mysql-replica mysql -uroot -proot -e "
STOP REPLICA;
CHANGE REPLICATION SOURCE TO
  SOURCE_HOST='mysql-primary',
  SOURCE_USER='repl',
  SOURCE_PASSWORD='repl',
  SOURCE_AUTO_POSITION=1,
  GET_SOURCE_PUBLIC_KEY=1;
START REPLICA;"

echo "Step 3: Checking replica status..."
docker exec mysql-replica mysql -uroot -proot -e "SHOW REPLICA STATUS\G"

echo "Step 4: Creating test data on primary..."
docker exec mysql-primary mysql -uroot -proot lab -e "
CREATE TABLE IF NOT EXISTS replication_test (id INT PRIMARY KEY, note VARCHAR(80));
INSERT INTO replication_test VALUES (1,'created on primary');"

echo "Step 5: Verifying data on replica..."
sleep 3
docker exec mysql-replica mysql -uroot -proot lab -e "SELECT * FROM replication_test;"

echo "=== Activity 2 complete ==="
