# Activity 3 - Horizontal Sharding (PowerShell)

Write-Host "=== Activity 3: Horizontal Sharding ===" -ForegroundColor Cyan
Write-Host "Rule: Even IDs -> Shard 1 (mysql-primary), Odd IDs -> Shard 2 (mysql-shard2)"

Write-Host ""
Write-Host "Step 1: Creating schema on Shard 1 (mysql-primary)..." -ForegroundColor Yellow
docker exec mysql-primary mysql -uroot -proot -e "
CREATE DATABASE IF NOT EXISTS users_shard1;
CREATE TABLE IF NOT EXISTS users_shard1.users
  (id INT PRIMARY KEY, name VARCHAR(50), email VARCHAR(80), city VARCHAR(50));"

Write-Host ""
Write-Host "Step 2: Creating schema on Shard 2 (mysql-shard2)..." -ForegroundColor Yellow
docker exec mysql-shard2 mysql -uroot -proot -e "
CREATE DATABASE IF NOT EXISTS users_shard2;
CREATE TABLE IF NOT EXISTS users_shard2.users
  (id INT PRIMARY KEY, name VARCHAR(50), email VARCHAR(80), city VARCHAR(50));"

Write-Host ""
Write-Host "Step 3: Inserting EVEN IDs into Shard 1..." -ForegroundColor Yellow
docker exec mysql-primary mysql -uroot -proot users_shard1 -e "
INSERT INTO users VALUES
  (2, 'Ana Gomez',    'ana.gomez@mail.com',    'Bogota'),
  (4, 'Carlos Ruiz',  'carlos.ruiz@mail.com',  'Medellin'),
  (6, 'Lucia Perez',  'lucia.perez@mail.com',  'Cali');"

Write-Host ""
Write-Host "Step 4: Inserting ODD IDs into Shard 2..." -ForegroundColor Yellow
docker exec mysql-shard2 mysql -uroot -proot users_shard2 -e "
INSERT INTO users VALUES
  (1, 'Mario Lopez',  'mario.lopez@mail.com',  'Barranquilla'),
  (3, 'Sofia Torres', 'sofia.torres@mail.com', 'Cartagena'),
  (5, 'Diego Castro', 'diego.castro@mail.com', 'Bucaramanga');"

Write-Host ""
Write-Host "=== Querying each shard separately ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Shard 1 (Even IDs):" -ForegroundColor Yellow
docker exec mysql-primary mysql -uroot -proot users_shard1 -e "SELECT * FROM users ORDER BY id;"

Write-Host ""
Write-Host "Shard 2 (Odd IDs):" -ForegroundColor Yellow
docker exec mysql-shard2 mysql -uroot -proot users_shard2 -e "SELECT * FROM users ORDER BY id;"

Write-Host ""
Write-Host "=== Reconstructed logical result (manual UNION) ===" -ForegroundColor Cyan
Write-Host "id | name         | email                  | city"
Write-Host "----+---------------+------------------------+--------------"
Write-Host " 1 | Mario Lopez  | mario.lopez@mail.com   | Barranquilla  (Shard2)"
Write-Host " 2 | Ana Gomez    | ana.gomez@mail.com     | Bogota        (Shard1)"
Write-Host " 3 | Sofia Torres | sofia.torres@mail.com  | Cartagena     (Shard2)"
Write-Host " 4 | Carlos Ruiz  | carlos.ruiz@mail.com   | Medellin      (Shard1)"
Write-Host " 5 | Diego Castro | diego.castro@mail.com  | Bucaramanga   (Shard2)"
Write-Host " 6 | Lucia Perez  | lucia.perez@mail.com   | Cali          (Shard1)"

Write-Host ""
Write-Host "=== Activity 3 complete ===" -ForegroundColor Green
