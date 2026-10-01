-- ==========================================
-- 4.2 Fix with SELECT FOR UPDATE - SESSION A
-- ==========================================
START TRANSACTION;
SELECT balance FROM accounts WHERE id=1 FOR UPDATE;
-- Row is now locked; Session B will WAIT here
UPDATE accounts SET balance = balance + 100 WHERE id=1;
COMMIT;
