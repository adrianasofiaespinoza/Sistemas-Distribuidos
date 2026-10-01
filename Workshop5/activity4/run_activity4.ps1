# Activity 4 - Lost Update and Locking (PowerShell)
# NOTE: Steps 4.1 and 4.2 require TWO interactive terminals.
# This script automates setup and the single-session verification.

Write-Host "=== Activity 4: Lost Update and Locking ===" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 1: Setting up accounts table on primary..." -ForegroundColor Yellow
docker exec mysql-primary mysql -uroot -proot lab -e "
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
  id INT PRIMARY KEY,
  owner VARCHAR(50),
  balance INT NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;
INSERT INTO accounts VALUES (1,'Alice',1000,NOW()),(2,'Bob',1000,NOW());"

Write-Host ""
Write-Host "=== Accounts created ===" -ForegroundColor Green
docker exec mysql-primary mysql -uroot -proot lab -e "SELECT * FROM accounts;"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Red
Write-Host "4.1 - LOST UPDATE DEMO (requires 2 terminals)" -ForegroundColor Red
Write-Host "================================================================"
Write-Host "Open TWO terminals and connect with:"
Write-Host "  docker exec -it mysql-primary mysql -uroot -proot lab"
Write-Host ""
Write-Host "SESSION A:                              SESSION B:"
Write-Host "SET SESSION TRANSACTION                 SET SESSION TRANSACTION"
Write-Host "  ISOLATION LEVEL READ COMMITTED;         ISOLATION LEVEL READ COMMITTED;"
Write-Host "START TRANSACTION;                      START TRANSACTION;"
Write-Host "SELECT balance FROM accounts            SELECT balance FROM accounts"
Write-Host "  WHERE id=1;  -- sees 1000               WHERE id=1;  -- sees 1000"
Write-Host "-- computes 1000+100=1100               -- computes 1000-50=950"
Write-Host "UPDATE accounts SET balance=1100        "
Write-Host "  WHERE id=1;                           "
Write-Host "COMMIT;                                 UPDATE accounts SET balance=950"
Write-Host "                                          WHERE id=1;"
Write-Host "                                        COMMIT;"
Write-Host ""
Write-Host "Expected: 1050  |  Actual result will be: 950 (B overwrites A)" -ForegroundColor Red
Write-Host ""

Write-Host "================================================================" -ForegroundColor Green
Write-Host "4.2 - FIX WITH SELECT ... FOR UPDATE" -ForegroundColor Green
Write-Host "================================================================"

Write-Host "Resetting balance to 1000..."
docker exec mysql-primary mysql -uroot -proot lab -e "UPDATE accounts SET balance=1000 WHERE id=1;"

Write-Host ""
Write-Host "SESSION A:                              SESSION B:"
Write-Host "START TRANSACTION;                      START TRANSACTION;"
Write-Host "SELECT balance FROM accounts            SELECT balance FROM accounts"
Write-Host "  WHERE id=1 FOR UPDATE;  -- LOCKS!       WHERE id=1 FOR UPDATE;  -- WAITS"
Write-Host "UPDATE accounts SET balance=            "
Write-Host "  balance+100 WHERE id=1;              "
Write-Host "COMMIT;                                 -- unblocks, sees 1100"
Write-Host "                                        UPDATE accounts SET balance="
Write-Host "                                          balance-50 WHERE id=1;"
Write-Host "                                        COMMIT;"
Write-Host ""
Write-Host "Checking final balance (expected 1050)..."
Start-Sleep -Seconds 2
docker exec mysql-primary mysql -uroot -proot lab -e "SELECT id, balance FROM accounts WHERE id=1;"
Write-Host ""
Write-Host "=== Activity 4 complete ===" -ForegroundColor Green
