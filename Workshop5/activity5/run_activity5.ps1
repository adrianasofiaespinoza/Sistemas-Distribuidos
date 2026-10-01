# Activity 5 - Read-after-write consistency (PowerShell)

Write-Host "=== Activity 5: Read-after-write consistency ===" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 1: Write on primary, immediately read from replica..." -ForegroundColor Yellow
Write-Host "--- PRIMARY: Performing write ---"
docker exec mysql-primary mysql -uroot -proot lab -e "
UPDATE accounts SET balance=balance+1 WHERE id=1;
SELECT id,balance,updated_at FROM accounts WHERE id=1;"

Write-Host ""
Write-Host "--- REPLICA: Reading immediately (may be stale) ---"
docker exec mysql-replica mysql -uroot -proot lab -e "SELECT id,balance,updated_at FROM accounts WHERE id=1;"

Write-Host ""
Write-Host "Step 2: Getting GTID set from primary..." -ForegroundColor Yellow
$gtid = docker exec mysql-primary mysql -uroot -proot -se "SELECT @@GLOBAL.gtid_executed"
Write-Host "GTID set: $gtid"

Write-Host ""
Write-Host "Step 3: Waiting for replica to catch up using WAIT_FOR_EXECUTED_GTID_SET..." -ForegroundColor Yellow
docker exec mysql-replica mysql -uroot -proot -e "SELECT WAIT_FOR_EXECUTED_GTID_SET('$gtid',5);"

Write-Host ""
Write-Host "Step 4: Reading from replica after GTID wait..." -ForegroundColor Yellow
docker exec mysql-replica mysql -uroot -proot lab -e "SELECT id,balance,updated_at FROM accounts WHERE id=1;"

Write-Host ""
Write-Host "Result: 0 = set applied (consistent read), 1 = timeout (stale read)" -ForegroundColor Magenta
Write-Host "=== Activity 5 complete ===" -ForegroundColor Green
