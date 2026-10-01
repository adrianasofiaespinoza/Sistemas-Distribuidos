-- ==========================================
-- 6.1 Deadlock Demo - SESSION B
-- ==========================================
START TRANSACTION;
UPDATE accounts SET balance = balance - 10 WHERE id=2;
-- Wait for Session A to lock row 1 first
UPDATE accounts SET balance = balance + 10 WHERE id=1;
-- One of the sessions will get ERROR 1213 here
COMMIT;
