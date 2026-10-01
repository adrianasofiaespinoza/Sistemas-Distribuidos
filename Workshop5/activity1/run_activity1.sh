#!/bin/bash
# Activity 1 - Start Docker topology

echo "=== Activity 1: Starting Docker topology ==="
echo "Starting 3 MySQL containers: primary, replica, shard2"

docker compose up -d

echo ""
echo "Waiting for containers to be ready..."
sleep 10

echo ""
echo "=== Container status ==="
docker ps

echo ""
echo "=== Verifying each node accepts connections ==="
echo "Pinging mysql-primary..."
docker exec mysql-primary mysqladmin ping -uroot -proot

echo "Pinging mysql-replica..."
docker exec mysql-replica mysqladmin ping -uroot -proot

echo "Pinging mysql-shard2..."
docker exec mysql-shard2 mysqladmin ping -uroot -proot

echo ""
echo "=== Activity 1 complete ==="
