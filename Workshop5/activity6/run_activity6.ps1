# Activity 6 - Deadlock and Prevention (PowerShell)

Write-Host "=== Activity 6: Deadlock and Prevention ===" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 1: Resetting balances to 1000 for both accounts..." -ForegroundColor Yellow
docker exec mysql-primary mysql -uroot -proot lab -e "UPDATE accounts SET balance=1000 WHERE id IN (1,2);"
docker exec mysql-primary mysql -uroot -proot lab -e "SELECT id,owner,balance FROM accounts;"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Red
Write-Host "6.1 - DEADLOCK DEMO (requires 2 terminals)" -ForegroundColor Red
Write-Host "================================================================"
Write-Host "Connect with: docker exec -it mysql-primary mysql -uroot -proot lab"
Write-Host ""
Write-Host "SESSION A:                              SESSION B:"
Write-Host "START TRANSACTION;                      START TRANSACTION;"
Write-Host "UPDATE accounts SET balance=            UPDATE accounts SET balance="
Write-Host "  balance+10 WHERE id=1;  -- locks 1     balance-10 WHERE id=2;  -- locks 2"
Write-Host "(wait for B to lock row 2)              (wait for A to lock row 1)"
Write-Host "UPDATE accounts SET balance=            UPDATE accounts SET balance="
Write-Host "  balance-10 WHERE id=2;  -- CIRCULAR!   balance+10 WHERE id=1;  -- CIRCULAR!"
Write-Host ""
Write-Host "One session gets ERROR 1213 (deadlock victim). The other completes." -ForegroundColor Red
Write-Host ""

Write-Host "================================================================" -ForegroundColor Green
Write-Host "6.2 - FIX WITH CONSISTENT LOCKING ORDER" -ForegroundColor Green
Write-Host "================================================================"
Write-Host "In BOTH sessions, acquire rows in the SAME order first:"
Write-Host ""
Write-Host "START TRANSACTION;"
Write-Host "SELECT * FROM accounts WHERE id IN (1,2) ORDER BY id FOR UPDATE;"
Write-Host "-- then perform the session's specific updates"
Write-Host "COMMIT;"
Write-Host ""
Write-Host "This prevents circular waits -> no deadlock, just sequential blocking" -ForegroundColor Green
Write-Host ""

Write-Host "=== SQL for 6.1 Deadlock ==="
Write-Host "See: session_a_deadlock.sql and session_b_deadlock.sql"
Write-Host ""
Write-Host "=== SQL for 6.2 Ordered Locking ==="
Write-Host "See: session_a_ordered.sql and session_b_ordered.sql"
Write-Host ""
Write-Host "=== Activity 6 complete ===" -ForegroundColor Green
