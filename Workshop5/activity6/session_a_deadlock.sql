-- ==========================================
-- 6.1 Deadlock Demo - SESSION A
-- ==========================================
START TRANSACTION;
UPDATE accounts SET balance = balance + 10 WHERE id=1;
-- Wait for Session B to lock row 2 first
UPDATE accounts SET balance = balance - 10 WHERE id=2;
-- One of the sessions will get ERROR 1213 here
COMMIT;
