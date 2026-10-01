-- ==========================================
-- 6.2 Consistent Locking Order - SESSION B
-- ==========================================
START TRANSACTION;
-- Always acquire locks in id order (1, then 2) - same order as A
SELECT * FROM accounts WHERE id IN (1,2) ORDER BY id FOR UPDATE;
UPDATE accounts SET balance = balance - 10 WHERE id=2;
UPDATE accounts SET balance = balance + 10 WHERE id=1;
COMMIT;
