# Activity 2 - Primary-Replica Replication (PowerShell)

Write-Host "=== Activity 2: Primary-Replica Replication ===" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 1: Creating replication user on primary..." -ForegroundColor Yellow
docker exec mysql-primary mysql -uroot -proot -e "
CREATE USER IF NOT EXISTS 'repl'@'%' IDENTIFIED BY 'repl';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;"

Write-Host ""
Write-Host "Step 2: Configuring replica..." -ForegroundColor Yellow
docker exec mysql-replica mysql -uroot -proot -e "
STOP REPLICA;
CHANGE REPLICATION SOURCE TO
SOURCE_HOST='mysql-primary',
SOURCE_USER='repl',
SOURCE_PASSWORD='repl',
SOURCE_AUTO_POSITION=1,
GET_SOURCE_PUBLIC_KEY=1;
START REPLICA;"

Write-Host ""
Write-Host "Step 3: Checking replica status..." -ForegroundColor Yellow
docker exec mysql-replica mysql -uroot -proot -e "SHOW REPLICA STATUS\G"

Write-Host ""
Write-Host "Step 4: Creating test data on primary..." -ForegroundColor Yellow
docker exec mysql-primary mysql -uroot -proot lab -e "
CREATE TABLE IF NOT EXISTS replication_test (id INT PRIMARY KEY, note VARCHAR(80));
INSERT INTO replication_test VALUES (1,'created on primary');"

Write-Host ""
Write-Host "Step 5: Verifying data on replica..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
docker exec mysql-replica mysql -uroot -proot lab -e "SELECT * FROM replication_test;"

Write-Host ""
Write-Host "=== Activity 2 complete ===" -ForegroundColor Green
Write-Host "Question: Why is the replica read-only? What would happen if both accepted independent writes?" -ForegroundColor Magenta
