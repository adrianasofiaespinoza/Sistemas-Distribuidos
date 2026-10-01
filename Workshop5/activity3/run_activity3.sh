#!/bin/bash
# Activity 3 - Horizontal Sharding

echo "=== Activity 3: Horizontal Sharding ==="
echo "Rule: Even IDs -> Shard 1 (mysql-primary), Odd IDs -> Shard 2 (mysql-shard2)"

echo "Step 1: Creating schema on Shard 1 (mysql-primary)..."
docker exec mysql-primary mysql -uroot -proot -e "
CREATE DATABASE IF NOT EXISTS users_shard1;
CREATE TABLE IF NOT EXISTS users_shard1.users
  (id INT PRIMARY KEY, name VARCHAR(50), email VARCHAR(80), city VARCHAR(50));"

echo "Step 2: Creating schema on Shard 2 (mysql-shard2)..."
docker exec mysql-shard2 mysql -uroot -proot -e "
CREATE DATABASE IF NOT EXISTS users_shard2;
CREATE TABLE IF NOT EXISTS users_shard2.users
  (id INT PRIMARY KEY, name VARCHAR(50), email VARCHAR(80), city VARCHAR(50));"

echo "Step 3: Inserting EVEN IDs into Shard 1..."
docker exec mysql-primary mysql -uroot -proot users_shard1 -e "
INSERT INTO users VALUES
  (2, 'Ana Gomez',    'ana.gomez@mail.com',    'Bogota'),
  (4, 'Carlos Ruiz',  'carlos.ruiz@mail.com',  'Medellin'),
  (6, 'Lucia Perez',  'lucia.perez@mail.com',  'Cali');"

echo "Step 4: Inserting ODD IDs into Shard 2..."
docker exec mysql-shard2 mysql -uroot -proot users_shard2 -e "
INSERT INTO users VALUES
  (1, 'Mario Lopez',  'mario.lopez@mail.com',  'Barranquilla'),
  (3, 'Sofia Torres', 'sofia.torres@mail.com', 'Cartagena'),
  (5, 'Diego Castro', 'diego.castro@mail.com', 'Bucaramanga');"

echo ""
echo "=== Shard 1 (Even IDs) ==="
docker exec mysql-primary mysql -uroot -proot users_shard1 -e "SELECT * FROM users ORDER BY id;"

echo ""
echo "=== Shard 2 (Odd IDs) ==="
docker exec mysql-shard2 mysql -uroot -proot users_shard2 -e "SELECT * FROM users ORDER BY id;"

echo ""
echo "=== Activity 3 complete ==="
