-- ==========================================
-- 4.2 Fix with SELECT FOR UPDATE - SESSION B
-- ==========================================
START TRANSACTION;
SELECT balance FROM accounts WHERE id=1 FOR UPDATE;
-- Will block until Session A commits
UPDATE accounts SET balance = balance - 50 WHERE id=1;
COMMIT;
